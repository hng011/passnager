import os
import sys
import csv
import art
from random import randint
from dotenv import load_dotenv
from tabulate import tabulate
from passnager_modules.PassCrypt import pass_encrypt, pass_decrypt, generate_secret_key

# load .env
load_dotenv(dotenv_path="./.env")

class Passnager:
    def __init__(self, secret_key, file_name="data.csv"):
        self.__data = []
        self.__file_name = file_name
        self.__secret_key = secret_key
        # Open file
        while True:
            try:
                with open(self.__file_name, "r") as f:
                    for row in csv.reader(f):
                        self.__data.append(row)
                    break
            except FileNotFoundError:
                print(f"Create {self.__file_name} file")
                headers: list = ["id", "app", "username_or_email", "password"]
                with open("./data.csv", "w") as f:
                    writer = csv.DictWriter(f, fieldnames=headers)
                    writer.writeheader()
                continue

    def __encrypt_pass(self, plain_pwd=None):
        return pass_encrypt(plain_pwd, self.__secret_key)

    def __decrypt_pass(self, encrypted_pwd=None):
        return pass_decrypt(encrypted_pwd, self.__secret_key)

    def show_data(self, table_fmt="fancy_grid") -> tabulate:
        try:            
            print(len(self.__data[1:]), "data found")
            decrypted_data = []
            for x in self.__data[1:]:
                decrypted_data.append([x[0], x[1], x[2], self.__decrypt_pass(x[3])])

            return tabulate(decrypted_data, headers=self.__data[0], tablefmt=table_fmt)
        except:
            return "Something went wrong while trying to read a csv file"

    def __generate_id(val_len=4) -> str:
        id = ""
        while True:
            if len(id) == 4:
                break
            id += str(randint(0,9))
        return id

    def __add_list_data(self) -> tuple:
        if len(self.__data) > 1:
            list_id = [x[0] for x in self.__data[1:]]
            while True:
                id = self.__generate_id()
                if id not in list_id: 
                    break
        else:
            id = self.__generate_id()

        while True:
            app = input("\nApp\t\t: ")
            username = input("Username/email\t: ")
            password = input("Password\t: ")

            encr_password = self.__encrypt_pass(password)

            if app and username and encr_password:
                return (id, app, username, encr_password)
            else:
                print("Each field required!!!")


    def add_data(self) -> None:
        try:
            new_data = self.__add_list_data()
            if len(self.__data) > 1:
                list_app = [x[1] for x in self.__data[1:]]
                list_username = [x[2] for x in self.__data[1:]]
            else:
                list_app = []
                list_username = []

            with open(self.__file_name, "a") as f:
                # Abort when the username is already exists
                if (
                    new_data[1] in list_app and
                    new_data[2] in list_username
                ):
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

def generate_key():
    key = generate_secret_key()

    try:
        with open(".env", "w") as f:
            f.write(f"SECRET_KEY={key}")
    except Exception as e:
        sys.exit(e)

    sys.exit("Succesfully generating a secret key")

def get_dotenv() -> dict:
    if os.environ["SECRET_KEY"] == "":
        sys.exit("KEY NOT FOUND: Run python project.py --generate-key")

    envs = {}
    try:
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
        if not(input("0 for back\t: ") == "0"): continue    
        break

    clear_screen()
    
def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--generate-key" and os.environ["SECRET_KEY"] == "":
        generate_key()

    envs = get_dotenv()
    pm = Passnager(secret_key=envs["secret_key"])

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
        try:
            choice = input("[*] Menu Choice: ")
        except EOFError:
            choice = "0"
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
                input("Press anything")
                clear_screen()
                continue

        print(display)

if __name__ == "__main__":
    main()