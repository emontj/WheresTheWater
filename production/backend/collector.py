"""
Copyright @emontj 2024
"""

import feedparser
import pandas as pd
import hashlib

# TODO: Load sources from database
NEWS_SOURCES = {
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

def fetch_rss_for_outlet(outlet, news_sources, category=None):
    """
    Fetches RSS feeds for a specific news outlet or category.

    Args:
        outlet (str): The name of the news outlet.
        category (str, optional): Specific category to fetch. Defaults to None.

    Returns:
        dict: Parsed RSS feeds for the specified outlet/category.
    """
    if outlet not in news_sources:
        raise ValueError(f"Outlet '{outlet}' not found in news sources.")
    
    links = news_sources[outlet]["links"]
    feeds = {}

    if category:
        if category not in links:
            raise ValueError(f"Category '{category}' not found for outlet '{outlet}'.")
        feeds[category] = feedparser.parse(links[category])
    else:
        for topic, link in links.items():
            feeds[topic] = feedparser.parse(link)

    feeds['outlet'] = outlet

    return feeds

def rss_to_dataframe(entries, mapping):
    """
    Converts a list of RSS feed entries into a standardized pandas DataFrame using the provided mapping.

    Args:
        entries (list): List of RSS feed entries (parsed by feedparser).
        mapping (dict): The mapping dictionary for the RSS fields.

    Returns:
        pd.DataFrame: A pandas DataFrame with standardized columns.
    """
    standardized_items = []

    for entry in entries:
        # Apply mapping to standardize fields
        standardized_item = {
            "title": entry.get(mapping.get("title", None), None),
            "link": entry.get(mapping.get("link", None), None),
            "summary": entry.get(mapping.get("summary", None), None),
            "published": entry.get(mapping.get("published", None), None),
            "updated": entry.get(mapping.get("updated", None), None),
            "tags": [tag.get("term", None) for tag in entry.get(mapping.get("tags", None), [])] if mapping.get("tags") else None,
            "media_content": entry.get(mapping.get("media_content", None), None),
            "content": entry.get(mapping.get("content", None), None),
            "authors": entry.get(mapping.get("authors", None), None),
            "id": entry.get(mapping.get("id", None), None),
        }
        standardized_items.append(standardized_item)

    # Convert the list of standardized items into a pandas DataFrame
    df = pd.DataFrame(standardized_items)
    return df


def extract_all_entries(feed, news_sources):
    running_df = None

    for k, v in feed.items():
        if k != 'outlet':
            new_df = rss_to_dataframe(v['entries'], news_sources[feed['outlet']]['mapping'])

            if running_df is None:
                running_df = new_df
            else:
                running_df = pd.concat([running_df, new_df], ignore_index=True)
    
    return running_df

def print_rss_structure(feed_parsed, outlet = 'Unspecified'):
    print(outlet, ':', list(feed_parsed['entries'][0].keys()))

def add_hashed_column(df, column_name, hash_column_name):
    """
    Adds a new column with SHA-256 hashed values of an existing column.
    Converts None/NaN values to the string 'None' for consistent hashing.
    
    Parameters:
    - df: pandas.DataFrame - The DataFrame to modify.
    - column_name: str - The name of the column to hash.
    - hash_column_name: str - The name of the new column for hashed values.
    
    Returns:
    - pandas.DataFrame - DataFrame with the new hashed column.
    """
    def hash_value(val):
        val = "None" if pd.isna(val) else str(val)
        return hashlib.sha256(val.encode()).hexdigest()

    df[hash_column_name] = df[column_name].apply(hash_value)
    return df

def update_data(news_sources):
    running_df = None

    for k, v in news_sources.items():
        feed = fetch_rss_for_outlet(k, news_sources)
        new_df = extract_all_entries(feed, news_sources)

        if running_df is None:
            running_df = new_df
        else:
            running_df = pd.concat([running_df, new_df], ignore_index=True)
    
    # add_hashed_column(running_df, 'title', 'hashed_title')
    
    # TODO: write to SQL
    

if __name__ == "__main__":
    update_data(NEWS_SOURCES)
