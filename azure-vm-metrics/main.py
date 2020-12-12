import datetime
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.monitor import MonitorManagementClient

SUBSCRIPTION_ID = '80910117-1122-4cca-8f31-6d743a491221'
CLIENT_ID = 'd9b617ca-acb1-44a5-9d9c-2cfb38b161db'
SECRET = '2a~MoL-0PTvnJDKrM1M-7.28Cm_9RP.HT3'
TENANT_ID = 'c6879db7-9cbe-40b9-9204-955880c4f342'

RESOURCE_GROUP_NAME = 'python-lab-automation'

VM_NAMES_01 = 'machine-01'
VM_NAMES_02 = 'machine-02'

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
    # for metric in metrics_client.metric_definitions.list(resource_id):
    #     print("{}: id={}, unit={}".format(
    #         metric.name.localized_value,
    #         metric.name.value,
    #         metric.unit
    #     ))
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
