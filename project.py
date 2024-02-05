import os
import sys
import csv
import pyfiglet
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
                header: list = ["id", "app", "username_or_email", "password"]
                with open(self.__file_name, "w") as f:
                    writer = csv.DictWriter(f, fieldnames=header)
                    writer.writeheader()
                continue

    def encrypt_pass(self, plain_pwd=None):
        return pass_encrypt(plain_pwd, self.__secret_key)

    def decrypt_pass(self, encrypted_pwd=None):
        return pass_decrypt(encrypted_pwd, self.__secret_key)

    def sort_data(self, data: list) -> list:
        return sorted(data, key=lambda x: x[1])

    def show_data(self, *data, table_fmt="fancy_grid") -> tabulate:
        df=None

        if len(data) == 0:
            df = self.__data
        else:
            df = data[0]

        try:            
            print(len(df[1:]), "data found")
            decrypted_data = []

            for x in df[1:]:
                decrypted_data.append([x[0], x[1], x[2], self.decrypt_pass(x[3])])

            return tabulate(self.sort_data(decrypted_data), headers=df[0], tablefmt=table_fmt)
        except Exception as e:
            return f"Something went wrong while trying to read the csv file\n{e}"

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

            encr_password = self.encrypt_pass(password)

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

            while True:
                is_commited = input("Save (y/n) ").lower() 
                if is_commited == "n":
                    return 0
                elif is_commited == "y":                    
                    with open(self.__file_name, "a") as f:
                        # Abort when the username is already exists
                        if (
                            new_data[1] in list_app and
                            new_data[2] in list_username
                        ):
                            print("\nData already exist!!!\n")
                            return 1
                        else:
                            writer = csv.writer(f)
                            writer.writerow(new_data)
                            self.__data.append(new_data)
                            print("Successfully adding data ++\n")
                            return 1
                else:
                    print("Invalid input!!!")
                    continue

        except Exception as e:
            sys.exit(e)

    def delete_data(self):
        temp_data = []
        with open(self.__file_name, "r") as f:
            for row in csv.reader(f):
                temp_data.append(row)

        if len(temp_data) < 2:
            print("No data available")
            input("Press enter to continue...")
        else:
            print(self.show_data(temp_data))
            while True:
                id = input("Select one id to be deleted (0 for back): ")
                if id == "0": 
                    break
                else:
                    try:
                        for x in temp_data:
                            if id in x:
                                temp_data.pop(temp_data.index(x))
                                
                                # Make a dict
                                dict_temp_data = []
                                header = temp_data[0] 
                                for row in temp_data[1:]:
                                    dict_temp_data.append(
                                        {
                                            header[0]: row[0], 
                                            header[1]: row[1],
                                            header[2]: row[2],
                                            header[3]: row[3]
                                        }
                                    )                        

                                # Store
                                with open(self.__file_name, "w") as f:
                                    writer = csv.DictWriter(f, fieldnames=header)
                                    writer.writeheader()
                                    writer.writerows(dict_temp_data)

                                    self.__data = temp_data
                                    input(f"\nSuccessfully deleting data with id [{id}] -- | press enter to continue")
                                return
                        print("id not found")        
                    except Exception as e:
                        print(e)

def generate_key():
    key = generate_secret_key()

    try:
        with open(".env", "w") as f:
            f.write(f"SECRET_KEY={key}")
    except Exception as e:
        sys.exit(e)

    sys.exit("Secret key generated successfully++")

def get_dotenv() -> dict:
    if os.environ["SECRET_KEY"] == "":
        sys.exit("KEY NOT FOUND: Run python project.py --generate-key")
    envs = {}
    try:
        envs["secret_key"] = os.environ["SECRET_KEY"]
    except Exception as e:
        sys.exit(e)
    
    return envs

def clear_screen(osname=os.name):
    if osname == "nt":
        return "cls" 
    else:
        return "clear"

def back_to_menu():
    while True:
        if not(input("0 for back\t: ") == "0"): continue    
        break
    os.system(clear_screen())

def get_ascii_art(text, font="banner3-D"):
    return pyfiglet.figlet_format(text,font=font)

def get_welcome_display():
    return """
    ====================================
          | WELCOME TO PASSNAGER | 
    ++==+++==+++==+++==+++==+++==+++==++
        [1] show data
        [2] add data       
        [3] delete data       
        [0] Exit       
    ===================================="""

def get_display():
    return """
    ====================================         
             |   PASSNAGER   |
    ++==+++==+++==+++==+++==+++==+++==++
        [1] show data
        [2] add data       
        [3] delete data       
        [0] Exit       
    ===================================="""
    
def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--generate-key" and os.environ["SECRET_KEY"] == "":
        generate_key()

    envs = get_dotenv()
    os.system(clear_screen())
    pm = Passnager(secret_key=envs["secret_key"])

    welcome_display = get_welcome_display()
    display = get_display()

    print(welcome_display)

    while True:
        try:
            choice = input("\n[*] Menu Choice: ")
        except EOFError:
            choice = "0"
        print()
        match choice:
            case "1":
                print(pm.show_data())
                back_to_menu()
            case "2":
                res = pm.add_data()
                if res == 1:
                    back_to_menu()
            case "3":
                pm.delete_data()
            case "0":
                os.system(clear_screen())
                print(get_ascii_art(text="seeyou"))
                input("Press enter to continue")
                os.system(clear_screen())
                sys.exit()
            case _:
                print("Invalid Input!!!\n")
                input("Press enter to continue")
                continue

        os.system(clear_screen())
        print(display)

if __name__ == "__main__":
    main()