import os
import sys
import csv
import art
from dotenv import load_dotenv
from tabulate import tabulate
from passnager_modules.PassCrypt import pass_encrypt, pass_decrypt

class Passnager:
    def __init__(self, file_name: str="data.csv"):
        self.__data = []
        self.__file_name = file_name
        # Open file
        while True:
            try:
                with open(self.__file_name, "r") as f:
                    for row in csv.reader(f):
                        self.__data.append(row)
                    break
            except FileNotFoundError:
                print(f"Create {self.__file_name} file")
                headers: list = ["no", "username_or_email", "password"]
                with open("./data.csv", "w") as f:
                    writer = csv.DictWriter(f, fieldnames=headers)
                    writer.writeheader()
                    # writer.writerows(dummy)
                continue

    def show_data(self, table_fmt="fancy_grid") -> tabulate:
        try:
            if not self.__data:
                return "0 Data Found"
            
            print(len(self.__data[1:]), "data found")
            return tabulate(self.__data[1:], headers=self.__data[0], tablefmt=table_fmt)
        except:
            return "Something went wrong while trying to read a csv file"

    def __add_list_data(self) -> tuple:
        if len(self.__data) > 1:
            no = int(self.__data[-1][0]) + 1
        else:
            no = 1
        username = input("\nUsername/email\t: ")
        password = input("Password\t: ")
        return (no, username, password)

    def add_data(self) -> None:
        try:
            new_data = self.__add_list_data()
            if len(self.__data) > 1:
                list_username = [x[1] for x in self.__data[1:]]
            else:
                list_username = []

            with open(self.__file_name, "a") as f:
                # Abort when the username is already exists
                if new_data[1] in list_username:
                    print("\nData already exists!!!\n")
                else:
                    writer = csv.writer(f)
                    writer.writerow(new_data)
                    self.__data.append(new_data)
                    print("++ Successfully adding data\n")

        except Exception as e:
            sys.exit(e)

    def update_data(self):
        ...

    def delete_data(self):
        ...

def get_dotenv() -> dict:
    # load .env
    load_dotenv(dotenv_path="./.env")
    
    envs = {}
    try:
        envs["app_name"] = os.environ["APP_NAME"]
        envs["secret_key"] = os.environ["SECRET_KEY"]
    except Exception as e:
        sys.exit(e)
    return envs

def clear_screen():
    if os.name == "nt":
        os.system("cls") 
    else:
        os.system("clear")

def back_to_menu():
    while True:
        if input("0 for back\t: ") == "0":
            clear_screen()
        break
    
def main():
    clear_screen()
    pm = Passnager()
    print("""
====================================
      | WELCOME TO PASSNAGER | 
++==+++==+++==+++==+++==+++==+++==++
    [1] show data
    [2] add data       
    [0] Exit       
====================================""")

    display = """
====================================         
         |   PASSNAGER   |
++==+++==+++==+++==+++==+++==+++==++
    [1] show data
    [2] add data       
    [0] Exit       
===================================="""

    while True:
        choice = input("[*] Menu Choice: ")
        print()
        match choice:
            case "1":
                print(pm.show_data())
                back_to_menu()
            case "2":
                pm.add_data()
                back_to_menu()
            case "0":
                clear_screen()
                print(art.text2art('SEE YOU LATER', font='rand'))
                input("Press anything")
                sys.exit()
            case _:
                print("Invalid Input!!!\n")
                continue

        print(display)

if __name__ == "__main__":
    main()