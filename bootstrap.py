import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.express as px  # for graphs
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import dash_table
import pandas as pd
import numpy as np
import re

# pip install dash, pip install dash_bootstrap_components, pip install xlrd

## Import data ##
data_path = 'data_files/mentions_posts_df.csv'
df_activity = pd.read_csv(data_path)

data_path2 = 'data_files/monthly_sentiment_df.csv'
df_sent0 = pd.read_csv(data_path2)

data_path3 = 'data_files/average_sentiments.csv'
df_avg_sent = pd.read_csv(data_path3)

data_path4 = 'data_files/KLM.csv'
time_KLM = pd.read_csv(data_path4,usecols=['id_str','56377143'], encoding='latin-1')

data_path5 = 'data_files/text_blob_update.csv'
subjectivity_df = pd.read_csv(data_path5,usecols=['tweet_id','polarity','subjectivity'], encoding='latin-1')

data_path6 = 'data_files/complete_data_with_vader.csv'
tweets_df = pd.read_csv(data_path6, usecols=['id_str', 'year_tweet', 'month_tweet', 'day_tweet', 'Vader_com'], encoding='latin-1')

data_path7 = 'data_files/LUF.csv'
time_Luf = pd.read_csv(data_path7,usecols=['id_str','124476322'], encoding='latin-1')

data_path8 = 'data_files/word_frequency.csv'
df_word_freq = pd.read_csv(data_path8)

# For grouping: KLM is 0, Lufthansa is 4
airline_list = ['56377143', '106062176', '18332190', '22536055', '124476322', '26223583', '2182373406', '38676903',
                '1542862735','253340062', '218730857', '45621423', '20626359']
airline_names = ['KLM', 'AirFrance', 'British_Airways', 'AmericanAir', 'Lufthansa', 'AirBerlin', 'Airberlin_assist',
                 'easyJet', 'RyanAir', 'SingaporeanAir', 'Qantas', 'EtihadAirways', 'VirginAtlantic']
airline_dict = dict(zip(airline_list, airline_names))

### change according to DEMO ###
start_date = "2019-05-22"
end_date = "2020-03-30"
start_month = "2019-05"
end_month = "2020-03"

### DF time interval ###
df_activity = df_activity[(df_activity['tweet_date'] > start_date) & (df_activity['tweet_date'] < end_date)]
df_sent = df_sent0.copy()
df_sent['tweet_date'] = df_sent['tweet_created_at'].apply(lambda x: str(x)[:10])
df_sent = df_sent[(df_sent['tweet_date'] > start_date) & (df_sent['tweet_date'] < end_date)]

### CONFUSION MATRIX DF ###
data1 = [[[8, 0, 1], [3, 9, 0]],
         [[2, 3, 0], [0, 5, 1]],
         [[0, 0, 6], [0, 1, 1]]]
columns1 = ['vader_sentiment', 'textblob_polarity']
df1 = pd.DataFrame(data1, columns=columns1)

data2 = [[[10, 1]], [[3, 6]]]
column_names2 = ['textblob_subjectivity']
df2 = pd.DataFrame(data2, columns=column_names2)

### TABLE FOR SENTIMENT EVOLUTION ###
data = {
    'Airline': ['KLM', 'Air France', 'Singapore Air', 'Virgin Atlantic'],
    'Neg->Neu': [0,7,11,0],
    'Neu->Pos': [0,17,22,0],
    'Neg->Pos': [67,41,30,0],
    'Pos->Neu': [0,0,2,33],
    'Neu->Neg': [0,0,0,0],
    'Pos->Neg': [33,0,0,0],
    'Pos_same': [0,24,33,33],
    'Neu_same': [0,10,2,0],
    'Neg_same': [0,0,0,33],
    'Conversations': [5,29,46,3],
    'Mean Difference': [0.1517,-0.0459,0.1559,-0.1398]
}

df = pd.DataFrame(data)

