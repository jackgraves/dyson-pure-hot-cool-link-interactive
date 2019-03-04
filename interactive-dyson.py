# Bypass SSL Warning
import requests
import getpass
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Import Dyson Modules
from libpurecoollink.dyson import DysonAccount
from libpurecoollink.const import FanSpeed, FanMode, NightMode, Oscillation, \
    FanState, StandbyMonitoring, QualityTarget, ResetFilter, HeatMode, \
    FocusMode, HeatTarget

# Get Username and Password Inputs using Interactive Input:
dyson_username = input("Enter Dyson Account Username: ")
dyson_password = getpass.getpass("Enter Dyson Account Password: ")

# Override with static values if you want:
# dyson_username = "username@domain.com"
# dyson_password = "my_cool_password"

# Log to Dyson account
dyson_account = DysonAccount(dyson_username, dyson_password, "GB")
logged = dyson_account.login()

# If Error, Stop
if not logged:
    print('Unable to login to Dyson account. Exiting.')
    exit(1)

# Connect to Dyson Fan (first and only device assumed)
devices = dyson_account.devices()
connected = devices[0].auto_connect()

# Chat Loop
while(True):
    # Commands are help, status, on, off, oscillate, night, speed, sleep or heat
    command = input("Enter a Command (try help): ")
    if(command == "help"):
        print("Available Commands: ")
        print(" - on")
        print(" - off")
        print(" - status")
        print(" - speed 1-10")
        print(" - 'heat 15-30'C")
        print(" -'oscillate on/off")
        print(" - 'sleep 0-60' minutes")
    elif(command == "status"):
        print("Fan Mode:    " + devices[0].state.fan_mode);
        print("Speed:       " + devices[0].state.speed)
        print("Oscillation: " + devices[0].state.oscillation)
        print("Tilt:        " + devices[0].state.tilt)
        print("Heat Mode:   " + devices[0].state.heat_mode)
        print("Heat State:  " + devices[0].state.heat_state)
        print("Heat Target: " + devices[0].state.heat_target)
    elif(command == "on"):
        print("Turning Dyson On")
        devices[0].set_configuration(fan_mode=FanMode.FAN)
    elif(command == "off"):
        print("Turning Dyson Off")
        devices[0].set_configuration(fan_mode=FanMode.OFF)
    elif("oscillate" in command):
        if(command[-1] == "n"):
            devices[0].set_configuration(oscillation=Oscillation.OSCILLATION_ON)
        elif(command[-1] == "f"):
            devices[0].set_configuration(oscillation=Oscillation.OSCILLATION_OFF)
    elif("night" in command):
        if(command[-1] == "n"):
            devices[0].set_configuration(night_mode=NightMode.NIGHT_MODE_ON)
        elif(command[-1] == "f"):
            devices[0].set_configuration(night_mode=NightMode.NIGHT_MODE_OFF)
    else:
        # At this point, we're dealing with parameters with numbers (speed, heat and sleep)
        if("speed" in command):
            parameter = command.split()[-1]
            print("Setting Speed to " + parameter)
            devices[0].set_configuration(fan_speed=FanSpeed["FAN_SPEED_" + parameter])
        elif("heat" in command):
            parameter = command.split()[-1]
            print("Setting Heat to " + parameter + "C")
            devices[0].set_configuration(heat_target=HeatTarget.celsius(parameter))
        elif("sleep" in command):
            parameter = int(command.split()[-1])
            print("Sleeping in " + parameter + " minutes")
            devices[0].set_configuration(sleep_timer=parameter)
