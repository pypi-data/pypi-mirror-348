# Ecocrop

Ecocrop is a Python package for modeling ecological suitability of crops based on climatic and edaphic parameters. It replicates the core logic of the R-based Recocrop model and supports both static and dynamic predictors, seasonal evaluation, and limiting-factor analysis.

## Features
- Flexible parameter setting for climate, soil, and terrain variables
- Support for dynamic (monthly) raster data with bi-monthly interpolation
- Evaluation across all possible planting windows in a year
- Limiting factor principle using Sprengel-Liebig's law
- Exportable raster output with metadata
- Summary statistics and plotting utilities
- Batch processing of multiple crops from a parameter table

## Installation
```bash
pip install ecocrop
```

## Usage
```python
from ecocrop import EcocropModel
import numpy as np

model = EcocropModel()
model.set_parameter("tmin", [10])
model.set_parameter("topmin", [20])
model.set_parameter("topmax", [30])
model.set_parameter("tmax", [40])

# Example with 12-month x 10x10 raster
temp_data = np.random.rand(12, 10, 10) * 35
model.set_predictor("temperature", temp_data, is_dynamic=True)

model.set_control("get_max", True)
suitability = model.run()
model.plot_suitability(suitability)
```

## Requirements
- numpy
- pandas
- rasterio
- matplotlib
- scipy

## License
MIT License
