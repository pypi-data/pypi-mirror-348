from stelar.client import Client as stelarClient
from stelar.client import Dataset

from stelar_synth_corr_data import generate_synthetic_data


def generate_synthetic_data_from_own_to_klms(data, name=None, credentials=None, num_samples=None, method="pearson"):
    """
    Generate synthetic data based on the input data and send it to the STELAR client.

    Parameters:
    data (pd.DataFrame): The input data to base the synthetic data on.
    credentials (dict): Dictionary containing the STELAR client credentials.

    num_samples (int): The number of samples to generate.

    Returns:
    pd.DataFrame: A DataFrame containing the synthetic data.
    """
    validate_credentials(credentials)

    # Create and return the stelar client instance
    stelar_client = stelarClient(base_url=credentials['url'],
                                 username=credentials['username'],
                                 password=credentials['password'])

    # Send the synthetic data to the STELAR client
    if name is None:
        name = "synthetic_data"
    if name in stelar_client.datasets:
        print("Dataset with name {} already exists.".format(name))
    else:
        stelar_client.datasets.create(title=name,
                                      name=name,
                                      description="Synthetic data generated from input data",
                                      author=credentials['username'])

    # Add the synthetic data to the dataset
    dataset = stelar_client.datasets[name]
    dataset.tags = ["synthetic", "correlation"]

    synth, correlation_diff = send_to_klms(dataset, data, credentials, num_samples, method)

    return synth, correlation_diff


def generate_synthetic_data_from_klms_to_klms(datasetname, resourcename, credentials=None, num_samples=None, method="pearson"):
    """
    Generate synthetic data based on the input data and send it to the STELAR client.

    Parameters:
    data (pd.DataFrame): The input data to base the synthetic data on.
    credentials (dict): Dictionary containing the STELAR client credentials.

    num_samples (int): The number of samples to generate.

    Returns:
    pd.DataFrame: A DataFrame containing the synthetic data.
    """
    validate_credentials(credentials)

    # Create and return the stelar client instance
    stelar_client = stelarClient(base_url=credentials['url'],
                                 username=credentials['username'],
                                 password=credentials['password'])

    # Load the dataset
    dataset = stelar_client.datasets[datasetname]
    # Locate the resource by name
    resource = next((res for res in dataset.resources if res.name == resourcename), None)

    if resource is None:
        raise ValueError(f"Resource '{resourcename}' not found in dataset '{datasetname}'")

    data = resource.read_dataframe()

    # Send the synthetic data to the STELAR client
    synth, correlation_diff = send_to_klms(dataset, data, credentials, num_samples, method)
    return synth, correlation_diff


def validate_credentials(credentials):
    # Validate the credentials
    if 'url' not in credentials:
        raise ValueError("Credentials must contain 'url' key under 'stelar_client'")

    if 'username' not in credentials:
        raise ValueError("Credentials must contain 'username' key under 'stelar_client'")

    if 'password' not in credentials:
        raise ValueError("Credentials must contain 'password' key under 'stelar_client'")

    if 'bucket' not in credentials:
        raise ValueError("Credentials must contain 'bucket' key under 'stelar_client'")
    return


def send_to_klms(dataset, data, credentials, num_samples=1000, method="pearson"):
    """
    Send the synthetic data to the STELAR client.
    Parameters:
    dataset (Dataset): The STELAR dataset to send the data to.
    synthetic_data (pd.DataFrame): The synthetic data to send.
    credentials (dict): Dictionary containing the STELAR client credentials.
    name (str): The name of the dataset.
    """
    synthetic_data, correlation_diff = generate_synthetic_data.generate_synthetic_data(data, num_samples, method)
    # Send the synthetic data to the STELAR client
    pot_res_name = "synth_{}_{}_{}".format(dataset.name, num_samples, method)
    res = next((res for res in dataset.resources if res.name == pot_res_name), None)
    if res:
        pot_res_name = pot_res_name + "_v{}".format(len(dataset.resources))
    s3path = "s3://{}/{}.csv".format(credentials['bucket'], pot_res_name)

    dataset.add_dataframe(synthetic_data, s3path)
    return synthetic_data, correlation_diff
