import pyperclip
import random
from string import ascii_letters, digits

valid_chars = ascii_letters + digits + '!@#$%^&*()".,></?`~|'


def generate_key(length=2048):
    key = [random.choice(valid_chars) for _ in range(length)]
    key = ''.join(key)
    return key


keys = [generate_key() for _ in range(4)]

output = f'''private_password = """{keys[0]}"""

private_salt = """{keys[1]}"""

public_password = """{keys[2]}"""

public_salt = """{keys[3]}"""

'''

pyperclip.copy(output)