### TABLE FOR CONVERSATIONS ###
data_convo = {
    'Airline': ['American Air','British Airways','Easy Jet','KLM','Qantas','Virgin Atlantic', 'Ryan Air', 'Lufthansa','Singapore Air','Air France','Etihad Airways','Air Berlin & Assist'],
    'Mean Length': [2.005,2.025,2.041,2.144,2.010,2.023,2.003,2.024,2.061,2.210,2.018,0],
    'Minimum Length': [2,2,2,2,2,2,2,2,2,2,2,0],
    'Maximum Length': [7,5,5,7,5,4,3,4,5,5,5,0],
    'Conversations': [31500,14662,8283,4243,3162,2912,2029,1864,1448,1202,279,0],
    'Unanswered Tweets':[14923,8082,5737,4025,3504,2686,6557,2560,689,1775,997,4427],
    'Level 1 Reply':  [31640,15023,8618,4848,3186,2976,2036,1909,1488,1425,284,0],
    'Level 2 Reply':  [0,0,0,5,6,3,0,0,46,29,0,0]
}

df_convo = pd.DataFrame(data_convo)

### TABLE FOR REPLY TIME ###
excel_file_path = "data_files/18332190_time_describe.xls"
df_reply = pd.read_excel(excel_file_path)
df_reply.rename(columns={'Unnamed: 0': ''}, inplace=True)


# Create stacked bar chart -- SENTIMENT EVOLUTION
colors = ['#FFC300', '#FF5733', '#C70039', '#900C3F', '#581845', '#3D9970', '#7FDBFF', '#001f3f', '#FF4136']

fig = go.Figure()

for i, column in enumerate(df.columns[1:]):
    if column != 'Conversations' and column != 'Mean Difference':  # Exclude 'Conversations' column
        color_index = i % len(colors)
        fig.add_trace(go.Bar(
            x=df['Airline'],
            y=df[column],
            name=column,
            text=[f"<b>{column}</b>" for _ in df],  # Set the text to the column name with HTML bold tags
            textposition='auto',
            textfont=dict(color='white', size=22),
            marker=dict(color=colors[color_index])
        ))

fig.update_layout(
    barmode='stack',
    title='<b>Sentiment Changes by Airline<b>',
    height=600,  # Set the height of the bar chart
    yaxis={
            'title': {'text': 'Airlines', 'font': {'size': 24}},
            'tickfont': {'size':22}
        },
    xaxis={
            'title': {'text': 'Sentiment Changes', 'font': {'size':24}},
            'tickfont': {'size': 22}
        },
    legend={
        'title': {'text': 'Sentiment Changes'},
        'font': {'size':26},
        'itemsizing': 'constant'
    },
    margin=dict(t=40),
)

# Create stacked bar chart -- SENTIMENT PROPORTIONS
# Calculate proportions per airline

df_sent = df_sent[(df_sent['tweet_date'] > start_date) & (df_sent['tweet_date'] < end_date)]
df_sent['sentiment_category'] = pd.cut(df_sent['Vader_com'], bins=[-1, -0.25, 0.25, 1],
                                       labels=['Negative', 'Neutral', 'Positive'])
# updated_airlines = ['KLM', 'AemricanAir', 'SingaporeanAir', 'British_Airways', 'VirginAtlantic', 'AirFrance', 'Lufthansa']
# df_sent_updated = df_sent[df_sent['the_airline'].isin(updated_airlines)]
df_proportions = df_sent.groupby(['the_airline', 'sentiment_category']).size().unstack().reset_index()
df_proportions['Total'] = df_proportions[['Negative', 'Neutral', 'Positive']].sum(axis=1)
df_proportions['Negative'] /= df_proportions['Total']
df_proportions['Neutral'] /= df_proportions['Total']
df_proportions['Positive'] /= df_proportions['Total']

colors2 = ['#ed0606', '#f9ba00', '#00235f']

fig1 = px.bar(df_proportions, x="the_airline", y=['Negative', 'Neutral', 'Positive'], height=600,
              color_discrete_sequence=colors2)


fig1.update_layout(
    yaxis_range=[0, 1],
    yaxis={
            'title': {'text': 'Proportions (%)', 'font': {'size': 24}},
            'tickfont': {'size': 22},
        },
    xaxis={
            'title': {'text': 'Airlines', 'font': {'size': 24}},
            'tickfont': {'size': 22}
        },
    legend={
        'title': {'text': 'Sentiment Categories'},
        'font': {'size': 24},
        'itemsizing': 'constant'
    },
    margin=dict(t=40),
    title={
        'text': "<b>Sentiment Proportions per Airline</b>",
        'font': {'size': 24}
    }
)


# Plot the average sentiment scores for all airlines and Lufthansa -- WORD FREQUENCY
fig2 = px.bar(df_avg_sent, y='Word Combination', x=['All Airlines', 'Lufthansa'],
             barmode='group', color_discrete_map={'All Airlines': 'blue', 'Lufthansa': 'orange'})

