from urlextract import URLExtract
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from collections import Counter
import emoji
import pandas as pd

extractor = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]

    words = []
    for message in df['message']:
        words.extend(message.split())

    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df_percent = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index()
    df_percent.columns = ['name', 'percent']
    return x, df_percent

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def clean_text(text):
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        return text

    temp['message'] = temp['message'].apply(clean_text)
    all_words = ' '.join(temp['message'])
    word_counts = Counter(all_words.split())
    wordcloud = WordCloud(width=500, height=500, min_font_size=10, background_color='white').generate_from_frequencies(word_counts)
    return wordcloud

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))), columns=['emoji', 'count'])
    return emoji_df

def most_common_words(selected_user, df, top_n=10):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def clean_text(text):
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        return text

    temp['message'] = temp['message'].apply(clean_text)
    all_words = ' '.join(temp['message'])
    word_counts = Counter(all_words.split())
    most_common = word_counts.most_common(top_n)
    common_words_df = pd.DataFrame(most_common, columns=["Word", "Frequency"])
    return common_words_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df['month'] = df['date'].dt.to_period('M').astype(str)
    timeline = df.groupby('month').size().reset_index(name='message')
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df['only_date'] = df['date'].dt.date
    daily_timeline = df.groupby('only_date').size().reset_index(name='message')
    return daily_timeline

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df['hour'] = df['date'].dt.hour
    df['day'] = df['date'].dt.dayofweek
    heatmap_data = df.pivot_table(index='day', columns='hour', values='message', aggfunc='count').fillna(0)
    return heatmap_data

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['date'].dt.day_name().value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['date'].dt.month_name().value_counts()
