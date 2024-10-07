from drone_commands import execute_directive, connect_to_drone


def start_controller_loop(queue):
    return  # Currently disabled to text the detection system

    vehicle = connect_to_drone()  # Connect to the drone when starting the controller loop
    current_directive = None
    while True:
        while not queue.empty():
            current_directive = queue.get()  # Get the latest directive from the queue
            execute_directive(vehicle, current_directive)  # Execute the command based on the directive
    return
