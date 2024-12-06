"""
Copyright @emontj 2024
"""

import os

import pandas as pd
from openai import OpenAI

def read_table(engine, table_name) -> pd.DataFrame:
    return pd.read_sql(f'SELECT * FROM {table_name}', con=engine, index_col='index')

def analyze_all_rows(df, limit = float('inf')):
    results_df = None

    for index, row in df.iterrows():
        if limit > index:
            row_dict = row.to_dict()
            analysis_df = analyze_dict(row_dict)

            if results_df is None:
                results_df = analysis_df
            else:
                results_df = pd.concat([results_df, analysis_df], ignore_index=True)
        else:
            print('Analysis limit reached')
            break

    return results_df

def analyze_dict(row_dict) -> pd.DataFrame:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    prompt = f'''
        Assess the title and summary of this article, and extract the topic and any well-known individuals involved in the article.
        Use First and Last name for individuals regardless of how they are referenced in the article data.

        Output format:
        Topic: <insert topic here, singular>
        Individuals: <insert individuals identified in the information, comma seperated>
        Sentiment: <choose between Positive, Neutral and Negative>

        Input:
        Article Title: {row_dict['title']}
        Article Summary: {row_dict['summary']}
    '''

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an intelligent assistant that determines characteristics about data"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.0
    )

    message = str(completion.choices[0].message.content)

    message_parts = message.split('\n')
    message_parts = [part.strip() for part in message_parts]
    message_parts = [part.lower() for part in message_parts]
    message_parts = {part.split(': ', 1)[0] : part.split(': ', 1)[1] for part in message_parts}
    message_parts['hashed_title'] = row_dict['hashed_title']

    return pd.DataFrame([message_parts])

def run_analysis(sql_engine, limit = float('inf')):
    stored_df = read_table(sql_engine, 'news_rss')
    # TODO: some kind of logic to determine what has been previously analyzed
    analyzed_df = analyze_all_rows(stored_df, limit = limit)

    if sql_engine:
        analyzed_df.to_sql('analyzed_rss', sql_engine, if_exists='replace') # TODO: use add rows without duplicates method

    return analyzed_df

if __name__ == '__main__':
    analyze_dict(
        {
            'title' : 'test concept',
            'summary' : 'test summary',
        }
    )