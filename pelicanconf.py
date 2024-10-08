from datetime import datetime
from pelican import signals

AUTHOR = 'Gifted'
SITENAME = 'Gifted Space'
SITEURL = ""
PATH = "content"
TIMEZONE = 'Africa/Lagos'
DEFAULT_LANG = 'en'

SUBTITLE = 'Gifted say welcome'
SUBTEXT = '''My allocated space on the internet where
I record my Doings, Thoughts and Writing.
'''
USE_FOLDER_AS_CATEGORY = False
DISPLAY_CATEGORIES_ON_MENU = False
SUMMARY_MAX_LENGTH = 17
DEFAULT_PAGINATION = 8

ARTICLE_PATH = ["blog"]
PAGE_PATH = ["pages"]

ARTICLE_URL = 'posts/{date:%Y}/{date:%b}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%b}/{date:%d}/{slug}/index.html'
PAGE_URL = 'pages/{slug}/'
PAGE_SAVE_AS = 'pages/{slug}/index.html'

COPYRIGHT = '©2024 - Gifted'
THEME = 'theme/Papyrus'
THEME_STATIC_PATHS = ['static']

DISPLAY_PAGES_ON_MENU = True
DIRECT_TEMPLATES = (('index', 'tags', 'archives',))
PAGINATED_TEMPLATES = {'index': None, 'tag': None, 'category': None, 'author': None, 'archives': 24,}

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'

# Social widgets
SOCIAL = (
    ('github', 'https://github.com/netzro'),
    ('twitter', 'https://twitter.com/gifted_99'),
)

# #100DaysToOffload configuration
OFFLOAD_START_DATE = datetime(2024, 8, 10)  # The date you started the challenge
TOTAL_DAYS = 365  # Total days of the challenge

# Function to calculate the remaining days in the challenge
def calculate_days_left():
    today = datetime.today()
    days_passed = (today - OFFLOAD_START_DATE).days
    return TOTAL_DAYS - days_passed

# Function to count the number of posts tagged with #100DaysToOffload
def count_offload_posts(generator):
    offload_posts = [article for article in generator.articles if '#100DaysToOffload' in article.tags]
    generator.context['OFFLOAD_COUNT'] = len(offload_posts)
    generator.context['DAYS_LEFT'] = calculate_days_left()

# Connect the count_offload_posts function to Pelican's article generator
def register():
    signals.article_generator_finalized.connect(count_offload_posts)

register()
