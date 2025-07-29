import numpy as np
import pandas as pd
import rasterio
from rasterio.transform import from_origin
import os
import matplotlib.pyplot as plt

class EcocropModel:
    def __init__(self):
        self.parameters = {}
        self.predictors = {}
        self.dynamic_predictors = {}
        self.has_error = False
        self.messages = []
        self.nyears = 1  # default; should be set based on context
        self.meta = None

    def set_parameter(self, name, values):
        if not name or not isinstance(values, (list, np.ndarray)):
            self.has_error = True
            self.messages.append(f"Invalid parameter '{name}'")
            return
        self.parameters[name] = np.array(values)

    def remove_parameter(self, name):
        if name == "ALL":
            self.parameters.clear()
            return True
        return self.parameters.pop(name, None) is not None

    def set_predictor(self, name, values, is_dynamic=False):
        if not name or not isinstance(values, (list, np.ndarray)):
            self.has_error = True
            self.messages.append(f"Invalid predictor '{name}'")
            return

        values = np.array(values)
        if is_dynamic:
            expected_length = 12 * self.nyears
            if values.size % expected_length != 0:
                self.has_error = True
                self.messages.append(f"Length of dynamic predictor '{name}' should be multiple of {expected_length}")
                return
            self.dynamic_predictors[name] = values
        else:
            self.predictors[name] = values

    def load_raster_predictor(self, name, file_path):
        try:
            with rasterio.open(file_path) as src:
                data = src.read(1)
                self.set_predictor(name, data)
                if self.meta is None:
                    self.meta = src.meta
        except Exception as e:
            self.has_error = True
            self.messages.append(f"Error loading raster predictor '{name}': {str(e)}")

    def get_error(self):
        if self.has_error:
            msg = "\n".join(self.messages)
            self.has_error = False
            self.messages = []
            raise ValueError(f"EcocropModel error:\n{msg}")

    def load_crop_parameters(self, crop_name):
        mock_crop_db = {
            "maize": {
                "tmin": 8, "topmin": 18, "topmax": 30, "tmax": 40,
                "pmin": 300, "popmin": 500, "popmax": 800, "pmax": 1200,
                "gmin": 90, "gmax": 150
            },
            "wheat": {
                "tmin": 3, "topmin": 10, "topmax": 24, "tmax": 35,
                "pmin": 250, "popmin": 400, "popmax": 600, "pmax": 1000,
                "gmin": 100, "gmax": 180
            }
        }

        crop = mock_crop_db.get(crop_name.lower())
        if not crop:
            self.has_error = True
            self.messages.append(f"Crop parameters for '{crop_name}' not found.")
            return

        for key, value in crop.items():
            self.set_parameter(key, [value])

    def load_parameters_from_dataframe(self, df, crop_name):
        row = df[df['species'].str.lower() == crop_name.lower()]
        if row.empty:
            self.has_error = True
            self.messages.append(f"Crop '{crop_name}' not found in dataframe.")
            return

        row = row.iloc[0]
        try:
            self.set_parameter('topmin', [float(row['temp_opt_min'])])
            self.set_parameter('topmax', [float(row['temp_opt_max'])])
            self.set_parameter('gmin', [int(row['cycle_min'])])
            self.set_parameter('gmax', [int(row['cycle_max'])])
        except Exception as e:
            self.has_error = True
            self.messages.append(f"Error parsing parameters for '{crop_name}': {str(e)}")

    def run(self):
        try:
            temp = self.predictors.get('temperature')
            prec = self.predictors.get('precipitation')

            if temp is None or prec is None:
                raise ValueError("Both 'temperature' and 'precipitation' predictors are required.")

            tmin = self.parameters.get('tmin', [0])[0]
            topmin = self.parameters.get('topmin', [0])[0]
            topmax = self.parameters.get('topmax', [0])[0]
            tmax = self.parameters.get('tmax', [0])[0]

            pmin = self.parameters.get('pmin', [0])[0]
            popmin = self.parameters.get('popmin', [0])[0]
            popmax = self.parameters.get('popmax', [0])[0]
            pmax = self.parameters.get('pmax', [0])[0]

            tsuit = np.where((temp >= topmin) & (temp <= topmax), 1.0, 0.0)
            tsuit = np.where((temp >= tmin) & (temp < topmin), (temp - tmin) / (topmin - tmin), tsuit)
            tsuit = np.where((temp > topmax) & (temp <= tmax), (tmax - temp) / (tmax - topmax), tsuit)

            psuit = np.where((prec >= popmin) & (prec <= popmax), 1.0, 0.0)
            psuit = np.where((prec >= pmin) & (prec < popmin), (prec - pmin) / (popmin - pmin), psuit)
            psuit = np.where((prec > popmax) & (prec <= pmax), (pmax - prec) / (pmax - popmax), psuit)

            suitability = np.minimum(tsuit, psuit)
            return suitability

        except Exception as e:
            self.has_error = True
            self.messages.append(f"Error in run: {str(e)}")
            self.get_error()

    def export_suitability(self, suitability_array, output_path):
        if self.meta is None:
            self.has_error = True
            self.messages.append("Raster metadata not available for export.")
            self.get_error()

        meta = self.meta.copy()
        meta.update({"dtype": 'float32', "count": 1})

        try:
            with rasterio.open(output_path, 'w', **meta) as dst:
                dst.write(suitability_array.astype('float32'), 1)
        except Exception as e:
            self.has_error = True
            self.messages.append(f"Error writing suitability raster: {str(e)}")
            self.get_error()

    def process_multiple_crops(self, df, crop_names, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        summary_stats = {}
        for crop in crop_names:
            self.parameters.clear()
            self.load_parameters_from_dataframe(df, crop)
            self.get_error()
            suitability = self.run()
            self.get_error()
            output_path = os.path.join(output_dir, f"suitability_{crop.replace(' ', '_')}.tif")
            self.export_suitability(suitability, output_path)
            stats = self.summarize_suitability(suitability)
            summary_stats[crop] = stats
            print(f"Processed {crop} -> {output_path}\nStats: {stats}")
        return pd.DataFrame.from_dict(summary_stats, orient='index')

    def summarize_suitability(self, suitability_array):
        stats = {
            "mean": float(np.nanmean(suitability_array)),
            "min": float(np.nanmin(suitability_array)),
            "max": float(np.nanmax(suitability_array)),
            "std": float(np.nanstd(suitability_array)),
            "count": int(np.sum(~np.isnan(suitability_array)))
        }
        return stats

    def plot_suitability(self, suitability_array, title="Suitability Map"):
        plt.figure(figsize=(10, 6))
        plt.imshow(suitability_array, cmap='YlGn', interpolation='nearest')
        plt.title(title)
        plt.colorbar(label='Suitability')
        plt.axis('off')
        plt.show()