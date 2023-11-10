if __name__ == '__main__':
    from multiprocessing import freeze_support
    from interface_layer.application import Application

    freeze_support()
    Application()()  # masslaw content processing :)
