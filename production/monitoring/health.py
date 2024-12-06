import requests
from sqlalchemy import create_engine
import feedparser

class ReadinessChecks:
    @staticmethod
    def check_database(engine):
        """
        Check if the database is reachable.
        """
        try:
            with engine.connect() as connection:
                connection.execute("SELECT 1")
            return True, "Database is reachable"
        except Exception as e:
            return False, f"Database error: {e}"

    @staticmethod
    def check_gpt_api(api_url, api_key):
        """
        Check if the GPT API is reachable.
        """
        try:
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get(api_url, headers=headers, timeout=5)
            if response.status_code == 200:
                return True, "GPT API is reachable"
            else:
                return False, f"GPT API returned status code {response.status_code}"
        except Exception as e:
            return False, f"GPT API error: {e}"

    @staticmethod
    def check_rss_feed(feed_url):
        """
        Check if the RSS feed is reachable and parsable.
        """
        try:
            feed = feedparser.parse(feed_url)
            if feed.bozo == 0:  # Check if feed parsed without errors
                return True, "RSS feed is reachable and parsable"
            else:
                return False, f"RSS feed parsing error: {feed.bozo_exception}"
        except Exception as e:
            return False, f"RSS feed error: {e}"
