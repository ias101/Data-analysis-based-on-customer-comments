from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import csv
# crate a list to store all vader score
vader_score = []
result = []
with open('data_files/complete_data_with_vader.csv',encoding='gb18030',errors = 'ignore') as f:
    read = csv.DictReader(f)
    for i in read:
        result.append(dict(i))


analyzer = SentimentIntensityAnalyzer()
# do sentimental analyz for each row in database
id = []
for i in result:
    if i['lang'] == 'en':
        vader_score.append(analyzer.polarity_scores(i['full_text']))
        id.append(i['id_str'])
    else:
        vs = {'neg': 'NaN', 'neu': 'NaN', 'pos': 'NaN', 'compound': 'NaN'}
        vader_score.append(vs)
        id.append(i['id_str'])

with open('vader.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["id_str", "Vader_neg", "Vader_neu", "Vader_pos", "Vader_com"])
    for i in range(len(id)):
        writer.writerow([id[i], vader_score[i]["neg"], vader_score[i]["neu"], vader_score[i]["pos"], vader_score[i]["compound"]])





