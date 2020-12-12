import traceback
from msrestazure.azure_exceptions import CloudError
from azure.mgmt.network import NetworkManagementClient
from azure.common.credentials import ServicePrincipalCredentials
from conf_file_yaml import cfg_azure_common as common
from conf_file_yaml import cfg_azure_network as nic

VNET_NAME = nic()["VNET_NAME"]
SUBNET_NAME = nic()["SUBNET_NAME"]
IP_NAME = nic()["IP_NAME"]
NIC_NAME = nic()["NIC_NAME"]
PUBLIC_IP_NAME = nic()["PUBLIC_IP_NAME"]

RESOURCE_GROUP_NAME = common()["RESOURCE_GROUP_NAME"]
LOCATION = common()["LOCATION"]


def net_client(cred: ServicePrincipalCredentials, sub: str):
    return NetworkManagementClient(cred, sub)


def create_vnet(net: NetworkManagementClient):
    if net.virtual_networks.get(RESOURCE_GROUP_NAME, VNET_NAME) != '':
        print('aze')
    else:
        print('aze')
    try:
        vnet = net.virtual_networks.create_or_update(
            RESOURCE_GROUP_NAME,
            VNET_NAME,
            {
                'location': LOCATION,
                'address_space': {
                    'address_prefixes': ['10.0.0.0/16']
                }
            }
        ).result()
    except CloudError:
        print('VNET: operation failed:\n{}'.format(traceback.format_exc()))
        return False
    else:
        print('VNET: completed successfully!')
        return vnet


def create_subnet(net: NetworkManagementClient):
    try:
        subnet = net.subnets.create_or_update(
            RESOURCE_GROUP_NAME,
            VNET_NAME,
            SUBNET_NAME,
            {
                'address_prefix': '10.0.0.0/24',
                'delegations': [],
                'private_endpoint_network_policies': 'Enabled',
                'private_link_service_network_policies': 'Enabled'
            }
        ).result()
    except CloudError:
        print('SUBNET: operation failed:\n{}'.format(traceback.format_exc()))
        return False
    else:
        print('SUBNET: completed successfully!')
        return subnet


def create_public_ip(net: NetworkManagementClient):
    try:
        params = {
            'location': LOCATION,
            'sku': {
                'name': 'Basic'
            },
            'public_ip_address_version': 'IPv4',
            'public_ip_allocation_method': 'Dynamic',
            'idle_timeout_in_minutes': 15
        }
        public_ip = net.public_ip_addresses.create_or_update(
            RESOURCE_GROUP_NAME,
            PUBLIC_IP_NAME,
            params
        ).result()
    except CloudError:
        print('PUBLIC_IP: operation failed:\n{}'.format(traceback.format_exc()))
        return False
    else:
        print('PUBLIC_IP: completed successfully!')
        return public_ip


def create_interface(net: NetworkManagementClient, subnet):
    public_ip = net.public_ip_addresses.get(
        RESOURCE_GROUP_NAME,
        PUBLIC_IP_NAME
    )
    try:
        nic_driver_1 = net.network_interfaces.create_or_update(
            RESOURCE_GROUP_NAME,
            NIC_NAME + '_1',
            {
                'location': LOCATION,
                'ip_configurations': [{
                    'name': IP_NAME + '_1',
                    'public_id_address': public_ip,
                    'subnet': {
                        'id': subnet.id
                    }
                }]
            }
        ).result()
        nic_driver_2 = net.network_interfaces.create_or_update(
            RESOURCE_GROUP_NAME,
            NIC_NAME + '_2',
            {
                'location': LOCATION,
                'ip_configurations': [{
                    'name': IP_NAME + '_2',
                    'subnet': {
                        'id': subnet.id
                    }
                }]
            }
        ).result()
    except CloudError:
        print('INTERFACE: operation failed:\n{}'.format(traceback.format_exc()))
        return False
    else:
        print('INTERFACE: completed successfully!')
        return nic_driver_1, nic_driver_2


def get_private(network_client: NetworkManagementClient):
    try:
        ips = network_client.network_interfaces.get(RESOURCE_GROUP_NAME, NIC_NAME + '_2').ip_configurations
        for ip in ips:
            return ip.private_ip_address
    except:
        False