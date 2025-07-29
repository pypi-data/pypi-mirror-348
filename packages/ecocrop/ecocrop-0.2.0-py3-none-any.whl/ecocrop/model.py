import numpy as np
import pandas as pd
import rasterio
from rasterio.transform import from_origin
import os
import matplotlib.pyplot as plt
from scipy.ndimage import zoom

class EcocropModel:
    def __init__(self):
        self.meta = None
        self.params = {}
        self.predictors = {}
        self.duration = None
        self.control = {}
        self.time_series_keys = ["temperature", "precipitation"]
        self.has_error = False
        self.messages = []
        self.nyears = 1

    def set_parameter(self, name, values):
        if not name or not isinstance(values, (list, np.ndarray)):
            self.has_error = True
            self.messages.append(f"Invalid parameter '{name}'")
            return
        self.params[name.lower()] = np.array(values)
        if name.lower() == "duration":
            self.duration = self.params[name.lower()][0]

    def remove_parameter(self, name):
        if name == "ALL":
            self.params.clear()
            return True
        return self.params.pop(name.lower(), None) is not None

    def set_predictor(self, name, values, is_dynamic=False):
        if not name or not isinstance(values, (list, np.ndarray)):
            self.has_error = True
            self.messages.append(f"Invalid predictor '{name}'")
            return

        arr = np.array(values)
        if is_dynamic:
            expected_length = 12 * self.nyears
            if arr.shape[0] != expected_length:
                self.has_error = True
                self.messages.append(f"Length of dynamic predictor '{name}' should be {expected_length}")
                return
        self.predictors[name.lower()] = arr

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
            raise ValueError(f"RecocropModel error:\n{msg}")

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

    def _score_plateau(self, value, min_val, opt_min, opt_max, max_val):
        score = np.full(value.shape, np.nan, dtype=np.float32)
        score[(value >= opt_min) & (value <= opt_max)] = 1.0
        mask1 = (value >= min_val) & (value < opt_min)
        score[mask1] = (value[mask1] - min_val) / (opt_min - min_val)
        mask2 = (value > opt_max) & (value <= max_val)
        score[mask2] = (max_val - value[mask2]) / (max_val - opt_max)
        score[(value < min_val) | (value > max_val)] = 0.0
        return score

    def _expand_monthly_to_bimonthly(self, array):
        return zoom(array, (2, 1, 1), order=1)

    def _score_seasonal_time_series(self, variable, min_val, opt_min, opt_max, max_val):
        bimonthly = self._expand_monthly_to_bimonthly(variable)
        period = self.duration if self.duration else 12
        seasonal_scores = []

        for start in range(24):
            end = start + period
            if end > 24:
                window = np.concatenate((bimonthly[start:], bimonthly[:end - 24]), axis=0)
            else:
                window = bimonthly[start:end]

            window_score = self._score_plateau(window, min_val, opt_min, opt_max, max_val)
            suitability = np.nanmin(window_score, axis=0)
            seasonal_scores.append(suitability)

        return np.stack(seasonal_scores)

    def run(self):
        all_scores = []

        if all(k in self.params for k in ["tmin", "topmin", "topmax", "tmax"]):
            temp = self.predictors.get("temperature")
            if temp is not None and temp.ndim == 3:
                scores = self._score_seasonal_time_series(temp, self.params["tmin"], self.params["topmin"], self.params["topmax"], self.params["tmax"])
                all_scores.append(scores)

        if all(k in self.params for k in ["pmin", "popmin", "popmax", "pmax"]):
            prec = self.predictors.get("precipitation")
            if prec is not None and prec.ndim == 3:
                scores = self._score_seasonal_time_series(prec, self.params["pmin"], self.params["popmin"], self.params["popmax"], self.params["pmax"])
                all_scores.append(scores)

        for factor in ["ph", "salinity", "texture", "drainage", "slope", "elevation"]:
            if all(k in self.params for k in [f"{factor}min", f"{factor}optmin", f"{factor}optmax", f"{factor}max"]):
                raster = self.predictors.get(factor)
                if raster is not None and raster.ndim == 2:
                    score = self._score_plateau(
                        raster,
                        self.params[f"{factor}min"],
                        self.params[f"{factor}optmin"],
                        self.params[f"{factor}optmax"],
                        self.params[f"{factor}max"]
                    )
                    stacked_score = np.stack([score] * 24)
                    all_scores.append(stacked_score)

        if not all_scores:
            first = next(iter(self.predictors.values()))
            return np.full((24, *first.shape[-2:]), np.nan, dtype=np.float32)

        suitability_stack = np.nanmin(np.stack(all_scores), axis=0)

        if self.control.get("which_max", False):
            return np.nanargmax(suitability_stack, axis=0) + 1
        elif self.control.get("count_max", False):
            max_val = np.nanmax(suitability_stack, axis=0)
            return np.sum(suitability_stack == max_val, axis=0)
        elif self.control.get("get_max", False):
            return np.nanmax(suitability_stack, axis=0)

        return np.nanmin(suitability_stack, axis=0)

    def export_suitability(self, array, output_path):
        if self.meta is None:
            self.has_error = True
            self.messages.append("Raster metadata not available for export.")
            self.get_error()

        meta = self.meta.copy()
        meta.update({"dtype": 'float32', "count": 1})

        try:
            with rasterio.open(output_path, 'w', **meta) as dst:
                dst.write(array.astype('float32'), 1)
        except Exception as e:
            self.has_error = True
            self.messages.append(f"Error writing raster: {str(e)}")
            self.get_error()

    def summarize_suitability(self, array):
        return {
            "mean": float(np.nanmean(array)),
            "min": float(np.nanmin(array)),
            "max": float(np.nanmax(array)),
            "std": float(np.nanstd(array)),
            "count": int(np.sum(~np.isnan(array)))
        }

    def plot_suitability(self, array, title="Suitability Map"):
        plt.figure(figsize=(10, 6))
        plt.imshow(array, cmap='YlGn', interpolation='nearest')
        plt.title(title)
        plt.colorbar(label='Suitability')
        plt.axis('off')
        plt.show()

    def process_multiple_crops(self, df, crop_names, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        summary_stats = {}
        for crop in crop_names:
            self.params.clear()
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