# Update the figure layout
fig2.update_layout(title={'text': 'Average Sentiment Scores for Word Combinations', 'font': {'size': 24}},
                   yaxis={'title': {'text': 'Word Combination', 'font': {'size': 24}}, 'tickfont': {'size': 22}},
                   xaxis={'title': {'text': 'Sentiment Score', 'font': {'size': 24}}, 'tickfont': {'size': 22}},
                   margin=dict(t=40)
                   )

### PLOT FOR REAL-LIFE EVENTS ###
name = ['id_str','reply_time']
time_KLM.columns = name
time_Luf.columns = name
merged_KLM = pd.merge(time_KLM, tweets_df, left_on='id_str', right_on='id_str')
merged_KLM = pd.merge(merged_KLM,subjectivity_df,left_on='id_str', right_on='tweet_id')
merged_KLM['date'] = merged_KLM[['year_tweet', 'month_tweet', 'day_tweet']].astype(str).agg('-'.join, axis=1)
merged_KLM['date'] = pd.to_datetime(merged_KLM['date'], errors='coerce')
merged_KLM.drop(['year_tweet', 'month_tweet', 'day_tweet'], axis=1, inplace=True)
merged_Luf = pd.merge(time_Luf, tweets_df, left_on='id_str', right_on='id_str')
merged_Luf = pd.merge(merged_Luf,subjectivity_df,left_on='id_str', right_on='tweet_id')
merged_Luf['date'] = merged_Luf[['year_tweet', 'month_tweet', 'day_tweet']].astype(str).agg('-'.join, axis=1)
merged_Luf['date'] = pd.to_datetime(merged_Luf['date'], errors='coerce')
merged_Luf.drop(['year_tweet', 'month_tweet', 'day_tweet'], axis=1, inplace=True)

# September
start_date = pd.to_datetime('2019-09-01')
end_date = pd.to_datetime('2019-09-30')
filtered_df = merged_KLM[(merged_KLM['date'] >= start_date) & (merged_KLM['date'] <= end_date)]
filtered_df_Luf = merged_Luf[(merged_Luf['date'] >= start_date) & (merged_Luf['date'] <= end_date)]

# Sentiment and Subjectivity (Sept)
grouped_sentiment = filtered_df.groupby(filtered_df['date']).mean()
fig_sentiment = px.line(grouped_sentiment, x = grouped_sentiment.index, y = ['Vader_com','subjectivity'],color_discrete_map={'Vader_com': 'blue', 'subjectivity': 'orange'},range_y=[-1,1])
fig_reply = px.line(grouped_sentiment,x = grouped_sentiment.index,y = ['reply_time'])

fig_sentiment.update_layout(
    barmode='stack',
    title='<b>Sentiment And Subjectivity After Strikes: KLM (Sept)<b>',
    title_font=dict(size=24),
    height=600,
    width=900,
    yaxis={
            'title': {'text': 'VADER score', 'font': {'size': 24}},
            'tickfont': {'size': 20}
        },
    xaxis={
            'title': {'text': 'Month and Year', 'font': {'size': 24}},
            'tickfont': {'size': 20}
        },
    legend={
        'title': {'text': 'Airlines'},
        'font': {'size': 20},
        'itemsizing': 'constant'
    },
    margin=dict(t=40)
)
fig_reply.update_layout(
    barmode='stack',
    title='<b>Response Time After Strikes: KLM (Sept)<b>',
    title_font=dict(size=24),
    height=600,
    width=900,
    yaxis={
            'title': {'text': 'Reply time', 'font': {'size': 24}},
            'tickfont': {'size': 20}
        },
    xaxis={
            'title': {'text': 'Month and Year', 'font': {'size': 24}},
            'tickfont': {'size': 20}
        },
    legend={
        'title': {'text': 'Airlines'},
        'font': {'size': 20},
        'itemsizing': 'constant'
    },
    margin=dict(t=40)
)

# Lufthansa
grouped_sentiment_Luf = filtered_df_Luf.groupby(filtered_df_Luf['date']).mean()
fig_sentiment_Luf = px.line(grouped_sentiment_Luf, x = grouped_sentiment_Luf.index, y = ['Vader_com','subjectivity'],color_discrete_map={'Vader_com': 'blue', 'subjectivity': 'orange'},range_y=[-1,1])
fig_reply_Luf = px.line(grouped_sentiment_Luf,x = grouped_sentiment_Luf.index,y = ['reply_time'])

