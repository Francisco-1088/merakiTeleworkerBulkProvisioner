# merakiTeleworkerBulkProvisioner

Alternative to the bulk network creation tool, focused on Teleworker deployments with MXs and Zs.

![image alt text](images/diagram.png)

# Table of Contents

[Introduction](#intro)

[Prerequisites](#prereq)

[How to use](#howtouse)

[Caveats](#caveats)

<a id="intro"></a>

# Introduction

Cisco Meraki Configuration Templates and Switch Profiles allow organizations to manage large numbers of switches distributed across many locations in a simplified manner, centralizing configurations in one point. However, they also introduce a number of limitations:
1. All sites bound to the template must conform to a single firmware version, and must be upgraded together
2. It removes the option of using Staged Upgrades, forcing all upgrades within a site to happen concurrently
3. It forces all template-bound networks to conform not only to the same Switch Profiles, but also to the same Group Policies, QoS settings, ACL rules and other network-wide settings
4. It limits local divergences in switch port configurations, as any changes to the switch profiles will be pushed out to all bound switches

This tool allows decoupling of firmware upgrades and network settings from switch port configurations, and offers additional flexibility in deploying port configuration changes, like defining ports to be ignored during configuration pushes, and only pushing changes to a subset of your switches. All of this is achieved via Tags:

* **Network Tags** identify networks the tool will operate on and copy Network-wide configurations to (Group Policies, QoS, ACLs, Alerts, Syslog, SNMP, Traffic Analytics)
* **Switch Tags** identify switches within these networks that will have their ports synced to profiles that carry the same name as the tag (including associated Access Policies and Port Schedules)
* **Ignore Port Tags** identify ports that should not be updated by the script, even if the script is operating on other ports in the same switch. This allows preservation of local overrides and protecting critical ports like uplinks and server ports

The script also has the added flexibility of allowing you to reference a configuration template as a source that resides in a different organization than the one where your switches currently exist on, permitting syncing configurations across organizations. It also allows the definition of a template for switch port profiles, and a separate different template for Network settings, decoupling port-level configurations from ACLs, QoS, Alerting and other settings for added flexibility.

All of this is done without ever binding switches to configuration templates, which allows you to keep completely separate firmware upgrade procedures across networks, and keeping advanced functionalities like Staged Upgrades available.

<a id="prereq"></a>

## Prerequisites

1. Active Cisco Meraki subscriptions in the orgs where the script will be run
2. API access enabled for these organizations, as well as an API Key with access to them. See how to enable [here](https://documentation.meraki.com/General_Administration/Other_Topics/Cisco_Meraki_Dashboard_API)
3. A working Python 3.0 environment
4. Install libraries in `requirements.txt`
5. Create a configuration template for housing your configurations, and optionally a second configuration template if you wish to decouple Group Policies, QoS, ACL, Alert, Syslog, SNMP configurations from the switch profiles template.
6. Set up switch port profiles for each of the types of switches you will deploy in your environment in the source template. You can see how to configure port profiles [here](https://documentation.meraki.com/Architectures_and_Best_Practices/Cisco_Meraki_Best_Practice_Design/Best_Practice_Design_-_MS_Switching/Templates_for_Switching_Best_Practices#Switch_Profiles)
7. Set up [Group Policies](https://documentation.meraki.com/MS/Access_Control/Meraki_MS_Group_Policy_Access_Control_Lists), [QoS](https://documentation.meraki.com/MS/Other_Topics/QoS_(Quality_of_Service)), [ACLs](https://documentation.meraki.com/MS/Layer_3_Switching/Configuring_ACLs), [Alerts](https://documentation.meraki.com/General_Administration/Cross-Platform_Content/Alerts_and_Notifications), [SNMP](https://documentation.meraki.com/General_Administration/Monitoring_and_Reporting/SNMP_Overview_and_Configuration), [Syslog](https://documentation.meraki.com/General_Administration/Monitoring_and_Reporting/Syslog_Server_Overview_and_Configuration), [Access Policies](https://documentation.meraki.com/MS/Access_Control/MS_Switch_Access_Policies_(802.1X)) and [Port Schedules](https://documentation.meraki.com/MS/Access_Control/Port_Schedules) in source templates.
8. Deploy additional standalone networks with switches in them

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
