# ex1:

def count_character(string, char):
    count = 0
    for c in string:
        if c == char:
            count += 1
    return count


print(count_character("roy the king", 'r'))

# ex2:


def flip_number(number):
    if isinstance(number, int):
        return int(str(number)[::-1])      # reverses it using slicing ([::-1])
    if isinstance(number, float):
        return float(str(number)[::-1])
    if isinstance(number, str):
        return str(number)[::-1]


print(flip_number(122.5))


# ex3:

def cel_to_fahr(celsius):
    return (celsius * 9/5) + 32


print(cel_to_fahr(100))


# ex4:

def is_leap_year(year):
    if year % 400 == 0:
        return True
    if year % 100 == 0:                ````
        return False
    if year % 4 == 0:
        return True

    return False


def is_leap_year_one_if(year):
    return year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)


print(is_leap_year(2004))
print(is_leap_year_one_if(2006))


# ex5:

def check_pass(passwd):
    if len(passwd) < 8:
        return False
    if not any(c.islower() for c in passwd):    # 'any' function to iterate over each character
        return False
    if not any(c.isupper() for c in passwd):
        return False
    if not any(c.isdigit() for c in passwd):
        return False
    if not any(c in '@#$%' for c in passwd):
        return False

    return True


print(check_pass("Roy1408b@"))


# ex6:

def sum_of_divisors(num):
    div_count = 0
    for i in range(1,num+1):
        if num % i == 0:
            print("can divided by", i)
            div_count += 1

    return div_count


print("total divisors", sum_of_divisors(10))


# ex7:

def breakdown_money(money):
    banknotes = [200,100,50,20,10,5,2,1]
    breakdown = {}           # This dictionary will store the count banknotes needed
    for banknote in banknotes:
        if money >= banknote:       # check if the banknote is less equal to the remaining money
            # calculates the number of times the current banknote can be used to form the money.
            count = money // banknote
            breakdown[banknote] = count     # The count is stored in the breakdown dictionary with the banknote
            money -= count * banknote   # updates the remaining money
    return breakdown


print(breakdown_money(12))


# ex8:

def is_prime(num):
    if num == 1:
        return False
    elif num > 1:
        for i in range(2,num):
            if (num % i) == 0:
                return False

    return True


print(is_prime(29))
