import pandas as pd
import matplotlib.pyplot as plt
import ast

def drop_row(t):
    if 'Lufthansa' in t and 'KLM' in t:
        return 'Lufthansa,KLM'
    elif 'KLM' in t:
        return 'KLM'
    elif 'Lufthansa' in t:
        return 'Lufthansa'
    else:
        return 'other airline'
tweets_df = pd.read_csv(r"complete_data_with_vader.csv", usecols=['id_str', 'year_tweet', 'month_tweet', 'day_tweet', 'entity_user_mentions', 'Vader_com'], encoding='latin-1')
#vader_df = pd.read_csv(r"C:\Users\20223661\OneDrive - TU Eindhoven\Documents\Git\DBL 18\Di, Tri Diagrams\dbl-data-challenge-Files\dbl-data-challenge-Files\vader.csv", encoding='latin-1')
subjectivity_df = pd.read_csv(r"text_blob_update.csv", encoding='latin-1')

# Merge on the tweet ID
merged_df = tweets_df
merged_df = pd.merge(merged_df, subjectivity_df, left_on='id_str', right_on='tweet_id')

# Making a date column
merged_df['date'] = merged_df[['year_tweet', 'month_tweet', 'day_tweet']].astype(str).agg('-'.join, axis=1)
merged_df['date'] = pd.to_datetime(merged_df['date'], errors='coerce')

# Dropping the columns that we don't need
merged_df.drop(['year_tweet', 'month_tweet', 'day_tweet', 'tweet_id', 'full_text', 'polarity'], axis=1, inplace=True)
merged_df['entity_user_mentions'] = merged_df['entity_user_mentions'].apply(drop_row) # Airline to ID dictionary
airline_user_ids = ['KLM', 'Lufthansa']

# Filter tweets that mention airline
mention_airline_KLM = merged_df[merged_df['entity_user_mentions'] == 'KLM']
mention_airline_KLM.dropna(axis=0, how='any', inplace=True)
mention_airline_Luf = merged_df[merged_df['entity_user_mentions'] == 'Lufthansa']
mention_airline_Luf.dropna(axis=0, how='any', inplace=True)



# This where insert the date
start_date = pd.to_datetime('2019-12-17')
end_date = pd.to_datetime('2019-12-21')
filtered_df = mention_airline_KLM[(mention_airline_KLM['date'] >= start_date) & (mention_airline_KLM['date'] <= end_date)]
grouped_vader = filtered_df['Vader_com'].groupby(filtered_df['date']).mean()
grouped_subjectivity = filtered_df['subjectivity'].groupby(filtered_df['date']).mean()

#Plot the sentiment and subjectivity change over time
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(grouped_vader.index, grouped_vader, label='Sentiment')
ax.plot(grouped_subjectivity.index, grouped_subjectivity, label='Subjectivity')
ax.set_xlabel('Date')
ax.set_ylabel('Score')
ax.set_title('KLM(strikes occur on 18,19)')
ax.legend()
plt.xticks(rotation=45)
plt.savefig(fname = 'KLM(Dec)',dpi=200)






