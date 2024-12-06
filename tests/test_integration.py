"""
Copyright @emontj 2024
"""

import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
import pandas as pd
from production.backend.collector import update_data
from production.backend.analyzer import run_analysis

class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        self.news_sources = {
            "TestSource": {
                "links": {
                    "politics": "http://example.com/rss"
                },
                "mapping": {
                    "title": "title",
                    "link": "link",
                    "summary": "summary",
                    "published": "published",
                    "id": "id",
                },
            }
        }

        self.sample_feed = {
            'entries': [
                {
                    'title': 'Test Title 1',
                    'link': 'http://example.com/article1',
                    'summary': 'Test Summary 1',
                    'published': '2024-12-01',
                    'id': 'unique-id-1',
                },
                {
                    'title': 'Test Title 2',
                    'link': 'http://example.com/article2',
                    'summary': 'Test Summary 2',
                    'published': '2024-12-02',
                    'id': 'unique-id-2',
                },
            ]
        }

    @patch('production.backend.collector.feedparser.parse')
    @patch('production.backend.analyzer.OpenAI')
    def test_full_workflow(self, mock_openai, mock_feedparser):
        mock_feedparser.return_value = self.sample_feed

        mock_openai_client = MagicMock()
        mock_openai.return_value = mock_openai_client
        mock_openai_client.chat.completions.create.side_effect = [
            {
                "choices": [
                    {"message": {"content": """
                    Topic: Politics
                    Individuals: John Doe
                    Sentiment: Positive
                    """}}
                ]
            },
            {
                "choices": [
                    {"message": {"content": """
                    Topic: Technology
                    Individuals: Jane Smith
                    Sentiment: Neutral
                    """}}
                ]
            }
        ]

        update_data(self.news_sources, sql_engine=self.engine)

        stored_df = pd.read_sql('SELECT * FROM news_rss', self.engine)
        self.assertEqual(len(stored_df), 2)
        self.assertIn('Test Title 1', stored_df['title'].values)

        analyzed_df = run_analysis(self.engine, limit=2)

        self.assertEqual(len(analyzed_df), 2)
        self.assertEqual(analyzed_df.iloc[0]['topic'], 'politics')
        self.assertEqual(analyzed_df.iloc[1]['individuals'], 'jane smith')

    def tearDown(self):
        self.engine.dispose()

if __name__ == '__main__':
    unittest.main()
