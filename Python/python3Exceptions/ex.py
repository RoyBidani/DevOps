
def check_pass(passwd):
    if len(passwd) < 8:
        raise ValueError("Password length should be at least 8 characters!")
    if not any(c.islower() for c in passwd):    # 'any' function to iterate over each character
        raise ValueError("Password length should be at least one lowercase letter!")
    if not any(c.isupper() for c in passwd):
        raise ValueError("Password length should be at least one uppercase letter!")
    if not any(c.isdigit() for c in passwd):
        raise ValueError("Password length should be at least one digit!")
    if not any(c in '@#$%' for c in passwd):
        raise ValueError("Password length should be at least one special character!")

    return True


try:
    print(check_pass("Roy1408b@"))
except ValueError as e:
    print(str(e))
