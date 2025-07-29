import pandas as pd
import numpy as np


def generate_synthetic_data(data, num_samples=1000, method="pearson"):
    """
    Generate synthetic data based on the input data.

    Parameters:
    data (pd.DataFrame): The input data to base the synthetic data on.
    num_samples (int): The number of samples to generate.

    Returns:
    pd.DataFrame: A DataFrame containing the synthetic data.
    """

    non_numeric_cols = data.select_dtypes(exclude=['number'])
    if non_numeric_cols.shape[1] > 0:
        raise ValueError("Input data contains non-numeric columns. Only numeric data is supported.")

    # Compute correlation matrix C on input data
    C = data.corr(numeric_only=False, method=method).values

    # Generate correlated data using the correlation matrix
    correlated_data = generate_correlated_data(C, num_samples)

    # Convert the correlated data to a DataFrame
    synthetic_data = pd.DataFrame(correlated_data, columns=data.columns)

    if data.shape[0] == num_samples:
        # Ensure same index
        synthetic_data.index = data.index

    # Ensure the synthetic data has the same dtypes as the input data
    for col in data.columns:
        if data[col].dtype == 'object':
            synthetic_data[col] = synthetic_data[col].astype('object')
        elif data[col].dtype == 'category':
            synthetic_data[col] = synthetic_data[col].astype('category')
        else:
            synthetic_data[col] = synthetic_data[col].astype(data[col].dtype)

    # Check difference in correlations between generated data and input data
    generated_corr = synthetic_data.corr().values
    correlation_diff = np.abs(generated_corr - C).max()

    return synthetic_data, correlation_diff


def generate_correlated_data(C, num_samples):
    """
    Generate a dataset with correlation matrix C.

    Parameters:
    -----------
    C : numpy.ndarray
        n x n correlation matrix (must be positive semi-definite)
    num_samples : int
        Number of samples to generate

    Returns:
    --------
    X : numpy.ndarray
        Generated dataset with shape (num_samples, n)
    """
    n = C.shape[0]

    # Verify C is symmetric
    if not np.allclose(C, C.T):
        raise ValueError("Correlation matrix must be symmetric")

    # Compute Cholesky decomposition
    try:
        L = np.linalg.cholesky(C)
    except np.linalg.LinAlgError:
        # If C is not positive definite, try a regularization approach
        # Add a small positive value to the diagonal
        C_reg = C + np.eye(n) * 1e-8
        L = np.linalg.cholesky(C_reg)

    # Generate independent random variables
    Z = np.random.standard_normal((num_samples, n))

    # Transform to correlated variables
    X = Z @ L.T

    return X
