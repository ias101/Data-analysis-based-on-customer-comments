import csv
from textblob import TextBlob

store = []
with open('data_files/complete_data_with_vader.csv',encoding='gb18030',errors = 'ignore') as f:
    read = csv.DictReader(f)
    for i in read:
        store.append(dict(i))

for i in range(len(store)):
    new_blob = dict()
    text = store[i]['full_text']
    text_score = TextBlob(text)
    new_blob['tweet_id'] = store[i]['id_str']
    new_blob['full_text'] = store[i]['full_text']
    new_blob['polarity'] = text_score.sentiment[0]
    new_blob['subjectivity'] = text_score.sentiment[1]
    store[i] = new_blob

head = ['tweet_id', 'full_text', 'polarity', 'subjectivity']

with open('Text_blob.csv', mode = 'w', newline="",encoding='gb18030',errors = 'ignore') as f:
    writer = csv.DictWriter(f, head)
    writer.writeheader()
    writer.writerows(store)
