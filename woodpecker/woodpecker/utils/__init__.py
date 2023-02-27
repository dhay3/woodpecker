import string
from loguru import logger


def phone_checker(phone: str):
    if 6 <= len(phone) <= 12:
        phone = [n for n in phone if n in string.digits]
        return ''.join(phone).strip()
    else:
        raise Exception('Invalid Phone number.')


# if __name__ == '__main__':
#     phone_checker('ffff')