fig_sentiment_Luf.update_layout(
    barmode='stack',
    title='<b>Sentiment And Subjectivity After Strikes: Lufthansa (Sept)<b>',
    title_font=dict(size=24),
    height=600,
    width=900,
    yaxis={
            'title': {'text': 'VADER score', 'font': {'size': 24}},
            'tickfont': {'size': 20}
        },
    xaxis={
            'title': {'text': 'Month and Year', 'font': {'size': 24}},
            'tickfont': {'size': 20}
        },
    legend={
        'title': {'text': 'Airlines'},
        'font': {'size': 20},
        'itemsizing': 'constant'
    },
    margin=dict(t=40)
)
fig_reply_Luf.update_layout(
    barmode='stack',
    title='<b>Response Time After Strikes: Lufthansa (Sept)<b>',
    title_font=dict(size=24),
    height=600,
    width=900,
    yaxis={
            'title': {'text': 'Reply time', 'font': {'size': 24}},
            'tickfont': {'size': 20}
        },
    xaxis={
            'title': {'text': 'Month and Year', 'font': {'size': 24}},
            'tickfont': {'size': 20}
        },
    legend={
        'title': {'text': 'Airlines'},
        'font': {'size': 20},
        'itemsizing': 'constant'
    },
    margin=dict(t=40)
)
# December
start_date_1 = pd.to_datetime('2019-12-01')
end_date_1 = pd.to_datetime('2019-12-21')
filtered_df_1 = merged_KLM[(merged_KLM['date'] >= start_date_1) & (merged_KLM['date'] <= end_date_1)]

# Sentiment and Subjectivity (Dec)
grouped_sentiment_1 = filtered_df_1.groupby(filtered_df_1['date']).mean()
fig_sentiment_1 = px.line(grouped_sentiment_1, x = grouped_sentiment_1.index, y = ['Vader_com','subjectivity'],color_discrete_map={'Vader_com': 'blue', 'subjectivity': 'orange'},range_y=[-1,1])
fig_reply_1 = px.line(grouped_sentiment_1, x = grouped_sentiment_1.index,y = ['reply_time'])

fig_sentiment_1.update_layout(
    barmode='stack',
    title='<b>Sentiment And Subjectivity After Strikes: KLM (Dec)<b>',
    title_font=dict(size=24),
    height=600,
    width=900,
    yaxis={
            'title': {'text': 'VADER score', 'font': {'size': 24}},
            'tickfont': {'size': 20}
        },
    xaxis={
            'title': {'text': 'Month and Year', 'font': {'size': 24}},
            'tickfont': {'size': 20}
        },
    legend={
        'title': {'text': 'Airlines'},
        'font': {'size': 20},
        'itemsizing': 'constant'
    },
    margin=dict(t=40)
)
fig_reply_1.update_layout(
    barmode='stack',
    title='<b>Response Time After Strikes: KLM (Dec)<b>',
    title_font=dict(size=24),
    height=600,
    width=900,
    yaxis={
            'title': {'text': 'Reply time', 'font': {'size': 24}},
            'tickfont': {'size': 20}
        },
    xaxis={
            'title': {'text': 'Month and Year', 'font': {'size': 24}},
            'tickfont': {'size': 20}
        },
    legend={
        'title': {'text': 'Airlines'},
        'font': {'size': 20},
        'itemsizing': 'constant'
    },
    margin=dict(t=40)
)

# November
start_date_2 = pd.to_datetime('2019-11-01')
end_date_2 = pd.to_datetime('2019-11-11')
filtered_df_Luf_1 = merged_Luf[(merged_Luf['date'] >= start_date_2) & (merged_Luf['date'] <= end_date_2)]

# Sentiment and Subjectivity(Nov)
grouped_sentiment_Luf_1 = filtered_df_Luf_1.groupby(filtered_df_Luf_1['date']).mean()
fig_sentiment_Luf_1 = px.line(grouped_sentiment_Luf_1, x = grouped_sentiment_Luf_1.index, y = ['Vader_com','subjectivity'],color_discrete_map={'Vader_com': 'blue', 'subjectivity': 'orange'},range_y=[-1,1])
fig_reply_Luf_1 = px.line(grouped_sentiment_Luf_1,x = grouped_sentiment_Luf_1.index,y = ['reply_time'])

