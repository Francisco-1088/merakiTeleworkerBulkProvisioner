import meraki
import pandas as pd
from datetime import datetime
import config

dashboard = meraki.DashboardAPI(api_key=config.api_key)

df = pd.read_csv('check.csv')

to_check = df.to_dict('records')

not_created = []

for serial in to_check:
    try:
        device = dashboard.devices.getDevice(serial['Serial'])
        if device['networkId']=='':
            print(device)
    except meraki.APIError as e:
        print(e)
        print(serial['Serial'])
        not_created.append(serial)

to_create = pd.DataFrame.from_dict(not_created)
to_create.to_csv('./to_create.csv')