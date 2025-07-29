import random
from typing import Literal, Union, Optional, Sequence, Any, List, Callable


RANDOM_METHODS = ["random_list", "random_matrix", "random_tuple", "random_dict"
                  "random_set", "random_str", "random_tensor"]


# ===== English Alphabet =====
EN_ALPHABET_LOWER = "abcdefghijklmnopqrstuvwxyz"
EN_ALPHABET_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
EN_ALPHABET_ALL = EN_ALPHABET_LOWER + EN_ALPHABET_UPPER

# Vowels
EN_VOWELS_LOWER = "aeiouy"
EN_VOWELS_UPPER = "AEIOUY"
EN_VOWELS_ALL = EN_VOWELS_LOWER + EN_VOWELS_UPPER

# Consonants
EN_CONSONANTS_LOWER = "bcdfghjklmnpqrstvwxz"
EN_CONSONANTS_UPPER = "BCDFGHJKLMNPQRSTVWXZ"
EN_CONSONANTS_ALL = EN_CONSONANTS_LOWER + EN_CONSONANTS_UPPER

# ===== Russian Alphabet =====
RU_ALPHABET_LOWER = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
RU_ALPHABET_UPPER = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
RU_ALPHABET_ALL = RU_ALPHABET_LOWER + RU_ALPHABET_UPPER

# Vowels
RU_VOWELS_LOWER = "аеёиоуыэюя"
RU_VOWELS_UPPER = "АЕЁИОУЫЭЮЯ"
RU_VOWELS_ALL = RU_VOWELS_LOWER + RU_VOWELS_UPPER

# Consonants
RU_CONSONANTS_LOWER = "бвгджзйклмнпрстфхцчшщ"
RU_CONSONANTS_UPPER = "БВГДЖЗЙКЛМНПРСТФХЦЧШЩ"
RU_CONSONANTS_ALL = RU_CONSONANTS_LOWER + RU_CONSONANTS_UPPER

# Hard/Soft signs
RU_SIGNS_LOWER = "ъыь"
RU_SIGNS_UPPER = "ЪЫЬ"
RU_SIGNS_ALL = RU_SIGNS_LOWER + RU_SIGNS_UPPER

# ===== Special Characters =====
PUNCTUATION = ".,!?;:'\"()-–—[]{}…/"
MATH_SYMBOLS = "+-×÷=≠≈<>≤≥^√%‰°"
CURRENCY_SYMBOLS = "$€£¥₽₹₩₺₴"
OTHER_SYMBOLS = "@#&*\\|~_©®™§¶•"
WHITESPACE = " \t\n\r\v\f"

# ===== Numbers =====
DIGITS_ARABIC = "0123456789"
DIGITS_ROMAN = "ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫⅬⅭⅮⅯ"
DIGITS_WORDS_EN = ["zero", "one", "two", "three", "four", 
                  "five", "six", "seven", "eight", "nine"]
DIGITS_WORDS_RU = ["ноль", "один", "два", "три", "четыре",
                  "пять", "шесть", "семь", "восемь", "девять"]

# ===== Combined Sets =====
LETTERS_ALL = EN_ALPHABET_ALL + RU_ALPHABET_ALL
SYMBOLS_ALL = PUNCTUATION + MATH_SYMBOLS + CURRENCY_SYMBOLS + OTHER_SYMBOLS
ALPHANUMERIC_EN = EN_ALPHABET_ALL + DIGITS_ARABIC
ALPHANUMERIC_RU = RU_ALPHABET_ALL + DIGITS_ARABIC
PRINTABLE_CHARS = LETTERS_ALL + DIGITS_ARABIC + SYMBOLS_ALL + WHITESPACE

# ===== Private Def =====
def _get_charset(language: str, category: Optional[str], case: str) -> str:
    """Select charset based on parameters"""
    base = {
        'en': {
            'all': EN_ALPHABET_ALL,
            'vowels': EN_VOWELS_ALL,
            'consonants': EN_CONSONANTS_ALL
        },
        'ru': {
            'all': RU_ALPHABET_ALL,
            'vowels': RU_VOWELS_ALL,
            'consonants': RU_CONSONANTS_ALL,
            'signs': RU_SIGNS_ALL
        }
    }.get(language, {}).get(category or 'all', PRINTABLE_CHARS)
    
    if case == 'lower':
        return base.lower()
    elif case == 'upper':
        return base.upper()
    return base

