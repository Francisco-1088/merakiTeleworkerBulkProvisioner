import meraki
import pandas as pd
from datetime import datetime
import config

dashboard = meraki.DashboardAPI(api_key=config.api_key)

df = pd.read_csv('to_create.csv')

to_create = df.to_dict('records')

templates = dashboard.organizations.getOrganizationConfigTemplates(organizationId=config.org_id)

error_list = []

for user in to_create:
    errors = {}
    errors['net_name']=user['net_name']
    try:
        network = dashboard.organizations.createOrganizationNetwork(organizationId=config.org_id, name=user['net_name'], productTypes=['appliance'])
    except meraki.APIError as e1:
        network = {'id':''}
        errors['e1']=e1
    try:
        claim = dashboard.networks.claimNetworkDevices(networkId=network['id'], serials=[user['serial']])
    except meraki.APIError as e2:
        errors['e2']=e2
    for temp in templates:
        if temp['name']==user['template_name']:
            try:
                bind = dashboard.networks.bindNetwork(networkId=network['id'], configTemplateId=temp['id'])
            except meraki.APIError as e3:
                errors['e3']=e3

    error_list.append(errors)

errors_df = pd.DataFrame.from_dict(error_list)

errors_df.to_csv(f'errors_{datetime.now()}.csv')