fig_sentiment_Luf_1.update_layout(
    barmode='stack',
    title='<b>Sentiment And Subjectivity After Strikes: Lufthansa (Nov)<b>',
    title_font=dict(size=24),
    height=600,
    width=900,
    yaxis={
            'title': {'text': 'VADER score', 'font': {'size': 24}},
            'tickfont': {'size': 20}
        },
    xaxis={
            'title': {'text': 'Month and Year', 'font': {'size': 24}},
            'tickfont': {'size': 20}
        },
    legend={
        'title': {'text': 'Airlines'},
        'font': {'size': 20},
        'itemsizing': 'constant'
    },
    margin=dict(t=40)
)
fig_reply_Luf_1.update_layout(
    barmode='stack',
    title='<b>Response Time After Strikes: Lufthansa (Nov)<b>',
    title_font=dict(size=24),
    height=600,
    width=900,
    yaxis={
            'title': {'text': 'Reply time', 'font': {'size': 24}},
            'tickfont': {'size': 20}
        },
    xaxis={
            'title': {'text': 'Month and Year', 'font': {'size': 24}},
            'tickfont': {'size': 20}
        },
    legend={
        'title': {'text': 'Airlines'},
        'font': {'size': 20},
        'itemsizing': 'constant'
    },
    margin=dict(t=40)
)

# Plot the frequency for word combinations for all airlines and Lufthansa -- WORD FREQUENCY
fig3 = px.bar(df_word_freq, x=['All Airlines', 'Lufthansa'], y='Word Combination',
            color_discrete_sequence=['blue', 'orange'],
            labels={'All Airlines': 'All Airlines', 'Lufthansa': 'Lufthansa', 'Word Combination': 'Word Combinations'},
            title='Frequency of Word Combinations')

# Set the font size for the title
fig3.update_layout(title={'text': 'Frequency of Word Combinations',
                        'font': {'size': 24}},
                   yaxis={'title': {'text': 'Word Combination', 'font': {'size': 24}}, 'tickfont': {'size': 22}},
                   xaxis={'title': {'text': 'Frequency', 'font': {'size': 24}}, 'tickfont': {'size': 22}},
                   margin=dict(t=40)
                   )



#---------------------------------------------------## APP ##---------------------------------------------------------#
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

