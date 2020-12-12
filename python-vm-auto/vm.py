import traceback

from msrestazure.azure_exceptions import CloudError
from conf_file_yaml import cfg_azure_common as common
from conf_file_yaml import cfg_azure_vm as vm

RESOURCE_GROUP_NAME = common()["RESOURCE_GROUP_NAME"]
LOCATION = common()["LOCATION"]

USERNAME = vm()["USERNAME"]
PASSWORD = vm()["PASSWORD"]
VM_REFERENCE = vm()["VM_REFERENCE"]


def create_vm_parameters(nic_id, vm_reference):
    return {
        'location': LOCATION,
        'os_profile': {
            'computer_name': "python-lab-auto02",
            'admin_username': USERNAME,
            "linuxConfiguration": {
                "disablePasswordAuthentication": "true",
                "ssh": {
                    "publicKeys": [
                        {
                            "path": "/home/{}/.ssh/authorized_keys".format(USERNAME),
                            "keyData": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDEK+GpskSS/gCxmtRX7Be6+JQ9\r\nMnbkt0i0f93ZRUVMF0J4iW+Ic+ZAks0aZicigzmnL9Bbei4VPj27lL5jaIYCdg5d\r\nz96Lw3Dn6plu0XdEilzuWAgycqEf+cTVu1HT9ahpOzGJtp4dOoDHb//Ra5v1XxOA\r\nV8hoYI0+tOuS2GxCcTbuRj3esQZE3wev7d4y6oQ88zYz0/enCLgLlYRc744S6FCF\r\nWbKFKYnRHeY7BzRoEIOKJ2tR4Vd6BpFLe6fMGcth9IlUeOiSSOvsxK/GYqOg/3LQ\r\nhB8141NpmPsQEyfg4/w8SVf4I8Ja5OQ5lHDBC8dZlcpENuuFCfKyBoAdLomHRsRq\r\npmADHwRwfGfKnd4JwYFLPcQm9vgJVFPsp3g9ZFnbhspwc5KWkEm/xkmC/aAu6SrI\r\nCfRz0SxHx9NNUyx9pQekL0bQZ3iVb1Oi26BwjtlNuSQJXKTmgwbo2LjJQJu9c6Ps\r\ncxtccFdftNKhiHBUAUYLznq46hxi95e44OkBTos= generated-by-azure\r\n"
                        }
                    ]
                },
            }
        },
        'hardware_profile': {
            'vm_size': 'Standard_DS1_v2'
        },
        'storage_profile': {
            'image_reference': {
                'publisher': vm_reference['publisher'],
                'offer': vm_reference['offer'],
                'sku': vm_reference['sku'],
                'version': vm_reference['version']
            },
        },
        'network_profile': {
            'network_interfaces': [{
                'id': nic_id,
            }]
        },
    }


def vm_create(cl, nic, vm_name):
    try:
        vm_parameters = create_vm_parameters(nic.id, VM_REFERENCE)
        machine = cl.virtual_machines.create_or_update(RESOURCE_GROUP_NAME, vm_name, vm_parameters).result()
    except CloudError:
        print('VIRTUAL-MACHINE: operation failed:\n{}'.format(traceback.format_exc()))
        return False
    else:
        print('VIRTUAL-MACHINE: completed successfully!')
        return machine
