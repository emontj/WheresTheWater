"""
Copyright @emontj 2024
"""

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import hashlib
from production.backend.collector import *

class TestNewsRSSFunctions(unittest.TestCase):

    def setUp(self):
        # Sample RSS feed data for testing
        self.sample_feed = {
            'entries': [
                {
                    'title': 'Test Title 1',
                    'link': 'http://example.com/article1',
                    'summary': 'Test Summary 1',
                    'published': '2024-12-01',
                    'id': 'unique-id-1',
                    'tags': [{'term': 'tag1'}, {'term': 'tag2'}],
                },
                {
                    'title': 'Test Title 2',
                    'link': 'http://example.com/article2',
                    'summary': 'Test Summary 2',
                    'published': '2024-12-02',
                    'id': 'unique-id-2',
                    'tags': [{'term': 'tag3'}, {'term': 'tag4'}],
                },
            ]
        }

        self.sample_mapping = {
            'title': 'title',
            'link': 'link',
            'summary': 'summary',
            'published': 'published',
            'tags': 'tags',
            'id': 'id'
        }

    def test_rss_to_dataframe(self):
        # Test converting RSS entries to DataFrame
        df = rss_to_dataframe(self.sample_feed['entries'], self.sample_mapping)
        self.assertEqual(len(df), 2)  # Check row count
        self.assertListEqual(
            df.columns.tolist(),
            ['title', 'link', 'summary', 'published', 'updated', 'tags', 'media_content', 'content', 'authors', 'id']
        )  # Check columns
        self.assertEqual(df['title'].iloc[0], 'Test Title 1')  # Check data

    def test_fetch_rss_for_outlet_invalid_outlet(self):
        with self.assertRaises(ValueError):
            fetch_rss_for_outlet('Invalid Outlet', TEST_NEWS_SOURCES)

    @patch('feedparser.parse')
    def test_fetch_rss_for_outlet_valid_outlet(self, mock_parse):
        mock_parse.return_value = self.sample_feed
        feeds = fetch_rss_for_outlet('CNN', TEST_NEWS_SOURCES)
        self.assertIn('politics', feeds)  # Ensure category is parsed
        self.assertEqual(feeds['outlet'], 'CNN')  # Check outlet name

    def test_add_hashed_column(self):
        # Test adding a hashed column
        df = pd.DataFrame({'title': ['Article 1', 'Article 2', None]})
        df = add_hashed_column(df, 'title', 'hashed_title')
        self.assertIn('hashed_title', df.columns)  # Check new column exists
        self.assertEqual(
            df['hashed_title'].iloc[0],
            hashlib.sha256('Article 1'.encode()).hexdigest()
        )  # Check hash of first article
        self.assertEqual(
            df['hashed_title'].iloc[2],
            hashlib.sha256('None'.encode()).hexdigest()
        )  # Check hash of None value

    def test_prepare_dataframe_for_sql(self):
        # Test preparing DataFrame for SQL insertion
        df = pd.DataFrame({
            'title': ['Article 1', None],
            'published': [pd.Timestamp('2024-12-01'), None]
        })
        prepared_df = prepare_dataframe_for_sql(df)
        self.assertEqual(prepared_df['title'].iloc[0], 'Article 1')  # Check string conversion
        self.assertEqual(prepared_df['title'].iloc[1], None)  # Check None value
        self.assertEqual(prepared_df['published'].iloc[0], '2024-12-01 00:00:00')  # Check datetime conversion

    @patch('sqlalchemy.engine.Engine.connect')
    def test_add_rows_without_duplicates(self, mock_connect):
        # Test adding rows without duplicates
        mock_engine = MagicMock()
        df = pd.DataFrame({
            'id': ['id1', 'id2'],
            'title': ['Article 1', 'Article 2']
        })
        add_rows_without_duplicates(df, mock_engine, 'test_table', ['id'])
        self.assertTrue(mock_connect.called)  # Ensure connection was used

    def test_extract_all_entries(self):
        # Test extracting all entries from feed
        feed = {'politics': self.sample_feed, 'outlet': 'CNN'}
        df = extract_all_entries(feed, TEST_NEWS_SOURCES)
        self.assertEqual(len(df), 2)
        self.assertIn('title', df.columns)

if __name__ == '__main__':
    unittest.main()
