import yaml
import os

def load_config(config_path):
    """
    Load configuration from a YAML file specified by the config_path.
    
    Args:
        config_path (str): Path to the config.yaml file.
    
    Returns:
        dict: Configuration dictionary.
    
    Raises:
        FileNotFoundError: If the config file is not found.
        yaml.YAMLError: If the YAML file cannot be parsed.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file '{config_path}' not found. Please provide a valid config.yaml file.")
    
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        if config is None:
            raise ValueError(f"Configuration file '{config_path}' is empty.")
        return config
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing '{config_path}': {e}")
