import json
import os
import argparse

def load_config(config_path:str):
    with open(config_path, 'r') as file:
        config = json.load(file)
    #check is API_KEY is defined in the environment and ovveride it in the config
    if "API_KEY" in os.environ:
        config["llm"]["api_key"] = os.environ["API_KEY"]
    #same for hf_token
    if "HF_TOKEN" in os.environ:
        config["hf"]["hf_token"] = os.environ["HF_TOKEN"]
    return config

def get_config():
    """
    Reads the -c input parameter and loads the configuration
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Path to the configuration file", default=".config/config.json")
    args = parser.parse_args()
    return load_config(args.config)
