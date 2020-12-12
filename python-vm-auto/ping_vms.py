from azure.mgmt.compute import ComputeManagementClient

from conf_file_yaml import cfg_azure_common as common
from conf_file_yaml import cfg_azure_vm as vm

RESOURCE_GROUP_NAME = common()["RESOURCE_GROUP_NAME"]
VM_NAMES_01 = vm()["VM_NAMES_01"]


def ping_vms(compute: ComputeManagementClient, cmd: str):
    run_command = {
        'command_id': 'RunShellScript',
        'script': [
            '{}'.format(cmd)
        ]
    }
    poller = compute.virtual_machines.run_command(
        RESOURCE_GROUP_NAME,
        VM_NAMES_01,
        run_command
    )
    result = poller.result()
    print("\n---- Ping to VM01 ==> VM02 ----\n")
    print(result.value[0].message)
