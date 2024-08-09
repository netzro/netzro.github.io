AUTHOR = 'Gifted'
SITENAME = 'Gifted Space'
SITEURL = ""
PATH = "content"
TIMEZONE = 'Africa/Lagos'
DEFAULT_LANG = 'en'

SUBTITLE = 'Gifted say Welcome'
SUBTEXT = '''My allocated space on the internet where
I record my Doings, Thoughts and Writing.
'''
COPYRIGHT = '©2024'
THEME = 'theme/Papyrus'
THEME_STATIC_PATHS = ['static']

DISPLAY_PAGES_ON_MENU = True
DIRECT_TEMPLATES = (('index', 'search', 'tags', 'categories', 'archives',))
PAGINATED_TEMPLATES = {'index':None,'tag':None,'category':None,'author':None,'archives':24,}


# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Social widgets
SOCIAL = (
    ('github', 'https://github.com/netzro'),
    ('twitter', 'https://twitter.com/gifted_99'),
)


DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True