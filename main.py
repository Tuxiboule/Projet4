from controller.appmanager import MainController


def main():

    # initialise main controller
    main_controller = MainController()
    while True:
        print("test")
        main_controller.run()


if __name__ == "__main__":
    main()
