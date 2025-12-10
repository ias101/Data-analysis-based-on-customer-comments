# DBL Data Challenge

***

## Evaluating Lufthansa's Twitter Presence
With the use of sentiment analysis, conversation mining, and topic analysis on tweets about/mentioning airlines, we evaluate our client Lufthansa's Twitter presence compared to other airlines, in particular their main competitor KLM.

With this we can advise Lufthansa on their social media strategy and answer the questions:
- [ ] How is Lufthansa faring on Twitter?
- [ ] How is Lufthansa's Twitter presence in comparison with other airlines, specifically KLM?
- [ ] And ultimately, should Lufthansa keep their Twitter account active?

***

## User Instructions 
### Installation Steps
- [ ] main/requirements.txt: all the required libraries to run the project

### Running the project
For this project we were given 567 JSON files of data to use for our data exploration. We saved these files into one big CSV in the [Data Storage](#data-storage-and-cleaning) step. However, we initially used a MySQL database from which we got a CSV called 'result.csv'. This is important to mention, as some code still uses this CSV instead of 'Complete_data.csv'.

For this project, we used a combination of PyCharm files and Jupyter Notebooks. Run the files mentioned at each step.

All CSVs that aren't generated anywhere yet used in later steps were made from existing/generated CSVs (pieces of CSVs or merged CSVs). They are all provided.

#### Data Storage and Cleaning
- [ ] Processing_Data_Final.ipynb
  - [ ] This selects certain wanted/necessary keys from each JSON file and cleans the data.
  - INPUT: each of the given JSON files
  - OUTPUT: a CSV with all our necessary data for the next steps: 'Complete_data.csv'

#### Conversation Mining
- [ ] Strict_Conversation_Mining_Final.ipynb
  - [ ] This file is used for mining conversations for each airline on Twitter.
  - INPUT: 'result.csv'
    - [ ] Replace the airline id for the Conversation function for each airline in airline_list to get that airline's conversations CSV
  - OUTPUT: All conversation CSVs split up per airline, e.g. 'conversations_124476322.csv'

#### Sentiment Analysis on Single Tweets
- [ ] Sentiment_Analysis/sentiment_vader/main.py
  - [ ] A copy of 'Complete_data.csv' is made: 'complete_data_with_vader.csv' and sentiment analysis is applied to each tweet's text using the sentiment analysis model VADER in a new file 'vader.csv'. These scores are added to the CSV.
  - INPUT: 'complete_data_with_vader.csv', 'vader.csv'
  - OUTPUT: 'complete_data_with_vader.csv'
- [ ] EDA/Final_Sentiment_Analysis_EDA.ipynb
  - [ ] This file produces visualisations used in presentation 2
  - INPUT: 'complete_data_with_vader.csv'

#### Topic Analysis 
- [ ] Files/word_frequency.py
  - [ ] Calculates word frequency for specified word combinations related to airlines.
  - INPUT: all airline's conversation CSVs, 'result.csv' 
  - OUTPUT: 'word_frequency.csv'
  - [ ] A copy of this file ('EDA/word_frequency.ipynb') is used for visualizations.
- [ ] EDA/Word_frequency_and_average_sentiment-checkpoint.ipynb
  - [ ] Graphs for word combinations and their sentiments for all airlines and Lufthansa separately.
  - INPUT: all airline's conversation csv, 'result.csv' 
  - OUTPUT: 'word_frequency.csv'

#### Sentiment Analysis on Conversations
- [ ] Files/add_vader_score.py
  - [ ] Adds VADER scores to mined conversations.
  - INPUT: 'vader.csv', all conversation files
    - [ ] Replace the conversations file being opened with the conversation file for each airline.
  - OUTPUT: All conversation files/CSVs split up per airline with VADER scores for each tweet in the conversation, e.g. 'conversations_124476322_vader.csv' 
- [ ] Sentiment_Analysis/Sentiment_Change_in_Conversation.ipynb
  - [ ] Calculates the sentiment change or evolution throughout conversations.
  - INPUT: Uses the conversations with VADER CSVs
  - OUTPUT: Table for final presentation's poster.

#### Sentiment versus Subjectivity
- [ ] Sentiment_Analysis/text_blob.py
  - [ ] Applies TextBlob to each tweet to gain polarity and subjectivity.
  - INPUT: 'complete_data.csv'
  - OUTPUT: 'text_blob_update.csv'
- [ ] Sentiment_Analysis/Sentiment_and_Subjectivity_after_strikes.py
  - [ ] Graphs of sentiment and subjectivity after strikes.
  - INPUT: 'complete_data_with_vader.csv', 'text_blob_update.csv'

#### Reply Time
- [ ] main/time_calculate.ipynb
  - [ ] Calculates the airlines' reply time to users.
  - INPUT: 'result.csv', all conversation CSVs split up per airline
  - OUTPUT: main/data_files/18332190_time_describe.xls
- [ ] EDA/Reply_time_after_strike.py
  - [ ] Plots the change in reply time over time. 
  - INPUT: 'complete_data_with_vader.csv', 'KLM.csv', 'LUF.csv'


#### Dashboard
This Plotly Dash bootstrap is meant for the visualization of our findings for our airline compared to other airlines.
- [ ] Run bootstrap.py which imports the following CSVs:
  - INPUT:
      - [ ] mentions_posts_df.csv
      - [ ] monthly_sentiment_df.csv
      - [ ] complete_data_with_vader.csv from [Sentiment Analysis on Single Tweets](#sentiment-analysis-on-single-tweets)
      - [ ] word_frequency.csv from [Topic Analysis](#topic-analysis-)
      - [ ] average_sentiments.csv
      - [ ] text_blob_update.csv from [Sentiment vs Subjectivity](#sentiment-versus-subjectivity)
      - [ ] KLM.csv and LUF.csv
  - OUTPUT: a link to an interactive Dashboard.


***

## Authors and acknowledgment
The team: DBL Group 18
- [ ] Annebel Hattingh-Haasbroek
- [ ] Hetvi Chaniyara
- [ ] Iris Shi
- [ ] Jikun Shen
- [ ] Thomas Heller

A special thanks to our tutor and the teachers with helping us throughout the process of this project.
