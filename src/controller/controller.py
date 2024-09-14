def start_controller_loop(queue):
    current_directive =
    while True:
        while not queue.empty():
            current_directive = queue.get()
    return
