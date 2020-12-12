import datetime
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.monitor import MonitorManagementClient
from conf_file_yaml import cfg_azure_common as common
from conf_file_yaml import cfg_azure_vm as vm


SUBSCRIPTION_ID = common()["SUBSCRIPTION_ID"]
CLIENT_ID = common()["CLIENT_ID"]
SECRET = common()["SECRET"]
TENANT_ID = common()["TENANT_ID"]
RESOURCE_GROUP_NAME = common()["RESOURCE_GROUP_NAME"]

VM_NAMES_01 = vm()["VM_NAMES_01"]
VM_NAMES_02 = vm()["VM_NAMES_02"]

resource_id = (
    "subscriptions/{}/"
    "resourceGroups/{}/"
    "providers/Microsoft.Compute/virtualMachines/{}"
).format(SUBSCRIPTION_ID, RESOURCE_GROUP_NAME, VM_NAMES_02)

credentials = ServicePrincipalCredentials(client_id=CLIENT_ID, secret=SECRET, tenant=TENANT_ID)

metrics_client = MonitorManagementClient(
    credentials,
    SUBSCRIPTION_ID
)

today = datetime.datetime.now().date()
tomorrow = today + datetime.timedelta(days=1)


if __name__ == '__main__':
    metrics_data_cpu = metrics_client.metrics.list(
        resource_id,
        timespan="{}/{}".format(today, tomorrow),
        interval='PT1H',
        metricnames='Percentage CPU',
        aggregation='Total'
    )

    metrics_data_hard_drive = metrics_client.metrics.list(
        resource_id,
        timespan="{}/{}".format(today, tomorrow),
        interval='PT1H',
        metricnames='OS Disk IOPS Consumed Percentage',
        aggregation='Total'
    )

    metrics_data_network_in = metrics_client.metrics.list(
        resource_id,
        timespan="{}/{}".format(today, tomorrow),
        interval='PT1H',
        metricnames='Network In Total',
        aggregation='Total'
    )

    metrics_data_network_out = metrics_client.metrics.list(
        resource_id,
        timespan="{}/{}".format(today, tomorrow),
        interval='PT1H',
        metricnames='Network Out Total',
        aggregation='Total'
    )

    print("\n--------------------------------------------------------\n")
    for cpu_item in metrics_data_cpu.value:
        print("{} ({})".format(cpu_item.name.localized_value, cpu_item.unit.name))
        for cpu_timeserie in cpu_item.timeseries:
            for cpu_data in cpu_timeserie.data:
                print("{}: {}".format(cpu_data.time_stamp, cpu_data.total))
    print("\n--------------------------------------------------------\n")
    for hdd_item in metrics_data_hard_drive.value:
        print("{} ({})".format(hdd_item.name.localized_value, hdd_item.unit.name))
        for hdd_timeserie in hdd_item.timeseries:
            for hdd_data in hdd_timeserie.data:
                print("{}: {}".format(hdd_data.time_stamp, hdd_data.total))
    print("\n---------------------------------------------------------\n")
    for net_in_item in metrics_data_network_in.value:
        print("{} ({})".format(net_in_item.name.localized_value, net_in_item.unit.name))
        for net_in_timeserie in net_in_item.timeseries:
            for net_in_data in net_in_timeserie.data:
                print("{}: {}".format(net_in_data.time_stamp, net_in_data.total))
    print("\n--------------------------------------------------------\n")
    for net_out_item in metrics_data_network_out.value:
        print("{} ({})".format(net_out_item.name.localized_value, net_out_item.unit.name))
        for net_out_timeserie in net_out_item.timeseries:
            for net_out_data in net_out_timeserie.data:
                print("{}: {}".format(net_out_data.time_stamp, net_out_data.total))

    metrics_client.close()
