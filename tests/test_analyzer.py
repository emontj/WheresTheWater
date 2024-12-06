"""
Copyright @emontj 2024
"""

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from production.backend.analyzer import *

class TestAnalyzer(unittest.TestCase):

    def setUp(self):
        # Sample DataFrame for testing
        self.sample_df = pd.DataFrame({
            'title': ['Test Title 1', 'Test Title 2'],
            'summary': ['Summary 1', 'Summary 2'],
            'hashed_title': ['hash1', 'hash2']
        })

    @patch('production.backend.analyzer.OpenAI')
    def test_analyze_dict(self, mock_openai):
        # Mock OpenAI client and response
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.return_value = {
            "choices": [
                {
                    "message": {
                        "content": """
                        Topic: Politics
                        Individuals: John Doe
                        Sentiment: Neutral
                        """
                    }
                }
            ]
        }

        row_dict = {
            'title': 'Test Title',
            'summary': 'Test Summary',
            'hashed_title': 'hash1'
        }

        result_df = analyze_dict(row_dict)

        # Check DataFrame contents
        self.assertEqual(result_df.iloc[0]['topic'], 'politics')
        self.assertEqual(result_df.iloc[0]['individuals'], 'john doe, jane smith')
        self.assertEqual(result_df.iloc[0]['sentiment'], 'neutral')
        self.assertEqual(result_df.iloc[0]['hashed_title'], 'hash1')

    @patch('production.backend.analyzer.analyze_dict')
    def test_analyze_all_rows(self, mock_analyze_dict):
        # Mock analyze_dict to return a DataFrame
        mock_analyze_dict.return_value = pd.DataFrame([{
            'topic': 'politics',
            'individuals': 'john doe',
            'sentiment': 'neutral',
            'hashed_title': 'hash1'
        }])

        result_df = analyze_all_rows(self.sample_df, limit=1)

        # Check the length of the resulting DataFrame
        self.assertEqual(len(result_df), 1)
        self.assertEqual(result_df.iloc[0]['topic'], 'politics')

    @patch('production.backend.analyzer.pd.read_sql')
    def test_read_table(self, mock_read_sql):
        # Mock SQL read operation
        mock_read_sql.return_value = self.sample_df
        mock_engine = MagicMock()

        df = read_table(mock_engine, 'news_rss')

        # Validate returned DataFrame
        self.assertEqual(len(df), 2)
        self.assertEqual(df.columns.tolist(), ['title', 'summary', 'hashed_title'])

if __name__ == '__main__':
    unittest.main()
