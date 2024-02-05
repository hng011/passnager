import os
import sys
import csv
from dotenv import load_dotenv
from tabulate import tabulate
from passnager_modules.PassCrypt import pass_encrypt, pass_decrypt

class Passnager:
    def __init__(self, file_name: str="data.csv"):
        self.__data = []
        # Open file
        while True:
            try:
                with open(file_name, "r") as f:
                    print(f"Read {file_name} file")
                    for row in csv.reader(f):
                        self.__data.append(row)
                    break
            except FileNotFoundError:
                # Only in development: delete this when you're already in production
                dummy = [
                    {"no":1,"username_or_email":"dummy1","password":"dummy1"},
                    {"no":2,"username_or_email":"dummy2","password":"dummy2"}
                ]
                print(f"Create {file_name} file")
                headers: list = ["no", "username_or_email", "password"]
                with open("./data.csv", "w") as f:
                    writer = csv.DictWriter(f, fieldnames=headers)
                    writer.writeheader()
                    writer.writerows(dummy)
                continue

    def show_data(self, table_fmt="fancy_grid") -> tabulate:
        try:
            return tabulate(self.__data[1:], headers=self.__data[0], tablefmt=table_fmt)
        except:
            return "Something went wrong while trying to read a csv file"

    def create_data():
        ...

    def read_data():
        ...

    def update_data():
        ...

    def delete_data():
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

def main():
    pm = Passnager()

    # test
    print(pm.show_data())

if __name__ == "__main__":
    main()