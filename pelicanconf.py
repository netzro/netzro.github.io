AUTHOR = 'Gifted'
SITENAME = 'Gifted Space'
SITEURL = ""
PATH = "content"
TIMEZONE = 'Africa/Lagos'
DEFAULT_LANG = 'en'

SUBTITLE = 'Papyrus'
SUBTEXT = '''A fast and responsive theme built for the <a class="underline" 
href="https://blog.getpelican.com/">Pelican</a> site generator.<br>
The theme is inspired from <a class="underline" 
href="https://github.com/adityatelange/hugo-PaperMod">Hugo-PaperMod</a>. 
It is styled using <a class="underline" 
href="https://tailwindcss.com/">Tailwind CSS</a>. 
It supports dark mode and built in search function.
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

# Blogroll
LINKS = (
    ("Pelican", "https://getpelican.com/"),
    ("Python.org", "https://www.python.org/"),
    ("Jinja2", "https://palletsprojects.com/p/jinja/"),
    ("You can modify those links in your config file", "#"),
)

# Social widgets
SOCIAL = (
    ('github', 'https://github.com/netzro'),
    ('twitter', 'https://twitter.com/gifted_99'),
)


DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True