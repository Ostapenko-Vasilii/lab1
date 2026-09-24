"""Заготовки задач на базовый Python."""

from grader_contracts.python_basics import PositiveIntegerInput, TextInput, VectorPairInput


def count_vowels(data: TextInput) -> int:
    text = data.value
    count = 0
    for i in text.lower():
        if i in 'aeiou':
            count += 1
    return count

# count_vowels tests

assert count_vowels(TextInput("a")) == 1
assert count_vowels(TextInput("a e i!owqsu")) == 5
assert count_vowels(TextInput("")) == 0
assert count_vowels(TextInput("123wfhw")) == 0
assert count_vowels(TextInput("abcde")) == 2
assert count_vowels(TextInput("aeiou")) == 5
assert count_vowels(TextInput("AEIOU")) == 5
assert count_vowels(TextInput("AeIopU")) == 5
assert count_vowels(TextInput("wdw")) == 0


def has_unique_characters(data: TextInput) -> bool:
    text = data.value
    return len(set(text)) == len(text)

assert has_unique_characters(TextInput("a")) == True
assert has_unique_characters(TextInput("abc")) == True
assert has_unique_characters(TextInput("")) == True
assert has_unique_characters(TextInput("aac")) == False



def count_one_bits(data: PositiveIntegerInput) -> int:
    number = data.value
    count = 0
    for i in bin(number):
        if i == "1":
            count += 1
    return count

assert count_one_bits(PositiveIntegerInput(0)) == 0
assert count_one_bits(PositiveIntegerInput(1)) == 1
assert count_one_bits(PositiveIntegerInput(63)) == 6
assert count_one_bits(PositiveIntegerInput(128)) == 1
assert count_one_bits(PositiveIntegerInput(129)) == 2



def multiplicative_persistence(data: PositiveIntegerInput) -> int:
    number = data.value
    count = 0
    while number // 10 != 0:
        count += 1
        new_number = 1
        for i in str(number):
            new_number *= int(i)
        number = new_number
    return count

assert multiplicative_persistence(PositiveIntegerInput(10)) == 1
assert multiplicative_persistence(PositiveIntegerInput(205)) == 1
assert multiplicative_persistence(PositiveIntegerInput(39)) == 3
assert multiplicative_persistence(PositiveIntegerInput(1)) == 0
assert multiplicative_persistence(PositiveIntegerInput(9)) == 0
assert multiplicative_persistence(PositiveIntegerInput(999)) == 4



def mse(data: VectorPairInput) -> float:
    predicted, expected = data.predicted, data.expected
    n = len(predicted)
    if n != len(expected) or n == 0: raise ValueError()
    summ = 0
    for i in range(n):
        summ += (predicted[i] - expected[i])**2
    return 1/n * summ

assert abs(mse(VectorPairInput([1, 1, 1], [1, 1, 1])) - 0.0) < 1e-6
assert abs(mse(VectorPairInput([1,1,1], [2,2,2])) - 1) < 1e-6
assert abs(mse(VectorPairInput([2,2,2], [1,1,1])) - 1) < 1e-6
assert abs(mse(VectorPairInput([0], [1])) - 1) < 1e-6
assert abs(mse(VectorPairInput([7,8,4], [1,0,0])) - (116 / 3)) < 1e-6

try:
    mse(VectorPairInput([1, 2, 3], [1, 2]))
    assert False
except ValueError:
    pass

try:
    mse(VectorPairInput([], []))
    assert False
except ValueError:
    pass


def prime_factorization(data: PositiveIntegerInput) -> str:
    number = data.value
    if number == 1: return "(1)"
    f = []
    i = 2
    while i * i <= number:
        st = 0
        while number % i == 0:
            st += 1
            number //= i
        if st > 0:
            if st == 1:
                f.append(f"{i}")
            else:
                f.append(f"{i}**{st}")
        i += 1
    if number != 1:
        f.append(number)
    return "".join(f"({p})" for p in f)
assert prime_factorization(PositiveIntegerInput(4)) == "(2**2)"
assert prime_factorization(PositiveIntegerInput(27)) == "(3**3)"
assert prime_factorization(PositiveIntegerInput(30)) == "(2)(3)(5)"
assert prime_factorization(PositiveIntegerInput(101)) == "(101)"
assert prime_factorization(PositiveIntegerInput(68)) == "(2**2)(17)"
assert prime_factorization(PositiveIntegerInput(86240)) == "(2**5)(5)(7**2)(11)"
assert prime_factorization(PositiveIntegerInput(1)) == "(1)"
assert prime_factorization(PositiveIntegerInput(11)) == "(11)"


def pyramid(data: PositiveIntegerInput) -> int | str:
    cube_count = data.value
    left = 0
    right = cube_count
    while left < right:
        middle = (left + right) // 2
        if cube_count <= (middle * ((middle + 1) * (2 * middle + 1)) // 6):
            right = middle
        else:
            left = middle + 1
    if right * ((right + 1) * (2 * right + 1)) // 6 == cube_count:
        return right
    else:
        return "It is impossible"

assert pyramid(PositiveIntegerInput(1)) == 1
assert pyramid(PositiveIntegerInput(2)) == "It is impossible"
assert pyramid(PositiveIntegerInput(4)) == "It is impossible"
assert pyramid(PositiveIntegerInput(5)) == 2
assert pyramid(PositiveIntegerInput(6)) == "It is impossible"
assert pyramid(PositiveIntegerInput(13)) == "It is impossible"
assert pyramid(PositiveIntegerInput(14)) == 3


def is_balanced_number(data: PositiveIntegerInput) -> bool:
    number = data.value
    n = len(str(number))
    b = ((n + 1) % 2)
    n = n // 2
    right = number % 10 ** (n - b)
    left = number // 10 ** (n + 1)
    summ_right = 0
    for i in str(right):
        summ_right += int(i)
    summ_left = 0
    for i in str(left):
        summ_left += int(i)
    return summ_right == summ_left

assert is_balanced_number(PositiveIntegerInput(121121)) == True
assert is_balanced_number(PositiveIntegerInput(12121)) == True
assert is_balanced_number(PositiveIntegerInput(131121)) == False
assert is_balanced_number(PositiveIntegerInput(12129)) == False
assert is_balanced_number(PositiveIntegerInput(121121)) == True
assert is_balanced_number(PositiveIntegerInput(1)) == True
assert is_balanced_number(PositiveIntegerInput(12)) == True
assert is_balanced_number(PositiveIntegerInput(122)) == False
