"""Constants for Foodgram."""

# for users model

USER_REGEX = r'^[\w.@+-]+$'
USERFIELDS_LENGTH = 150
EMAIL_LENGTH = 254

# for core models

DEFAULT_LENGTH = 100
NAME_LENGTH = 256
TAG_LENGTH = 32
HASH_LENGTH = 32

NAME_INGREDIENT_LENGTH = 128
MEASUREMENT_UNIT_LENGTH = 64

MIN_VALUE = 1
MAX_VALUE = 1000
INVALID_MIN_MESSAGE = 'Недопустимое минимальное значение.'
INVALID_MAX_MESSAGE = 'Недопустимое максимальное значение.'

# for utils

MIN_HASH_LENGTH = 3
MAX_HASH_LENGTH = 12

# for admin zone

INGREDIENTS_PER_PAGE = 20
TAGS_PER_PAGE = 20
RECIPES_PER_PAGE = 20
USERS_PER_PAGE = 20
SUBS_PER_PAGE = 20

# pagination

PAGE_SIZE = 6
