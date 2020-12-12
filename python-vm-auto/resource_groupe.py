from azure.mgmt.resource import ResourceManagementClient
from conf_file_yaml import cfg_azure_common as common

RESOURCE_GROUP_NAME = common()["RESOURCE_GROUP_NAME"]
LOCATION = common()["LOCATION"]


def create_rg(rg_client: ResourceManagementClient):
    return rg_client.resource_groups.create_or_update(
        RESOURCE_GROUP_NAME,
        {
            "location": LOCATION
        }
    )
