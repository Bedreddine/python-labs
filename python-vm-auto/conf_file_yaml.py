import yaml


def get_config(section: str):
    with open("env.yml", "r") as ymlConf:
        cfg = yaml.load(ymlConf, yaml.FullLoader)
    return cfg[section]


def cfg_azure_common():
    return get_config("azure")


def cfg_azure_vm():
    return get_config("azure-vm")


def cfg_azure_network():
    return get_config("azure-network")