def _generate_digit(weights: Optional[Sequence[float]]) -> Union[str, int]:
    """Generates digit in different formats"""
    formats = [
        (DIGITS_ARABIC, 0.6),
        (DIGITS_ROMAN, 0.2),
        (DIGITS_WORDS_EN, 0.1),
        (DIGITS_WORDS_RU, 0.1)
    ]
    
    charset, *rest = random.choices(
        [f[0] for f in formats],
        weights=weights or [f[1] for f in formats]
    )[0]
    
    if isinstance(charset, list):
        return random.choice(charset)
    return random.choice(charset)


# ===== Public Def =====

def random_list(
    length: int = 10,
    *,
    # Core generation parameters
    min_value: Union[int, float] = 0,
    max_value: Union[int, float] = 100,
    value_type: Literal['int', 'float', 'str', 'bool', 'mixed', 'letter', 'digit', 'custom'] = "int",
    
    # Uniqueness and sorting parameters
    unique: bool = False,
    sorted: bool = False,
    
    # Custom elements parameters
    elements: Optional[Sequence[Any]] = None,
    weights: Optional[Sequence[float]] = None,
    
    # String generation parameters
    string_length: int = 5,
    charset: Optional[str] = None,
    language: Literal['en', 'ru'] = "en",
    char_category: Optional[Literal['all', 'vowels', 'consonants', 'signs']] = None,
    case: str = "mixed",  # 'lower', 'upper', 'mixed'
    
    # Nested structures parameters
    nested: bool = False,
    nested_depth: int = 1,
    nested_length: int = 3,
    
    # Additional control parameters
    generator: Optional[Callable[[int], Any]] = None,
    seed: Optional[int] = None,
    
    # Element processing
    function: Optional[Callable[[Any], Any]] = None  # Lambda for element transformation
) -> List[Any]:
    """
    Generates a highly customizable random list with support for multiple languages and data types.

    This function provides extensive control over list generation including:
    - Numeric values (integers/floats) within specified ranges
    - Text generation with language-specific character sets
    - Mixed-type lists with configurable probabilities
    - Nested list structures
    - Unique element enforcement and sorting options
    - Post-generation element processing

    Args:
        length (int): Desired length of the list (default: 10)
        min_value (Union[int, float]): Minimum value for numeric types (default: 0)
        max_value (Union[int, float]): Maximum value for numeric types (default: 100)
        value_type (str): Type of elements to generate. Options:
            - 'int': Integer numbers
            - 'float': Floating-point numbers
            - 'str': Random strings
            - 'bool': Boolean values
            - 'mixed': Mixed types
            - 'letter': Single letters
            - 'digit': Numeric representations
            - 'custom': Use provided elements (default: 'int')
        unique (bool): Whether elements must be unique (default: False)
        sorted (bool): Whether to sort the resulting list (default: False)
        elements (Optional[Sequence[Any]]): Custom elements when value_type='custom'
        weights (Optional[Sequence[float]]): Probability weights for custom/mixed types
        string_length (int): Length of generated strings (default: 5)
        charset (Optional[str]): Custom character set for string generation
        language (str): Language for character generation ('en' or 'ru') (default: 'en')
        char_category (Optional[str]): Character category. Options:
            - 'all': All letters
            - 'vowels': Only vowels
            - 'consonants': Only consonants
            - 'signs': Only signs (Russian only)
        case (str): Letter casing. Options: 'lower', 'upper', 'mixed' (default: 'mixed')
        nested (bool): Whether to generate nested lists (default: False)
        nested_depth (int): Maximum nesting depth (default: 1)
        nested_length (int): Length of nested lists (default: 3)
        generator (Optional[Callable[[int], Any]]): Custom element generator function
        seed (Optional[int]): Random seed for reproducible results
        element_processor (Optional[Callable[[Any], Any]]): Transformation function applied to each 
            generated element. The function receives the element and should return the processed version.
            Applied to both top-level and nested elements. (default: None)

    Returns:
        List[Any]: A randomly generated list according to specified parameters

    Raises:
        ValueError: If invalid parameters are provided (e.g., not enough unique elements)
        TypeError: If sorting fails due to mixed incompatible types

    Examples:
        >>> # Basic integer list
        >>> random_list(5, value_type='int')
        [42, 87, 15, 93, 61]

        >>> # Russian vowels in uppercase
        >>> random_list(3, value_type='letter', language='ru', 
        ...             char_category='vowels', case='upper')
        ['А', 'У', 'О']

        >>> # Mixed-type nested structure with processing
        >>> random_list(4, value_type='mixed', nested=True,
        ...             element_processor=lambda x: str(x).upper())
        ['28', ['FOO', '3.14'], 'TRUE', ['FALSE', 'BAR']]

        >>> # Custom elements with weights and processing
        >>> random_list(5, value_type='custom', 
        ...             elements=['red', 'green', 'blue'],
        ...             weights=[0.5, 0.3, 0.2],
        ...             element_processor=lambda x: f"color_{x}")
        ['color_red', 'color_blue', 'color_red', 'color_green', 'color_red']

        >>> # Number processing
        >>> random_list(3, value_type='int',
        ...             element_processor=lambda x: x**2)
        [16, 64, 9]

    Notes:
        - When using unique=True with nested lists, entire sublists are considered for uniqueness
        - Sorting mixed-type lists will convert elements to strings for comparison
        - Character categories are language-specific (e.g., 'signs' only applies to Russian)
        - For string generation, charset overrides language/char_category parameters
        - When using seed, results will be reproducible across runs
        - The element_processor is applied:
            * After element generation
            * Before uniqueness checking
            * Before sorting
            * Recursively to nested elements
        - For nested structures, the processor receives entire sublists
    """
    if seed is not None:
        random.seed(seed)
    
    # Character set selection
    if charset is None and value_type == "str":
        charset = _get_charset(language, char_category, case)
    
    if generator is not None:
        result = [generator(i) for i in range(length)]
        return [function(x) for x in result] if function else result
    
    value_generators = {
        'int': lambda: random.randint(int(min_value), int(max_value)),
        'float': lambda: random.uniform(min_value, max_value),
        'str': lambda: ''.join(random.choices(charset, k=string_length)),
        'bool': lambda: random.choice([True, False]),
        'mixed': lambda: random.choices(
            [random.randint(int(min_value), int(max_value)),
             random.uniform(min_value, max_value),
             ''.join(random.choices(charset or PRINTABLE_CHARS, k=string_length)),
             random.choice([True, False])],
            weights=weights or [0.4, 0.3, 0.2, 0.1])[0],
        'letter': lambda: random.choice(charset or LETTERS_ALL),
        'digit': lambda: _generate_digit(weights)
    }
    
    if value_type == 'custom' and elements:
        if unique and len(elements) < length:
            raise ValueError("Not enough unique elements for requested length")
        if weights and len(weights) != len(elements):
            raise ValueError("Weights length must match elements length")
        
        result = random.sample(elements, k=length) if unique else random.choices(elements, weights=weights, k=length)
        return [function(x) for x in result] if function else result
    
    if value_type not in value_generators and value_type != 'custom':
        raise ValueError(f"Unsupported value_type: {value_type}")
    
    def generate_element():
        if nested and random.random() < 0.3 and nested_depth > 0:
            nested_result = random_list(
                length=nested_length,
                min_value=min_value,
                max_value=max_value,
                value_type=value_type,
                unique=unique,
                sorted=sorted,
                weights=weights,
                elements=elements,
                string_length=string_length,
                charset=charset,
                language=language,
                char_category=char_category,
                case=case,
                nested=True,
                nested_depth=nested_depth-1,
                nested_length=nested_length,
                generator=generator,
                function=function  # Pass processor to nested calls
            )
            return function(nested_result) if function else nested_result
        generated = value_generators[value_type]()
        return function(generated) if function else generated
    
    result = []
    seen = set()
    
    while len(result) < length:
        element = generate_element()
        
        if unique:
            element_key = tuple(element) if isinstance(element, list) else element
            if element_key in seen:
                continue
            seen.add(element_key)
        
        result.append(element)
    
    if sorted:
        try:
            result.sort()
        except TypeError:
            result.sort(key=lambda x: str(x))
    
    return result

def random_matrix():
    pass

def random_tensor():
    pass

def random_tuple():
    pass

def random_dict():
    pass

def random_set():
    pass

def random_str():
    pass