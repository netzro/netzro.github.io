AUTHOR = 'Gifted'
SITENAME = 'Gifted Space'
PATH = "content"
TIMEZONE = 'Africa/Lagos'
DEFAULT_LANG = 'en'

SITEURL = ""
SUBTITLE = 'Gifted say welcome'
SUBTEXT = '''My allocated space on the internet where
I record my Doings, Thoughts and Writing.
'''
USE_FOLDER_AS_CATEGORY = False
DISPLAY_CATEGORIES_ON_MENU = False
SUMMARY_MAX_LENGTH = 15
DEFAULT_PAGINATION = 8

ARTICLE_PATH = ["posts"]
PAGE_PATH = ["pages"]

ARTICLE_URL = 'posts/{date:%Y}/{date:%b}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%b}/{date:%d}/{slug}/index.html'

GOOGLE_ANALYTICS = 'G-VJD75C7TTC'
PAGE_URL = 'pages/{slug}/'
PAGE_SAVE_AS = 'pages/{slug}/index.html'

COPYRIGHT = '©2026 - Gifted'
THEME = 'theme/Papyrus'
THEME_STATIC_PATHS = ['static']
STATIC_PATHS = ['images', 'extra']

# Map robots.txt to site root
EXTRA_PATHS = [
    'extra/robots.txt',
]
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
}

DISPLAY_PAGES_ON_MENU = False
DIRECT_TEMPLATES = (('index', 'tags', 'archives',))
PAGINATED_TEMPLATES = {'index': None, 'tag': None, 'category': None, 'author': None, 'archives': 24,}

# Plugins
PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['sitemap']

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