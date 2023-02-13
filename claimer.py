import meraki
import pandas as pd
from datetime import datetime
import config

dashboard = meraki.DashboardAPI(api_key=config.api_key)

df = pd.read_csv('to_create.csv')

serial_list = df['Serial'].tolist()

dashboard.organizations.claimIntoOrganizationInventory(config.org_id, serials=serial_list)