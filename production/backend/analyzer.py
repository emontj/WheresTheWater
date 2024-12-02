import os

import pandas as pd
from openai import OpenAI

def read_table(engine, table_name) -> pd.DataFrame:
    return pd.read_sql(f'SELECT * FROM {table_name}', con=engine, index_col='index')

def analyze_all_rows(df):
    results_df = None

    for index, row in df.iterrows():
        analysis_df = analyze_dict(row.to_dict())

        if results_df is None:
            results_df = analysis_df
        else:
            results_df = pd.concat([results_df, analysis_df], ignore_index=True)

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
        ]
    )

    message = str(completion.choices[0].message.content)
    print(message)



def run_analysis(engine):
    df = read_table(engine, 'news_rss')
    analyze_all_rows(df)

if __name__ == '__main__':
    analyze_dict(
        {
            'title' : 'test concept',
            'summary' : 'test summary',
        }
    )