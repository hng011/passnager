import os
import sys
from dotenv import load_dotenv
from passnager_modules.PassCrypt import pass_encrypt, pass_decrypt

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
    pass_encrypt()
    pass_decrypt()
    envs = get_dotenv()
    print(envs["app_name"])
    print(envs["secret_key"])

if __name__ == "__main__":
    main()