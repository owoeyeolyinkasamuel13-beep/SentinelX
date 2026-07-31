from utils.banner import display_banner
from core.registry import ModuleRegistry
from modules.network.port_scanner import PortScanner


class Application:

    def __init__(self):
        self.registry = ModuleRegistry()
        self.registry.register(PortScanner())

    def start(self):

        display_banner()

        while True:

            print("\nRegistered Modules\n")

            modules = self.registry.get_modules()

            for index, module in enumerate(modules, start=1):
                print(f"{index}. {module.name}")

            print("0. Exit")

            choice = input("\nSelect an option: ")

            if choice == "0":
                print("\nThank you for using SentinelX.")
                break

            if choice.isdigit():

                module = self.registry.get_module(int(choice))

                if module:
                    module.run()
                else:
                    print("\nInvalid option.")

            else:
                print("\nPlease enter a valid number.")