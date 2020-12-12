from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
import networks as azure_net
import resource_groupe as azure_rg
import vm as azure_vm
import ping_vms as ping_test
from conf_file_yaml import cfg_azure_common as common
from conf_file_yaml import cfg_azure_vm as vm

SUBSCRIPTION_ID = common()["SUBSCRIPTION_ID"]
CLIENT_ID = common()["CLIENT_ID"]
SECRET = common()["SECRET"]
TENANT_ID = common()["TENANT_ID"]
RESOURCE_GROUP_NAME = common()["RESOURCE_GROUP_NAME"]

VM_NAMES_01 = vm()["VM_NAMES_01"]
VM_NAMES_02 = vm()["VM_NAMES_02"]


if __name__ == '__main__':
    # INIT
    credentials = ServicePrincipalCredentials(client_id=CLIENT_ID, secret=SECRET, tenant=TENANT_ID)
    resource_client = ResourceManagementClient(credentials, SUBSCRIPTION_ID)
    network_client = NetworkManagementClient(credentials, SUBSCRIPTION_ID)
    compute_client = ComputeManagementClient(credentials, SUBSCRIPTION_ID)

    # Resource Group
    azure_rg.create_rg(resource_client)

    # NETWORK
    azure_net.create_vnet(network_client)
    subnet = azure_net.create_subnet(network_client)
    azure_net.create_public_ip(network_client)
    nic_1, nic_2 = azure_net.create_interface(network_client, subnet)
    destination_ip = azure_net.get_private(network_client)

    # VM creation
    azure_vm.vm_create(compute_client, nic_1, VM_NAMES_01)
    azure_vm.vm_create(compute_client, nic_2, VM_NAMES_02)

    # Test Connection between VM01 & VM02
    cmd = 'ping {0} -c 2'.format(destination_ip)
    ping_test.ping_vms(compute_client, cmd)

    # close
    network_client.close()
    compute_client.close()
    resource_client.close()
