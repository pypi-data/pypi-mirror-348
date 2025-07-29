
import os
import numpy as np
import pandas as pd
import rasterio
from recocrop import RecocropModel

def run_ecocrop_model(crop_params, raster_data, output_path, control_mode='get_max'):
    model = RecocropModel()

    # Set parameters
    for key, val in crop_params.items():
        model.set_parameter(key, [val])

    # Set predictors
    for name, array in raster_data.items():
        is_dynamic = array.ndim == 3  # 3D for dynamic predictors
        model.set_predictor(name, array, is_dynamic=is_dynamic)

    # Set control mode
    if control_mode:
        model.set_control(control_mode, True)

    # Run the model
    suitability = model.run()
    model.export_suitability(suitability, output_path)

    # Optionally return summary
    return model.summarize_suitability(suitability)

if __name__ == '__main__':
    # Mock example
    crop_params = {
        'tmin': 10, 'topmin': 20, 'topmax': 30, 'tmax': 40,
        'pmin': 400, 'popmin': 600, 'popmax': 800, 'pmax': 1000,
        'duration': 6
    }

    temp = np.random.rand(12, 50, 50) * 35
    prec = np.random.rand(12, 50, 50) * 200
    raster_data = {'temperature': temp, 'precipitation': prec}

    out_path = 'output_suitability.tif'
    stats = run_ecocrop_model(crop_params, raster_data, out_path)
    print(f"Suitability stats: {stats}")
