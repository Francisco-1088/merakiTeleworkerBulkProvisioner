# merakiTeleworkerBulkProvisioner

Alternative to the bulk network creation tool, focused on Teleworker deployments with MXs and Zs.

# Table of Contents

[Prerequisites](#prereq)

[How to use](#howtouse)


<a id="prereq"></a>

## Prerequisites

1. Active Cisco Meraki subscriptions in the orgs where the script will be run
2. API access enabled for these organizations, as well as an API Key with access to them. See how to enable [here](https://documentation.meraki.com/General_Administration/Other_Topics/Cisco_Meraki_Dashboard_API)
3. A working Python 3.0 environment

<a id="howtouse"></a>

## How to Use

1. Clone repo to your working directory with `git clone https://github.com/Francisco-1088/merakiSwitchProfiler.git`
2. Edit `config.py`
* Add your API Key under `api_key` in line 2
* Add the Organization ID of the organization where the source configuration template exists. You can find your Org ID easily by right clicking anywhere in the screen while logged in to your organization, and clicking "View Page Source". In the resulting page use "Find" to look for the keyword `Mkiconf.org_id`
3. Populate the sample `to_create.csv` file with the list of devices and networks to provision, as well as the configuration templates they will be bound to. Configuration template name MUST match exactly with whatever you add to the file.
4. Run `pip install -r requirements.txt` from your terminal
5. Run `python main.py`
6. Check the output `errors.csv` file to verify that your networks created successfully. Common errors you will find are serial numbers that have already been claimed, mismatched Template network names and existing Network Names.
7. `bulkChecker.py` together with `check.csv` can help verify if any Serial numbers have previously been claimed.
8. `claimer.py` helps claim any serial numbers into your inventory, as they must be there BEFORE you may use `main.py`.
