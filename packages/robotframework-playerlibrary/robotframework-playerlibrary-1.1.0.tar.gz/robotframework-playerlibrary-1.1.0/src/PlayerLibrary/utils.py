import json
import string
from json import JSONDecodeError
import random
from robotlibcore import keyword
from robot.libraries.BuiltIn import BuiltIn as Robot


def pretty_logging(content):
    try:
        parsed_dict = json.loads(content)
    except (JSONDecodeError, TypeError):
        parsed_dict = content
    indent_one = json.dumps(parsed_dict, indent=4, sort_keys=True)
    code_snippet = f"""
    <script src="https://cdn.jsdelivr.net/gh/google/code-prettify@master/loader/run_prettify.js"></script>
        <pre class="prettyprint">{indent_one}</pre>
    """
    Robot().log(message=code_snippet, html=True)


def random_word(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def random_number_chars(length):
    digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    return ''.join(random.choice(digits) for _ in range(length))


@keyword("should be equal as amounts")
def should_be_equal_as_amounts(number_1, number_2, deviation: float = 0.01):
    """
    Compare 2 numbers with the acceptable deviation

    E.g: With ``deviation``= 0.01, ``7.01`` will be equal to ``7.00``

    *number_1*: the first number

    *number_2*: the second number

    *deviation*: the acceptable amount of deviation
    """
    number_1 = str(number_1).replace(",", "")
    number_2 = str(number_2).replace(",", "")
    difference = round(float(number_1) - float(number_2), 4)
    if abs(difference) <= deviation:
        pass
    else:
        Robot().should_be_equal_as_numbers(number_1, number_2)


@keyword("should not be equal as amounts")
def should_not_be_equal_as_amounts(number_1, number_2):
    """
    Negative keyword of `should be equal as amounts`
    """
    difference = round(float(number_1) - float(number_2), 2)
    if abs(round(difference, 2)) <= 0.01:
        raise AssertionError("The number is likely equal")
    else:
        Robot().should_not_be_equal_as_numbers(number_1, number_2)


def rgb_to_hex(color_tuple):
    return '#' + ''.join(f'{i:02X}' for i in color_tuple)


def escape_single_quote(text):
    return text.replace("'", "\'")
