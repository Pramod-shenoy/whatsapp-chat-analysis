from urlextract import URLExtract
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from collections import Counter
import emoji  # Ensure you import the emoji module
import pandas as pd

# Initialize URL extractor
extractor = URLExtract()


# Function to fetch statistics: number of messages, words, media messages, and links
def fetch_stats(selected_user, df):
    # Filter by selected user if not 'Overall'
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Number of messages
    num_messages = df.shape[0]

    # Total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # Number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # Number of links shared
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


# Function to get the most busy users (group level analysis)
def most_busy_users(df):
    x = df['user'].value_counts().head()
    df_percent = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index()
    df_percent.columns = ['name', 'percent']
    return x, df_percent


# Function to create a word cloud from messages
def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Filter out group notifications and media messages
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    # Clean the text (remove non-alphabetical characters)
    def clean_text(text):
        text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove numbers and special characters
        return text

    temp['message'] = temp['message'].apply(clean_text)

    # Combine all messages into one large text
    all_words = ' '.join(temp['message'])

    # Create a Counter object to count word frequencies
    word_counts = Counter(all_words.split())

    # Create a word cloud from the most common words
    wordcloud = WordCloud(background_color='white').generate_from_frequencies(word_counts)

    # Return the WordCloud as an image (numpy array)
    return wordcloud.to_array()  # This is the fix


# Function to extract and count emojis from messages
def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df


# Function to find the most common words used in messages
def most_common_words(selected_user, df, top_n=10):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Filter out group notifications and media messages
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    # Clean the text (remove non-alphabetical characters)
    def clean_text(text):
        text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove numbers and special characters
        return text

    temp['message'] = temp['message'].apply(clean_text)

    # Combine all messages into one large text
    all_words = ' '.join(temp['message'])

    # Create a Counter object to count word frequencies
    word_counts = Counter(all_words.split())

    # Get the most common words
    most_common = word_counts.most_common(top_n)

    # Return a DataFrame with the most common words and their counts
    common_words_df = pd.DataFrame(most_common, columns=["Word", "Frequency"])
    return common_words_df


# Function to get the monthly message timeline
def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Extract month from the 'date' column (assuming you have a 'date' column)
    df['month'] = df['date'].dt.month
    timeline = df.groupby('month').size().reset_index(name='message')

    return timeline


# Function to get the daily message timeline
def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Extract date (ignoring the time part)
    df['only_date'] = df['date'].dt.date
    daily_timeline = df.groupby('only_date').size().reset_index(name='message')

    return daily_timeline


# Function to get activity heatmap (weekly), based on day of the week and hour of the day
def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Create a pivot table for heatmap, this assumes you have 'date' and 'hour' columns
    df['hour'] = df['date'].dt.hour
    df['day'] = df['date'].dt.dayofweek  # Monday=0, Sunday=6
    heatmap_data = df.pivot_table(index='day', columns='hour', values='message', aggfunc='count').fillna(0)

    return heatmap_data


def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Monday = 0, Sunday = 6
    return df['date'].dt.day_name().value_counts()


def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['date'].dt.month_name().value_counts()
