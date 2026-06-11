import pandas as pd
from urlextract import URLExtract
from collections import Counter
import emoji
import matplotlib.pyplot as plt
from textblob import TextBlob
from wordcloud import STOPWORDS
import re

extract = URLExtract()

# =========================
# 🔹 1. Basic Stats
# =========================
def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # messages
    # remove system messages
    df = df[df['user'] != 'group_notification']

    # filter user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]

    # words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # links
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return {
        "messages": num_messages,
        "words": len(words),
        "media": num_media_messages,
        "links": len(links)
    }


# =========================
# 🔹 2. Most Active Users
# =========================
def most_busy_users(df):
    x = df['user'].value_counts().head()
    df_percent = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index()
    df_percent.columns = ['name', 'percent']
    return x, df_percent


# =========================
# 🔹 3. WordCloud
# =========================
# from wordcloud import WordCloud

# def create_wordcloud(selected_user, df):

#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
#     df_wc = wc.generate(df['message'].str.cat(sep=" "))
#     return df_wc

from wordcloud import WordCloud, STOPWORDS

def create_wordcloud(selected_user, df):

    # filter user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # ❌ REMOVE group notifications
    df = df[df['user'] != 'group_notification']

    # ❌ REMOVE media messages
    df = df[~df['message'].str.contains('<Media omitted>', case=False, na=False)]

    # ❌ REMOVE extra noise (VERY IMPORTANT)
    df = df[df['message'].str.len() > 2]

    # 🔥 REMOVE common useless words
    stopwords = set(STOPWORDS)

    # Add custom stopwords
    custom_words = [
        'media', 'omitted', 'message', 'deleted',
        'http', 'https', 'www', 'com'
    ]
    stopwords.update(custom_words)

    wc = WordCloud(
        width=600,
        height=600,
        min_font_size=10,
        background_color='white',
        stopwords=stopwords
    )

    text = df['message'].str.cat(sep=" ")
    df_wc = wc.generate(text)

    return df_wc


# =========================
# 🔹 4. Most Common Words
# =========================
# def most_common_words(selected_user, df):

#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]
    
#     df = df[df['message'] != '<Media omitted>']

#     words = []

#     for message in df['message']:
#         for word in message.lower().split():
#             words.append(word)

#     common_df = pd.DataFrame(Counter(words).most_common(20))
#     return common_df

def most_common_words(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # remove notifications
    df = df[df['user'] != 'group_notification']

    # remove media messages
    df = df[~df['message'].str.contains('<Media omitted>', na=False)]

    stopwords = set(STOPWORDS)

    # custom stopwords
    stopwords.update([
        'media', 'omitted', 'message', 'deleted',
        'http', 'https', 'www', 'com',
        'the', 'and', 'for', 'are', 'was',
        'will', 'your', 'you', 'all', 'this',
        'that', 'have', 'with', 'from'
    ])

    words = []

    for message in df['message']:

        # remove punctuation
        message = re.sub(r'[^\w\s]', '', str(message).lower())

        for word in message.split():

            if (
                word not in stopwords
                and len(word) > 2
                and not word.isnumeric()
            ):
                words.append(word)

    common_df = pd.DataFrame(
        Counter(words).most_common(20),
        columns=['Word', 'Count']
    )

    return common_df


# =========================
# 🔹 5. Emoji Analysis
# =========================
def emoji_helper(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # remove system + media messages
    df = df[(df['user'] != 'group_notification') & (df['message'] != '<Media omitted>')]

    emojis = []

    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(
        Counter(emojis).most_common(),
        columns=['Emoji', 'Count']
    )

    return emoji_df

# =========================
# 🔹 6. Monthly Timeline
# =========================
def monthly_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


# =========================
# 🔹 7. Daily Timeline
# =========================
def daily_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily = df.groupby('date').count()['message'].reset_index()
    return daily
# week day timeline
def week_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # count messages per day name
    return df['day_name'].value_counts()


# =========================
# 🔹 8. Week Activity Map
# =========================
def week_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


# =========================
# 🔹 9. Month Activity Map
# =========================
def month_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

# activity heatmap
# def activity_heatmap(selected_user, df):

#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     heatmap = df.pivot_table(
#         index='day_name',
#         columns='hour',
#         values='message',
#         aggfunc='count'
#     ).fillna(0)

#     #
#     heatmap = heatmap.reindex([
#         'Monday', 'Tuesday', 'Wednesday',
#         'Thursday', 'Friday', 'Saturday', 'Sunday'
#     ])

#     return heatmap

def activity_heatmap(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # remove group notifications
    df = df[df['user'] != 'group_notification']

    # create day_name and hour
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour

    # create pivot
    heatmap = df.pivot_table(
        index='day_name',
        columns='hour',
        values='message',
        aggfunc='count'
    )

    # 🔥 FIX 1: ensure all hours 0–23 exist
    all_hours = list(range(24))
    heatmap = heatmap.reindex(columns=all_hours, fill_value=0)

    # 🔥 FIX 2: ensure all days in order
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap = heatmap.reindex(days)
    heatmap = heatmap.fillna(0)
    return heatmap

# def response_time_analysis(df):

#     # sort by time
#     df = df.sort_values(by='date')

#     # remove group notifications
#     df = df[df['user'] != 'group_notification']

#     # shift user and time
#     df['prev_user'] = df['user'].shift(1)
#     df['prev_time'] = df['date'].shift(1)

#     # calculate time difference (in minutes)
#     df['response_time'] = (df['date'] - df['prev_time']).dt.total_seconds() / 60

#     # only consider replies (user changes)
#     df = df[df['user'] != df['prev_user']]

#     # remove large gaps (like overnight chats)
#     df = df[df['response_time'] < 1440]  # less than 24 hrs

#     # average response time per user
#     response_df = df.groupby('user')['response_time'].mean().reset_index()

#     response_df.rename(columns={'response_time': 'avg_response_time'}, inplace=True)

#     # sort → fastest first
#     response_df = response_df.sort_values(by='avg_response_time')

#     return response_df
import pandas as pd

def response_time_analysis(selected_user, df):

    # remove group notifications
    df = df[df['user'] != 'group_notification']

    # sort by time
    df = df.sort_values(by='date')

    # previous message info
    df['prev_user'] = df['user'].shift()
    df['prev_date'] = df['date'].shift()

    # calculate response time (in minutes)
    df['response_time'] = (df['date'] - df['prev_date']).dt.total_seconds() / 60

    # keep only replies (user changes)
    df = df[df['user'] != df['prev_user']]

    # remove unrealistic gaps (optional but important)
    df = df[df['response_time'] < 60*24]  # < 1 day

    # 
    # 
    #
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # group and calculate average
    response_df = df.groupby('user')['response_time'].mean().reset_index()

    response_df.rename(columns={'response_time': 'avg_response_time'}, inplace=True)

    # sort (fastest first)
    response_df = response_df.sort_values(by='avg_response_time')

    return response_df

    # sentiment analysis

def sentiment_analysis(selected_user, df):

    # filter user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # remove group notifications
    df = df[df['user'] != 'group_notification']

    sentiments = []

    for message in df['message']:
        polarity = TextBlob(message).sentiment.polarity

        if polarity > 0:
            sentiments.append('Positive')
        elif polarity < 0:
            sentiments.append('Negative')
        else:
            sentiments.append('Neutral')

    df['sentiment'] = sentiments

    sentiment_counts = df['sentiment'].value_counts().reset_index()
    sentiment_counts.columns = ['Sentiment', 'Count']

    return sentiment_counts
