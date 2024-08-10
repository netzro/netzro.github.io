AUTHOR = 'Gifted'
SITENAME = 'Gifted Space'
#SITEURL = "http://127.0.0.1:8000"
PATH = "content"
TIMEZONE = 'Africa/Lagos'
DEFAULT_LANG = 'en'

SUBTITLE = 'Gifted say Welcome'
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
PAGE_SAVE_AS = 'pages/{slug}/index.html'  # Corrected line

COPYRIGHT = '©2024 - Gifted'
THEME = 'theme/Papyrus'
THEME_STATIC_PATHS = ['static']

DISPLAY_PAGES_ON_MENU = True
DIRECT_TEMPLATES = (('index', 'search', 'tags', 'categories', 'archives',))
PAGINATED_TEMPLATES = {'index': None, 'tag': None, 'category': None, 'author': None, 'archives': 24,}

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'

# Social widgets
SOCIAL = (
    ('github', 'https://github.com/netzro'),
    ('twitter', 'https://twitter.com/gifted_99'),
)


# Uncomment the following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
