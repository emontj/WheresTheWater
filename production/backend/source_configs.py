"""
Copyright @emontj 2024
"""

PRODUCTION_NEWS_SOURCES = {
    "CNN": {
        "links": {
            "politics": "http://rss.cnn.com/rss/cnn_allpolitics.rss",
        },
        "mapping": {
            "title": "title",                        # Title of the article
            "link": "link",                         # Article link
            "summary": "summary",                   # Short description or summary
            "published": "published",               # Publication date
            "updated": None,                        # Last update time (not available)
            "tags": None,                           # Tags/categories (not available)
            "media_content": "media_content",       # Media content URL, if available
            "content": None,                        # Full content (not available)
            "authors": None,                        # List of authors (not available)
            "id": "id",                             # Unique ID or GUID
        },
    },
    "Fox News": {
        "links": {
            "politics": "https://feeds.foxnews.com/foxnews/politics",
        },
        "mapping": {
            "title": "title",                        # Title of the article
            "link": "link",                         # Article link
            "summary": "summary",                   # Short description or summary
            "published": "published",               # Publication date
            "updated": None,                        # Last update time (not available)
            "tags": "tags",                         # Tags/categories
            "media_content": "media_content",       # Media content URL
            "content": "content",                   # Full content
            "authors": None,                        # List of authors (not available)
            "id": "id",                             # Unique ID or GUID
        },
    },
    "Washington Post": {
        "links": {
            "politics": "http://feeds.washingtonpost.com/rss/politics",
        },
        "mapping": {
            "title": "title",                        # Title of the article
            "link": "link",                         # Article link
            "summary": "summary",                   # Short description or summary
            "published": "published",               # Publication date
            "updated": None,                        # Last update time (not available)
            "tags": None,                           # Tags/categories (not available)
            "media_content": None,                  # Media content URL (not available)
            "content": None,                        # Full content (not available)
            "authors": "authors",                   # List of authors
            "id": "id",                             # Unique ID or GUID
        },
    },
    "NYT": {
        "links": {
            "politics": "https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml",
        },
        "mapping": {
            "title": "title",                        # Title of the article
            "link": "link",                         # Article link
            "summary": "summary",                   # Short description or summary
            "published": "published",               # Publication date
            "updated": None,                        # Last update time (not available)
            "tags": "tags",                         # Tags/categories
            "media_content": "media_content",       # Media content URL
            "content": "content",                   # Full content
            "authors": None,                        # List of authors (not available)
            "id": "id",                             # Unique ID or GUID
        },
    },
    "Guardian": {
        "links": {
            "politics": "https://www.theguardian.com/politics/rss",
        },
        "mapping": {
            "title": "title",                        # Title of the article
            "link": "link",                         # Article link
            "summary": "summary",                   # Short description or summary
            "published": "published",               # Publication date
            "updated": "updated",                   # Last update time
            "tags": "tags",                         # Tags/categories
            "media_content": "media_content",       # Media content URL
            "content": None,                        # Full content (not available)
            "authors": "authors",                   # List of authors
            "id": "id",                             # Unique ID or GUID
        },
    },
}
