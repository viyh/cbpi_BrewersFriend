from modules import cbpi
import requests

def get_param(param_name, default_value, param_type, param_desc):
    value = cbpi.get_config_parameter(param_name, None)
    if value is None:
        cbpi.add_config_parameter(param_name, default_value, param_type, param_desc)
        return default_value
    return value

def get_config():
    config = {}
    config['api_url'] = get_param("brewersfriend_api_url", "https://log.brewersfriend.com/stream/", "text", "BrewersFriend API URL Prefix")
    config['api_key'] = get_param("brewersfriend_api_key", "", "text", "BrewersFriend API Key")
    config['temp_sensor'] = get_param("brewersfriend_temp_sensor", "", "sensor", "BrewersFriend temperature sensor, i.e. 'sensor'")
    config['temp_unit'] = get_param("brewersfriend_temp_unit", "C", "text", "BrewersFriend temperature unit (C or F for Celsius or Fahrenheit)")
    config['gravity_sensor'] = get_param("brewersfriend_gravity_sensor", "", "sensor", "BrewersFriend gravity sensor, i.e. 'sensor2'")
    config['gravity_unit'] = get_param("brewersfriend_gravity_unit", "G", "text", "BrewersFriend gravity unit (G or P for Gravity or Plato)")
    return config

def log(s):
    print(s)
    cbpi.app.logger.info(s)
    # cbpi.notify("bf_task", s, type="danger", timeout=None)

def bf_submit(api_url, api_key, data):
    response = requests.post(api_url + api_key, json=data)
    if response.status_code == 200:
        log("Submitted data: " + str(data))
        return True
    else:
        log("Received unsuccessful response. Ensure API key is correct. HTTP Error Code: " + str(response.status_code))
        return False

def get_fermenter_sensors_data(fermenter, temp_sensor, temp_unit, gravity_sensor, gravity_unit):
    data = {"name": fermenter.name}
    gravity = get_sensor_value(fermenter, gravity_sensor)
    temp = get_sensor_value(fermenter, temp_sensor)
    if gravity:
        data['gravity'] = gravity
        data['gravity_unit'] = gravity_unit
    if temp:
        data['temp'] = temp
        data['temp_unit'] = temp_unit
    return data

def get_sensor_value(fermenter, sensor):
    if sensor != "":
        return cbpi.get_sensor_value(int(getattr(fermenter, sensor)))
    else:
        return False

@cbpi.backgroundtask(key="bf_task", interval=900)
def bf_background_task(api):
    log("Brewer's Friend START")
    config = get_config()

    if config['api_key'] == "":
        log("API key not set. Update brewersfriend_api_key parameter within System > Parameters.")
        return
    if config['gravity_sensor'] == "" and config['temp_sensor'] == "":
        log("No temperature or gravity sensors are set in the parameters.")
        return

    log("Finding fermenter sensors...")
    for i, fermenter in cbpi.cache.get("fermenter").iteritems():
        log("Fermenter: " + str(i) + ": " + fermenter.name + ", State: " + str(fermenter.state))
        if fermenter.state is not True:
            continue
        try:
            data = get_fermenter_sensors_data(
                fermenter,
                config['temp_sensor'],
                config['temp_unit'],
                config['gravity_sensor'],
                config['gravity_unit']
            )
            bf_submit(config['api_url'], config['api_key'], data)
        except Exception as e:
            log("Unable to send message: " + str(e))
            pass
