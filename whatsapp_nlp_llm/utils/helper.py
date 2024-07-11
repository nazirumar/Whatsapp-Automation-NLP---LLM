from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import string
import re
import emoji

extract = URLExtract()
stop_word = r'C:\Users\Nazbeen-Ai\Documents\My Projects\Machine Learning Projects\Whatsapp Automation NLP & LLM\stop_words.txt'

def fetch_stats(selected_User, df):
    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_messages,len(links)

#func will only work in group chat analysis
def most_busy_Users(df):
    x = df['User'].value_counts().head()
    df = round((df['User'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'User': 'percent'})
    return x,df

def remove_stop_words(message):
    y = []
    for word in message.lower().split():
        if word not in stop_word:
            y.append(word)
    return " ".join(y)

def remove_punctuation(message):
  x = re.sub('[%s]'% re.escape(string.punctuation), '', message)
  return x

def create_wordcloud(selected_User,df):
    if selected_User != 'Overall':
        df = df[df['User'] == selected_User]

    temp = df[df['User'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp['message'] = temp['message'].apply(remove_stop_words)
    temp['message'] = temp['message'].apply(remove_punctuation)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_User,df):
    if selected_User != 'Overall':
        df = df[df['User'] == selected_User]

    temp = df[df['User'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp['message'] = temp['message'].apply(remove_stop_words)
    temp['message'] = temp['message'].apply(remove_punctuation)
    words = []

    for message in temp['message']:
        words.extend(message.split())

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_User, df):
    if selected_User != 'Overall':
        df = df[df['User'] == selected_User]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_User,df):
    if selected_User != 'Overall':
        df = df[df['User'] == selected_User]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    month_timeline = []
    for i in range(timeline.shape[0]):
        month_timeline.append(timeline['month'][i]+"-"+str(timeline['year'][i]))

    timeline['time'] = month_timeline
    return timeline

def daily_timeline(selected_User,df):
    if selected_User != 'Overall':
        df = df[df['User'] == selected_User]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_User,df):
    if selected_User != 'Overall':
        df = df[df['User'] == selected_User]
    return df['day_name'].value_counts()

def month_activity_map(selected_User,df):
    if selected_User != 'Overall':
        df = df[df['User'] == selected_User]
    return df['month'].value_counts()

def activity_heatmap(selected_User,df):
    if selected_User != 'Overall':
        df = df[df['User'] == selected_User]

    User_heatmap = df.pivot_table(index='day_name', columns='period', 
                values='message', aggfunc='count').fillna(0)
    return User_heatmap