# app layout
app.layout = dbc.Container([
    dbc.Row(
        [
            dbc.Col(
                html.Img(src="https://cdn.freebiesupply.com/logos/large/2x/lufthansa-2-logo-png-transparent.png",
                         height="50px"),
                width=2,
                className='d-flex align-items-center justify-content-end'
            ),
            dbc.Col(
                html.H1("Lufthansa's Interactive Twitter Dashboard",
                        className='text-center text-primary mb-4'),
                width=8,
                className='d-flex align-items-center justify-content-center'
            ),
            dbc.Col(
                html.Img(src="https://cdn.freebiesupply.com/logos/large/2x/lufthansa-2-logo-png-transparent.png",
                         height="50px"),
                width=2,
                className='d-flex align-items-center justify-content-start'
            ),
        ]
    ),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='my-dpdn', multi=True, value=['Lufthansa', 'KLM'],
                         options=[{'label': x, 'value': x}
                                  for x in sorted(df_activity['the_airline'].unique())],
                         ),
            dcc.Graph(id='group-bar-chart', figure={})
        ]),

    ]),
    dbc.Row([
        dbc.Col(
            dash_table.DataTable(
                id='Conversations-table',
                columns=[{'name': col, 'id': col} for col in df_convo.columns],
                data=df_convo.to_dict('records'),
                style_table={
                    'padding': '40px',  # Add padding to the table
                    'overflowY': 'auto',  # Enable vertical scrolling if needed
                },
                style_cell={
                    'textAlign': 'center'  # Center align the data in the cells
                },
                style_data_conditional=[
                    {
                        'if': {'filter_query': '{Airline} eq "KLM" || {Airline} eq "Lufthansa"'},
                        'backgroundColor': '#e6f7ff',  # Apply background color to the matching rows
                        'color': 'black',  # Set text color for the matching rows
                    }
                ]
            ),
            width=12,
        ),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='my-dpdn3', multi=True, value=['Lufthansa', 'KLM'],
                         options=[{'label': x, 'value': x}
                                  for x in sorted(df_activity['the_airline'].unique())],
                         ),
            dcc.Graph(id='airline-lines', figure={})
        ], width=7),
    ], justify='center', style={'margin-bottom': '30px'},),

    dbc.Row([
        dbc.Col(
            dcc.Graph(
                id='sent-prop-bar-chart',
                figure=fig1,
            ),
            width=12,
        ),
    ], align="center",
    ),
    html.H5("Sentiment Evolution throughout Conversations", style={'margin-top': '50px', 'color': 'black'}),
    dbc.Row(
        [
            dbc.Col(
                dcc.Graph(
                    id='sentiment-bar-chart',
                    figure=fig,
                ),
                width=12,
            ),
        ],
        align="center",
    ),
    dbc.Row(
        [
            dbc.Col(
                dash_table.DataTable(
                    id='sentiment-table',
                    columns=[{'name': col, 'id': col} for col in df.columns],
                    data=df.to_dict('records'),
                    style_table={
                        'padding': '40px',  # Add padding to the table
                        'overflowY': 'auto',  # Enable vertical scrolling if needed
                    },
                    style_cell={
                        'textAlign': 'center'  # Center align the data in the cells
                    },
                    style_data_conditional=[
                        {'if': {'column_id': 'Neg->Pos'},
                            'backgroundColor': '#e6f7ff', 'color': 'black'}, # positive - blue
                        {'if': {'column_id': 'Neu->Pos'},
                            'backgroundColor': '#e6f7ff', 'color': 'black'},
                        {'if': {'column_id': 'Pos_same'},
                            'backgroundColor': '#e6f7ff', 'color': 'black'},
                        {'if': {'column_id': 'Neg_same'},
                            'backgroundColor': '#FFC0C0', 'color': 'black'}, # negative - red
                        {'if': {'column_id': 'Pos->Neg'},
                            'backgroundColor': '#FFC0C0', 'color': 'black'},
                        {'if': {'column_id': 'Neu->Neg'},
                            'backgroundColor': '#FFC0C0', 'color': 'black'},
                        {'if': {'column_id': 'Neu_same'},
                            'backgroundColor': '#FFFFE0', 'color': 'black'}, # neutral - orange
                        {'if': {'column_id': 'Pos->Neu'},
                            'backgroundColor': '#FFFFE0', 'color': 'black'},
                        {'if': {'column_id': 'Neg->Neu'},
                            'backgroundColor': '#FFFFE0', 'color': 'black'},
                    ],
                ),
                width=12,
                style={"margin": "auto"}  # Center align the table within the column
            ),
        ],
        align="center",
    ),
    dbc.Row(
       [
           dbc.Col(
               dcc.Graph(
                   id='word-freq-chart',
                   figure=fig3
               ),
               width=12,
           ),
       ],
       align="center",
    ),
    dbc.Row(
        [
            dbc.Col(
                dcc.Graph(
                    id='sent-avg-chart',
                    figure=fig2
                ),
                width=12,
            ),
        ],
        align="center",
    ),
    html.H5("Accuracy of the Sentiment Analysis Models", style={'margin-top': '50px', 'color': 'black'}),
    dbc.Row([
        dbc.Col(
            [
                dcc.Graph(
                    id='heatmap1',
                    figure={
                        'data': [
                            go.Heatmap(
                                z=df1['vader_sentiment'],
                                x=["Neg", "Neu", "Pos"],
                                y=["Neg", "Neu", "Pos"],
                                hoverongaps=False,
                                colorscale='Viridis',
                                showscale=True
                            )
                        ],
                        'layout': go.Layout(
                            title="VADER Sentiment Accuracy",
                            xaxis={'title': 'Predicted'},
                            yaxis={'title': 'Actual'},
                            margin={'l': 50, 'r': 50, 't': 40, 'b': 40}
                        )
                    }
                ),
                html.P("Accuracy: 85%", style={'margin-top': '10px'})
            ],
            width=4
        ),
        dbc.Col(
            [
                dcc.Graph(
                    id='heatmap2',
                    figure={
                        'data': [
                            go.Heatmap(
                                z=df1['textblob_polarity'],
                                x=["Neg", "Neu", "Pos"],
                                y=["Neg", "Neu", "Pos"],
                                hoverongaps=False,
                                colorscale='Viridis',
                                showscale=True
                            )
                        ],
                        'layout': go.Layout(
                            title="TextBlob Polarity Accuracy",
                            xaxis={'title': 'Predicted'},
                            yaxis={'title': 'Actual'},
                            margin={'l': 50, 'r': 50, 't': 40, 'b': 40}
                        )
                    }
                ),
                html.P("Accuracy: 45%", style={'margin-top': '10px'})
            ],
            width=4
        ),
        dbc.Col(
            [
                dcc.Graph(
                    id='heatmap3',
                    figure={
                        'data': [
                            go.Heatmap(
                                z=df2['textblob_subjectivity'],
                                x=['Obj', 'Subj'],
                                y=['Obj', 'Subj'],
                                hoverongaps=False,
                                colorscale='Viridis',
                                showscale=True
                            )
                        ],
                        'layout': go.Layout(
                            title="TextBlob Subjectivity Accuracy",
                            xaxis={'title': 'Predicted'},
                            yaxis={'title': 'Actual'},
                            margin={'l': 50, 'r': 50, 't': 40, 'b': 40}
                        )
                    }
                ),
                html.P("Accuracy: 80%", style={'margin-top': '10px'})
            ],
            width=4
        ),

    ],
        style={'margin-bottom': '20px'}  # Additional margin between the rows
    ),
    dbc.Row(
        [
            dbc.Col(
                dcc.Graph(
                    id='sentiment-subjectivity-line-chart',
                    figure=fig_sentiment,
                ),
                width=6,
            ),
            dbc.Col(
                dcc.Graph(
                    id='reply-line-chart',
                    figure=fig_reply,
                ),
                width=6,
            ),
        ],
        align="center",
    ),
    dbc.Row(
        [
            dbc.Col(
                dcc.Graph(
                    id='sentiment-subjectivity-line-chart_luf',
                    figure=fig_sentiment_Luf,
                ),
                width=6,
            ),
            dbc.Col(
                dcc.Graph(
                    id='reply-line-chart_luf',
                    figure=fig_reply_Luf,
                ),
                width=6,
            ),
        ],
        align="center",
    ),
    dbc.Row(
        [
            dbc.Col(
                dcc.Graph(
                    id='sentiment-subjectivity-line-chart_1',
                    figure=fig_sentiment_1,
                ),
                width=6,
            ),
            dbc.Col(
                dcc.Graph(
                    id='reply-line-chart_1',
                    figure=fig_reply_1,
                ),
                width=6,
            ),
        ],
        align="center",
    ),
    dbc.Row(
        [
            dbc.Col(
                dcc.Graph(
                    id='sentiment-subjectivity-line-chart_LUF',
                    figure=fig_sentiment_Luf_1,
                ),
                width=6,
            ),
            dbc.Col(
                dcc.Graph(
                    id='reply-line-chart_LUF',
                    figure=fig_reply_Luf_1,
                ),
                width=6,
            ),
        ],
        align="center",
    ),
    dbc.Row([
        dbc.Col(
            dash_table.DataTable(
                id='Reply-table',
                columns=[{'name': col, 'id': col} for col in df_reply.columns],
                data=df_reply.to_dict('records'),
                style_table={
                    'padding': '40px',  # Add padding to the table
                    'overflowY': 'auto',  # Enable vertical scrolling if needed
                },
                style_cell={
                    'textAlign': 'center'  # Center align the data in the cells
                },
                style_data_conditional=[
                        {'if': {'column_id': 'Lufthansa'},
                            'backgroundColor': '#e6f7ff', 'color': 'black'}, # positive - blue
                        {'if': {'column_id': 'KLM'},
                            'backgroundColor': '#e6f7ff', 'color': 'black'}
                ]
            ),
            width=12,
        ),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='my-dpdn2', multi=False, value='Lufthansa',
                         options=[{'label': x, 'value': x}
                                  for x in sorted(df_activity['the_airline'].unique())],
                         ),
            dcc.Graph(id='follow-sent-chart', figure={})
        ], width=8, ),

        dbc.Col(
            [
                html.H5("Analysis", style={'margin-top': '50px', 'color': 'black'}),
                html.P(id='additional-text')
            ],
            width=4, )
    ]),
], fluid=False)

