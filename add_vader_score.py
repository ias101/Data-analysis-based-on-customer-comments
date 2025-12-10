import csv
import ast

def fibonacci_search(key, arr):
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
            return arr[i]['Vader_com']  
    if (fib_N_1 and offset < length - 1) and (arr[offset + 1]['id_str'] == key):
        return arr[offset + 1]['Vader_com']
    return -1000 



vader = []
with open('E:\dbl-data-challenge\\vader.csv') as f:
    read = csv.DictReader(f)
    for i in read:
        vader.append(dict(i))




n = 0
new = []
headers = []
with open('E:\dbl-data-challenge\conversations_1542862735', mode='r') as f:
    air_read = csv.DictReader(f)
    for i in air_read:
        i_1 = dict(i)
        tem = []
        a = ast.literal_eval(i_1['full_conversation_ids'])
        for j in a:
            tem.append(fibonacci_search(j,vader))
        i_1['full_conversation_vader'] = tem
        new.append(i_1)
        n += 1
    headers = list(new[0].keys())

headers = tuple(headers)
with open('conversations_1542862735_vader.csv','w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, headers)
    writer.writeheader()
    writer.writerows(new)




