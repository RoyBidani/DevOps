# ex1:

def remove_non_strings(lst):
    result = []
    for item in lst:
        if isinstance(item,str):
            result.append(item)
    return result


my_list = [1, 'roy', 3.14, 'noy', True, 'aline']
result1 = remove_non_strings(my_list)
print(result1)


# ex2:

def count_letters(string):
    counter = {}
    for c in string:
        if c in counter:
            counter[c] += 1
        else:
            counter[c] = 1
    return counter


my_string = "roy is the most handsome guy in the world!"
letters_dict = count_letters(my_string)
print(letters_dict)


def count_letters_without_if(string):
    counter = {}
    for c in string:
        # get the current count for the letter c and set it to 0 if it doesn't exist. Then, we increment the count by 1.
        counter[c] = counter.get(c,0) + 1
    return counter


my_string2 = "roy is the most handsome guy in the world!"
print(count_letters_without_if(my_string2))


# ex3:

def common_elements(list1,list2):
    common = []
    for element in list1:
        if element in list2:
            common.append(element)
    return common


lista = [1,2,3,4,5]
listb = [3,4,5,6,7]
print(common_elements(listb,lista))


# ex4:

def unique_values(dict1):
    set1 = set(dict1.values())
    lst = list(set1)
    return lst


dict2 = {'a':1,'b':1,'c':2}
print(unique_values(dict2))


# ex5:

def left_rotate(lst):
    return lst[1:] + [lst[0]]


list_my = [1,2,3,4,5]
print(left_rotate(list_my))


# ex6:


def remove_second(lst):
    counter = 1
    while len(lst) > 0:
        if counter % 2 == 0:
            print(lst.pop(0))
        else:
            lst.pop(0)
        counter += 1


listc = [1,2,3,4,5,6,7,8,9,10]
remove_second(listc)


# ex7:

def dict_to_tuple(dictt):
    return list(dictt.items())


my_dict = {'a': 1, 'b': 2, 'c': 3}
print(dict_to_tuple(my_dict))



# ex8:

def min_max_keys(dict1):
    values = list(dict1.values())
    max_value = max(values)
    min_value = min(values)
    max_keys = [key for key, value in dict1.items() if value == max_value]
    min_keys = [key for key, value in dict1.items() if value == min_value]
    print("Maximum key:", max_keys)
    print("Minimum key:", min_keys)


my_dict2 = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
min_max_keys(my_dict2)


