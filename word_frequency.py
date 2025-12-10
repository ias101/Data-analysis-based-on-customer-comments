import csv
import ast
import re


# discard emoji
def filter_str(desstr, restr=''):
    res = re.compile("[^\\u4e00-\\u9fa5^a-z^A-Z\\x20]")
    return res.sub(restr, desstr)


# search full text in result
def fibonacci_text_search(key, arr):
    fib_N_2 = 0  # F(k-2)
    fib_N_1 = 1  # F(k-1)
    fib_next = fib_N_1 + fib_N_2  # F(n)=F(n-1)+F(n-2)
    length = len(arr)

    while (fib_next < length):
        fib_N_2 = fib_N_1
        fib_N_1 = fib_next
        fib_next = fib_N_2 + fib_N_1

    offset = -1

    while (fib_next > 1):
        i = min(offset + fib_N_2, length - 1)
        if (arr[i]['id_str'] < key):
            fib_next = fib_N_1
            fib_N_1 = fib_N_2
            fib_N_2 = fib_next - fib_N_1
            offset = i
        elif (arr[i]['id_str'] > key):
            fib_next = fib_N_1
            fib_N_1 = fib_N_2
            fib_N_2 = fib_next - fib_N_1
        else:
            return arr[i]['full_text']

    if (fib_N_1 and offset < length - 1) and (arr[offset + 1]['id_str'] == key):
        return arr[offset + 1]['full_text']
    return 'NaN'


# store full text in a list (data structure: [{id:full_text},{id:full_text}...,{id:full_text}])
def open_file(path, store, result):
    with open(f'{path}') as f:
        read = csv.DictReader(f)
        for i in read:
            i = dict(i)
            i_1 = ast.literal_eval(i['full_conversation_vader'])
            if i_1[0] != 'NaN':
                a = fibonacci_text_search(i['id_str'], result)
                a = a.lower()
                a = filter_str(a)
                a = ' '.join(a.split())
                store.append({i['id_str']: a})


# main procedure
def word_frequency_func(word_list_1 = []):
    result = []
    store = []
    #dict_store = dict()
    #new_store = []
    with open('result.csv', mode='r', encoding='utf-8') as f:
        read = csv.DictReader(f)
        for i in read:
            result.append(dict(i))

    file_list = [
        'conversations_18332190_vader.csv',
        'conversations_20626359_vader.csv',
        'conversations_22536055_vader.csv',
        'conversations_26223583_vader.csv',
        'conversations_38676903_vader.csv',
        'conversations_45621423_vader.csv',
        'conversations_56377143_vader.csv',
        'conversations_106062176_vader.csv',
        'conversations_124476322_vader.csv',
        'conversations_218730857_vader.csv',
        'conversations_253340062_vader.csv',
        'conversations_1542862735_vader.csv']

    for j in file_list:
        open_file(j, store, result)
    """
    for k in store:
        for K_2 in k:
            k_1 = k[K_2].split()
            for word in k_1:
                if word not in dict_store:
                    dict_store[word] = 1
                else:
                    dict_store[word] += 1
    
    for words in dict_store:
        new_store.append({'word': words, 'frequency': dict_store[words]})
    
    head = ['word', 'frequency']
    with open('word_frequency.csv', mode="w", encoding="utf-8-sig", newline="") as f:
        write = csv.DictWriter(f, head)
        write.writeheader()
        write.writerows(new_store)
    """

    word_list = word_list_1

    word_com_dict = dict()
    for word_com in word_list:
        for str_dict in store:
            for str_id in str_dict:
                if word_com in str_dict[str_id]:
                    if word_com not in word_com_dict:
                        word_com_dict[word_com] = [str_id]
                    else:
                        word_com_dict[word_com].append(str_id)

    return word_com_dict
