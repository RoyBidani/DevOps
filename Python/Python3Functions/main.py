# ex1:
words = ["hey","hello","hola","shalom","bye"]
print(words)
new_words = list(filter(lambda word: word != "bye",words))
print("after filtering with lambda:",new_words)


# ex2:
my_list = ["5", "2", "10", "1", "7"]
print(my_list)
sorted_list = sorted(my_list, key=lambda x: int(x))
print("after numerically sort:",sorted_list)


# ex3:
my_list2 = [1,2,-3,-4,5,6,-7,-8,9,10]
print(my_list2)
positive = sum(filter(lambda x: x > 0, my_list2))
negative = sum(filter(lambda x: x < 0, my_list2))
print("sum of positive:", positive)
print("sum of negative:", negative)


# ex4:
even_square = [x*x for x in my_list2 if x % 2 == 0]
print("Even square:",even_square)


# ex5:
def sale(dict1):
    sale_prices = dict(map(lambda x: (x[0], x[1] * 0.9), dict1.items()))
    return sale_prices


products = {
    "shirt": 50,
    "pants": 75,
    "jacket": 100,
    "suite": 200
}
print("prices before sale:", products)
print("prices after sale:", sale(products))


# ex6:
cipher = {
        'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9, 'י': 10,
        'כ': 20, 'ך': 500, 'ל': 30, 'מ': 40, 'ם': 600, 'נ': 50, 'ן': 700, 'ס': 60, 'ע': 70,
        'פ': 80, 'ף': 800, 'צ': 90, 'ץ': 900, 'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400, ' ': 0
    }
sentence1 = "שלום"
sentence2 = "אינפיניטי לאבס"

value1 = sum(cipher.get(c, 0) for c in sentence1)
value2 = sum(cipher.get(c, 0) for c in sentence2)

print("שלום",value1)
print("אינפיניטי לאבס",value2)


# ex7:
def luhn(card_number):
    card_number = str(card_number)

    # double every second digits start from the end
    double = [int(num) * 2 if i % 2 != 0 else int(num) for i, num in enumerate(card_number[::-1])]

    # substract 9 from any number greater than 9
    substracted = [num - 9 if num > 9 else num for num in double]

    # take the sum of all digits
    card_sum = sum(substracted)

    # check if the sum is evenly divisible by 10, if it is valid will be true otherwise false.
    valid = card_sum % 10 == 0

    return valid


card1 = "6011000990139424"  # true
card2 = "4580175109494129"  # false
card3 = "4532015112830367"  # false
card4 = "4532015112830366"  # true

print(f"Card number: {card1} valid: {luhn(card1)}")
print(f"Card number: {card2} valid: {luhn(card2)}")
print(f"Card number: {card3} valid: {luhn(card3)}")
print(f"Card number: {card4} valid: {luhn(card4)}")
