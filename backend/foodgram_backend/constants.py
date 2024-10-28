"""Constants for FOODGRAM PROJECT"""

# for users models

USER_REGEX = r'^[\w.@+-]+$'
USERFIELDS_LENGTH = 150
EMAIL_LENGTH = 254

# for core models

DEFAULT_LENGTH = 100
NAME_LENGTH = 256
TAG_LENGTH = 32

NAME_INGREDIENT_LENGTH = 128
MEASUREMENT_UNIT_LENGTH = 64

MIN_VALUE = 1
MAX_VALUE = 1000
INVALID_MIN_MESSAGE = 'Недопустимое минимальное значение.'
INVALID_MAX_MESSAGE = 'Недопустимое максимальное значение.'
