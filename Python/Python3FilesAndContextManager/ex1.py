import string

for l in string.ascii_uppercase:
    filename = f"{l}.txt"
    with open(filename, 'w') as file:
        file.write(l)
