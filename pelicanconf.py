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

ARTICLE_PATH = ["blog", "posts"]
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

# Article share widgets
SHARE = (
    ("twitter", "https://twitter.com/intent/tweet/?text=Features&amp;url="),
    ("linkedin", "https://www.linkedin.com/sharing/share-offsite/?url="),
    ("reddit", "https://reddit.com/submit?url="),
    ("facebook", "https://facebook.com/sharer/sharer.php?u="),
    ("whatsapp", "https://api.whatsapp.com/send?text=Features - "),
    ("telegram", "https://telegram.me/share/url?text=Features&amp;url="),
)