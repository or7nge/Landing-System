from dronekit import connect, VehicleMode
from time import sleep
import logging
import config
from pymavlink import mavutil

# Initialize logging for debugging
logging.basicConfig(level=logging.INFO)

def connect_to_drone():
    """
    Connects to the drone using the connection string from the config file.
    """
    connection_string = config.DRONE_CONNECTION_STRING
    if not connection_string:
        logging.error("No connection string provided in config, exiting...")
        return None
    
    logging.info(f"Connecting to vehicle on: {connection_string}")
    vehicle = connect(connection_string, wait_ready=True)
    
    if not vehicle:
        logging.error("Failed to connect to vehicle")
        return None
    
    logging.info("Connected to drone successfully")
    return vehicle

def ensure_vehicle_ready(vehicle):
    """
    Ensures the vehicle is in GUIDED mode and armed.
    """
    if not vehicle.is_armable:
        logging.warning("Vehicle is not armable yet. Waiting...")
        while not vehicle.is_armable:
            sleep(1)

    if vehicle.mode.name != "GUIDED":
        logging.info("Setting vehicle to GUIDED mode")
        vehicle.mode = VehicleMode("GUIDED")
        while vehicle.mode.name != "GUIDED":
            logging.info("Waiting for mode change to GUIDED...")
            sleep(1)

    if not vehicle.armed:
        logging.info("Arming the vehicle")
        vehicle.armed = True
        while not vehicle.armed:
            logging.info("Waiting for vehicle to arm...")
            sleep(1)
    
    logging.info("Vehicle is ready for commands")

def execute_directive(vehicle, directive):
    """
    Executes the command based on the directive passed.
    - vehicle: the connected drone object
    - directive: the Directive object containing the command and value
    """
    ensure_vehicle_ready(vehicle)

    if directive.command == "NO ARUKO":
        logging.info("No Aruko detected. Ascending to search.")
        ascend(vehicle, 2)  # Ascend 2 meters to search for the marker

    elif directive.command == "DESCEND":
        logging.info("Aruko detected in center. Descending.")
        descend(vehicle, 2)  # Descend 2 meters closer to the ground

    elif directive.command == "ROTATE":
        logging.info(f"Rotating {directive.value} degrees clockwise.")
        rotate(vehicle, directive.value)

    elif directive.command == "MOVE":
        logging.info(f"Moving {directive.value} cm forward.")
        move_forward(vehicle, directive.value / 100.0)  # Convert cm to meters

    elif directive.command == "LAND":
        logging.info("Landing the drone.")
        land(vehicle)

    else:
        logging.warning(f"Unknown directive: {directive.command}")

def ascend(vehicle, altitude_increase):
    """
    Ascends the drone by a given amount (in meters).
    """
    logging.info(f"Ascending {altitude_increase} meters.")
    current_alt = vehicle.location.global_relative_frame.alt
    target_alt = current_alt + altitude_increase
    vehicle.simple_takeoff(target_alt)

    while True:
        if vehicle.location.global_relative_frame.alt >= target_alt * 0.95:
            logging.info(f"Reached target altitude: {target_alt} meters")
            break
        sleep(1)

def descend(vehicle, altitude_decrease):
    """
    Descends the drone by a given amount (in meters).
    """
    logging.info(f"Descending {altitude_decrease} meters.")
    move(vehicle, 0, 0, altitude_decrease)

def rotate(vehicle, degrees):
    """
    Rotates the drone clockwise by a given number of degrees, relative to current heading.
    """
    if degrees < 0:
        logging.warning("Degrees must be positive for clockwise rotation.")
        return
    rotate_me(vehicle, degrees, 10, relative=True)

def move_forward(vehicle, distance):
    """
    Moves the drone forward by a given distance (in meters).
    """
    logging.info(f"Moving forward by {distance} meters.")
    move(vehicle, distance, 0, 0)

def land(vehicle):
    """
    Commands the drone to land.
    """
    logging.info("Landing the drone.")
    vehicle.mode = VehicleMode("LAND")
    while vehicle.armed:
        logging.info("Waiting for drone to land and disarm...")
        sleep(1)
    logging.info("Drone has landed and disarmed.")

def move(vehicle, x, y, z):
    """
    Moves the drone in the NED (North-East-Down) frame.
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0, 0, 0,
        mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED,
        0b0000111111000111,  # mask to enable control of x, y, z velocities
        x, y, z,  # x, y, z positions
        0, 0, 0,  # x, y, z velocities (unused here)
        0, 0, 0,  # accelerations (unused)
        0, 0  # yaw, yaw_rate
    )
    vehicle.send_mavlink(msg)
    vehicle.flush()

def rotate_me(vehicle, heading, speed, relative=True):
    """
    Rotates the drone by the specified heading relative to its current direction.
    """
    is_relative = 1 if relative else 0
    direction = 1 if heading < 180 else -1

    if heading >= 180:
        heading -= 180

    msg = vehicle.message_factory.command_long_encode(
        0, 0,
        mavutil.mavlink.MAV_CMD_CONDITION_YAW,
        0,
        heading,    # target heading
        speed,      # yaw speed (degrees per second)
        direction,  # direction (-1 = CCW, 1 = CW)
        is_relative, # relative = 1, absolute = 0
        0, 0, 0
    )
    vehicle.send_mavlink(msg)
    vehicle.flush()
