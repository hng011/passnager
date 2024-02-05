from project import Passnager, get_welcome_display, get_display, get_ascii_art, clear_screen 
from pyfiglet import figlet_format

test_default_key = "O4O-B7ZlJpbidLJi3YMBDr8J48sNvdSqSdRwCNZ6Qhk="
test_password = "test123"

def test_encrypt_password():
    pm = Passnager(secret_key=test_default_key)
    assert type(pm.encrypt_pass(plain_pwd=test_password)) == str
    assert len(pm.encrypt_pass(plain_pwd=test_password)) == 100

def test_decrypt_password():
    pm = Passnager(secret_key=test_default_key)
    token = pm.encrypt_pass(plain_pwd=test_password)
    assert type(pm.decrypt_pass(encrypted_pwd=token)) == str
    assert len(pm.decrypt_pass(encrypted_pwd=token)) == 7

def test_sort_data():
    assert Passnager.sort_data(Passnager,data=[["id2","app2","user2","pwd2"],["id1","app1","user1","pwd1"]]) == [["id1","app1","user1","pwd1"],["id2","app2","user2","pwd2"]]

def test_get_welcome_display():
    assert len(get_welcome_display()) == 264

def test_get_display():
    assert len(get_display()) == 268

def test_get_ascii_art():
    assert get_ascii_art("test") == figlet_format("test", font="banner3-D")

def test_clear_screen():
    assert clear_screen(osname="nt") == "cls"
    assert clear_screen() == "clear"