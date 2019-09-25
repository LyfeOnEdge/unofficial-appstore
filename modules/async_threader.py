import threading

class asyncThreader():
    def __init__(self):
        pass

    def do_async(self, func, arglist):
        vanillaThread(func, arglist)

    def async_button_place(self, button_build_function, button, base_x, base_y):
       buttonPlaceThread(button_build_function, button, base_x, base_y)

    def install_package(self, repo, appstore_handler_object, progress_function, reload_function):
        installThread(self.queue, repo, appstore_handler_object, progress_function, reload_function)

class installThread():
    def __init__(self, repo, appstore_handler_object, progress_function, reload_function):
        thread = threading.Thread(target=appstore_handler_object.install_package, args=(self.repo, progress_function, reload_function))
        thread.start()

class buttonPlaceThread():
    def __init__(self, button_build_function, button, base_x, base_y):
        thread = threading.Thread(target=button_build_function, args=(button, base_x, base_y))
        thread.start()

class vanillaThread():
    def __init__(self, func, arglist):
        thread = threading.Thread(target=func, args=arglist)
        thread.start()