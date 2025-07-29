# STELAR Synthetic Correlated Data Generator

Work in progress.

## Overview
This module generates synthetic data with the same correlations as a given dataset.

## Installation
```bash
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps stelar_synth_corr_data
```
## Usage outside STELAR KLMS
```python
import pandas as pd
from stelar_synth_corr_data import generate_synthetic_data

# Load your dataset
data = pd.read_csv('your_dataset.csv')
# Generate synthetic data
synthetic_data = generate_synthetic_data(data, num_samples=1000)

# Save the synthetic data to a CSV file
synthetic_data.to_csv('synthetic_data.csv', index=False)
```

### Parameters
- `data`: The input dataset (Pandas DataFrame) from which to derive correlations.
- `num_samples`: The number of samples to generate in the synthetic dataset.
- `random_state`: An optional seed for reproducibility.

### Output
- A Pandas DataFrame containing the synthetic data with the same correlations as the input dataset.
- The synthetic data will have the same column names and data types as the input dataset.
- The synthetic data will be saved to a CSV file with the specified filename.


## Usage inside STELAR KLMS


### Load dataset from KLMS, create synthetic data and upload as resource:
```python
from stelar_synth_corr_data import stelar
datasetname = 'your_dataset_name'
resource_name = 'filename.csv'
data = stelar.generate_synthetic_data_from_klms_to_klms(
    datasetname, resource_name, num_samples=1000, credentials
)
```

### Use own dataset, create synthetic data and upload as resource:
```python
import pandas as pd
from stelar_synth_corr_data import stelar
df = pd.read_csv('your_dataset.csv')
resource_name = 'filename.csv'
data = stelar.generate_synthetic_data_from_own_to_klms(
    df, resource_name, num_samples=1000, credentials
)
```

### Parameters
- `data`: The input dataset (Pandas DataFrame) from which to derive correlations.
- `num_samples`: The number of samples to generate in the synthetic dataset.
- `random_state`: An optional seed for reproducibility.
- `datasetname`: The name of the dataset in KLMS (if using KLMS).
- `resource_name`: The name of the resource to save the synthetic data to in KLMS (if using KLMS).
- `credentials`: A dictionary containing the credentials for accessing KLMS (if using KLMS).

#### To use this module inside STELAR KLMS, you need to have the following credentials:
- `username`: Your STELAR KLMS username.
- `password`: Your STELAR KLMS password.
- `url`: The URL of the STELAR KLMS instance.
- `bucket`: The name of the bucket where the dataset is stored.

For example:
```python
credentials = {
    'username': 'your_username',
    'password': 'your_password',
    'url': 'https://klms.stelar.gr/stelar',
    'bucket': 'klms-bucket'
}
```

### Output
- A Pandas DataFrame containing the synthetic data with the same correlations as the input dataset.
- The synthetic data will have the same column names and data types as the input dataset.
- The synthetic data will be saved to a CSV file with the specified filename.