@app.callback(
    Output('group-bar-chart', 'figure'),
    Input('my-dpdn', 'value')
)
def update_graph(value):
    dff = df_activity[df_activity['the_airline'].isin(value)]
    dff['month_year'] = dff['tweet_date'].apply(lambda x: str(x)[:7])
    dff2 = dff.groupby(['month_year', 'the_airline'], as_index=False)[
        ['airline_mentions_count', 'airline_posts_count']].sum()

    fig = px.bar(dff2, y='the_airline', x=['airline_posts_count', 'airline_mentions_count'],
                 barmode='group', hover_data='month_year', labels={
            'the_airline': 'Airlines',
            'value': 'Number of Tweets'
        },
                 title="<b>Number of posts by the airline VS number of mentions</b>")
    fig.update_traces(width=0.2)
    fig.update_layout(
        height=600,
        width=1200,
        legend={
            'title': {'text': 'Tweet Counts'},
            'font': {'size': 24},
            'itemsizing': 'constant',
            'itemclick': 'toggleothers',
        },
        yaxis={
            'title': {'text': 'Airlines', 'font': {'size': 24}},
            'tickfont': {'size': 24}
        },
        xaxis={
            'title': {'text': 'Number of Tweets', 'font': {'size': 24}},
            'tickfont': {'size':24}
        },
        margin=dict(t=40),
        bargap=0.05
    )

    return fig

