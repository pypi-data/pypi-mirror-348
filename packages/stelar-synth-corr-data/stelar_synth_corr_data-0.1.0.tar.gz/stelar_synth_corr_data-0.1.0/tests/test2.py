# Write test to test functionality of src.stelar_synth_corr_data.py

import pytest

from src.stelar_synth_corr_data import generate_synthetic_data
import pandas as pd


# Test function to check the functionality of generate_synthetic_data
def test_generate_synthetic_data():
    # Load the input data
    df = pd.read_csv("stocks_small.csv", index_col='index')

    # Generate synthetic data
    num_samples = df.shape[0]  # Use the same number of samples as the input data
    synth_data, correlation_diff = generate_synthetic_data.generate_synthetic_data(df, num_samples)

    # Check if the shape of the synthetic data is correct
    assert synth_data.shape == (num_samples, df.shape[1]), "Synthetic data shape is incorrect"

    # Check if the synthetic data has the same columns as the input data
    assert all(synth_data.columns == df.columns), "Synthetic data columns do not match input data"

    # Check if the synthetic data has the same index as the input data
    assert all(synth_data.index == df.index[:num_samples]), "Synthetic data index does not match input data"




if __name__ == "__main__":
    # Run the test
    pytest.main(["-v", "tests/test.py test_generate_synthetic_data"])
