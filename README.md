# Brewer's Friend (brewersfriend.com) stream plugin for CraftBeerPi3

Use this plugin to send your fermenation temperatures and gravities to Brewer's Friend

## Installation

Download and Install this Plugin via the CraftBeerPi user interface
or pull into the [craftbeerpi]/modules/plugins/ directory

Set the following parameters in CraftBeerPi3:
* brewersfriend_api_key: The api key from https://www.brewersfriend.com/homebrew/profile/account#integrations
* brewersfriend_temp_sensor: The name of the Temperature sensor for all fermenters being submitted to Brewer's Friend. This is one of "sensor", "sensor2", or "sensor3", and must be consistent on all fermenters. Leave empty if no temperature sensor.
* brewersfriend_gravity_sensor: The name of the Gravity sensor for all fermenters being submitted to Brewer's Friend. This is one of "sensor", "sensor2", or "sensor3", and must be consistent on all fermenters. Leave empty if no gravity sensor.

Additional parameters (default values are fine most of the time):
* brewersfriend_api_url: API URL, default: https://log.brewersfriend.com/stream/
* brewersfriend_temp_unit: Temperature unit of sensor (C or F for Celsius or Fahrenheit) default: C
* brewersfriend_gravity_unit: Gravity unit of sensor (G or P for Gravity or Plato), default: G

## Updates

Temperatures will update every 15 minutes to Brewer's Friend for all fermenters that are set to automatic.

You can view the logs and attach to a brew session under the Fermentation tab in your brew session within Brewer's Friend