@app.callback(
    Output('follow-sent-chart', 'figure'),
    Output('additional-text', 'children'),
    Input('my-dpdn2', 'value')
)
def update_graph(value):  # FOLLOWERS VS SENTIMENT
    dff = df_activity[df_activity['the_airline'] == value]
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=dff['tweet_date'], y=dff['Vader_com'], name="VADER score"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=dff['tweet_date'], y=dff['user_followers_count'], name="Followers"),
        secondary_y=True,
    )

    fig.update_layout(
        xaxis={
            'title': {'text': 'Date', 'font': {'size': 24}},
            'tickfont': {'size': 18}
        },
        yaxis=dict(
            title={'text': 'VADER score', 'font': {'size': 24}},
            tickfont={'size': 18}
        ),
        yaxis2=dict(
            title={'text': 'Followers', 'font': {'size': 24}},
            tickfont={'size': 18}
        ),
        legend={
            'font': {'size': 18},
            'itemsizing': 'constant',
            'itemclick': 'toggleothers',
        }
    )

    fig.update_layout(
        title_text="<b>Followers vs VADER scores<b>",
        legend=dict(
            y=1,
            x=1.1
        ),
        margin=dict(t=40)
    )

    ## ADDITIONAL TEXT -- ANALYSIS ##
    additional_text = ""
    if 'Lufthansa' in value:
        additional_text = "The sentiment score fluctuates a lot with a dip in October 2019." \
                          "There’s an unusual peak in August of 2019. Amount of data probably causes fluctuations." \
                          "There is a steady increase in follower count despite strikes and other events." \
                          "The follower count implies exponential growth in the future." \
                          "No apparent correlation between sentiment score and follower count."


    elif 'KLM' in value:
        additional_text = "The sentiment score fluctuates a lot with dips in July 2019 and September 2019." \
                          "The September dip might be caused by strikes." \
                          "KLM has more data than Lufthansa to go on." \
                          "There is an increase in follower count in the second half of 2019." \
                          "The follower count drops at the start of 2020." \
                          "The changes in follower count are relatively small." \
                          "No apparent correlation between sentiment score and follower count."

    else:
        additional_text = "None"

    return fig, additional_text


@app.callback(
    Output('airline-lines', 'figure'),
    Input('my-dpdn3', 'value')
)
def update_graph(value):  #SENTIMENT
    dff = df_sent0[df_sent0['the_airline'].isin(value)]

    dff['month_year'] = dff['tweet_created_at'].apply(lambda x: str(x)[:7])
    dff = dff[(dff['month_year'] >= start_month) & (dff['month_year'] <= end_month)]
    dff2 = dff.groupby(['month_year', 'the_airline'], as_index=False)['Vader_com'].mean()

    fig = px.line(dff2, x="month_year", y="Vader_com", color='the_airline')

    fig.update_layout(
        xaxis={
            'title': {'text': 'Month and Year', 'font': {'size': 24}},
            'tickfont': {'size': 24}
        },
        yaxis=dict(
            title={'text': 'VADER score', 'font': {'size': 24}},
            tickfont={'size': 24}
        ),
        legend={
            'title': {'text': 'Airlines'},
            'font': {'size': 24},
            'itemsizing': 'constant',
        }
    )

    fig.update_layout(
        title_text="<b>Average Monthly VADER scores<b>"
    )

    return fig


# to run
if __name__ == '__main__':
    app.run_server(debug=True, port=8000)
