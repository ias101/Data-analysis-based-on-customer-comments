import pandas as pd
import matplotlib.pyplot as plt

name = ['index','tweet_created_at ', 'id_str','entity_user_mentions ','con_id_str_list ','con_id_str_list1 ','con_id_str_list2 ','full_conversation_ids',
        'airline_contain_con','airline_contain_con_time','airline_reply_time','minus']
tweets_df = pd.read_csv(r"complete_data_with_vader.csv",
                        usecols=['id_str', 'year_tweet', 'month_tweet', 'day_tweet'],
                        encoding='latin-1')
time_KLM = pd.read_csv(r"KLM.csv", encoding='latin-1')
time_LUF = pd.read_csv(r"LUF.csv", encoding='latin-1')
time_KLM.columns = name
time_LUF.columns = ['index','tweet_created_at ', 'id_str','entity_user_mentions ','con_id_str_list ','con_id_str_list1 ','full_conversation_ids',
        'airline_contain_con','airline_contain_con_time','airline_reply_time','minus']
#Merge on the tweet ID

merged_KLM = pd.merge(time_KLM, tweets_df, left_on='id_str', right_on='id_str')
merged_LUF = pd.merge(time_LUF, tweets_df, left_on='id_str', right_on='id_str')

# # Making a date column
merged_KLM['date'] = merged_KLM[['year_tweet', 'month_tweet', 'day_tweet']].astype(str).agg('-'.join, axis=1)
merged_KLM['date'] = pd.to_datetime(merged_KLM['date'], errors='coerce')
merged_LUF['date'] = merged_LUF[['year_tweet', 'month_tweet', 'day_tweet']].astype(str).agg('-'.join, axis=1)
merged_LUF['date'] = pd.to_datetime(merged_LUF['date'], errors='coerce')

# Dropping the columns that we don't need
merged_KLM.drop(['year_tweet', 'month_tweet', 'day_tweet', 'index','tweet_created_at ', 'entity_user_mentions ','con_id_str_list ','con_id_str_list1 ','full_conversation_ids',
        'airline_contain_con','airline_contain_con_time','airline_reply_time','con_id_str_list2 '], axis=1, inplace=True)
merged_LUF.drop(['year_tweet', 'month_tweet', 'day_tweet', 'index','tweet_created_at ', 'entity_user_mentions ','con_id_str_list ','con_id_str_list1 ','full_conversation_ids',
        'airline_contain_con','airline_contain_con_time','airline_reply_time'], axis=1, inplace=True)


# This where insert the date
start_date = pd.to_datetime('2019-11-06')
end_date = pd.to_datetime('2019-11-08')
filtered_df = merged_KLM[
    (merged_KLM['date'] >= start_date) & (merged_KLM['date'] <= end_date)]
grouped_time_1 = filtered_df['minus'].groupby(filtered_df['date']).mean()
filtered_df = merged_LUF[
    (merged_LUF['date'] >= start_date) & (merged_LUF['date'] <= end_date)]
grouped_time_2 = filtered_df['minus'].groupby(filtered_df['date']).mean()

#Plot the sentiment and subjectivity change over time
fig, ax = plt.subplots(figsize=(10, 6))
#ax.plot(grouped_time_1.index, grouped_time_1, label='KLM')
ax.plot(grouped_time_2.index, grouped_time_2, label='Lufthansa')
ax.set_xlabel('Date')
ax.set_ylabel('time(minutes)')
ax.set_title('Lufthansa(November)')
ax.legend()
plt.xticks(rotation=45)
plt.savefig(fname='Lufthansa (November)', dpi=200)

