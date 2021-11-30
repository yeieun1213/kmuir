
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

def make_dataList(root):
    f = open(root, mode='rt', encoding='utf-8')
    dataList = []
    while (True):
        line = f.readline()
        if not line:
            break
        d = re.split('\t', line)
        d[2] = re.split('\n', d[2])[0]
        dataList.append(d[1])
    #print(len(dataList))
    #print(dataList[10:])
    f.close()
    return dataList

def make_01(root):
    f = open(root, mode='rt', encoding='utf-8')
    dataList = []
    while (True):
        line = f.readline()
        if not line:
            break
        d = re.split('\t', line)
        d[2] = re.split('\n', d[2])[0]
        dataList.append(d[2])
    f.close()
    return dataList


def tokenizer_store_function(DataList):
    ascii = re.compile(r'[^ 0-9가-힣+]')
    ascii_token = set()
    bigram = []
    token = []

    # a. 아스키 문자열 분리
    # b. 한글 이외 문자열 분리
    word = ''
    dd = DataList

    if len(dd) < 1:
        print("error: ", dd)
    n = -1
    ddd = dd
    b = ''
    for s in ascii.finditer(dd):
        # print(s)
        ddd = ddd.replace(s.group(), ' ')
        if (n == s.span()[0]):
            word += s.group()
            n = s.span()[1]
        else:
            n = s.span()[1]
            if len(word) != 0:
                ascii_token.add(word)
                word = s.group()
            else:
                word = s.group()

    if len(word) != 0:
        ascii_token.add(word)
        b = b + ' ' + word
    if len(ascii_token) != 0:
        print(ascii_token, file=a)
    #data.append(ddd)

    d = ddd.split()

    token.append(d)
    for j in range(len(d)):
        for k in range(len(d[j])):
            if (k == 0) and (k == len(d[j]) - 1):
                b = b + ' ' + "_" + d[j][k] + "_"
            elif (k == 0):
                b = b + ' ' + "_" + d[j][k]
                b = b + ' ' + d[j][k] + d[j][k + 1]
            elif (k == len(d[j]) - 1):
                b = b + ' ' + d[j][k] + "_"
            else:
                b = b + ' ' + d[j][k] + d[j][k + 1]
    bigram.append(b)



    if len(bigram) != 0:
        print(bigram, file=t)

    return b


def tokenizer_function(DataList):
    ascii = re.compile(r'[^ 0-9가-힣+]')
    ascii_token = set()
    bigram = []
    token = []
    data = []

    # a. 아스키 문자열 분리
    # b. 한글 이외 문자열 분리
    word = ''
    dd = DataList

    if len(dd) < 1:
        print("error: ", dd)
    n = -1
    ddd = dd
    b = ''
    for s in ascii.finditer(dd):
        # print(s)
        ddd = ddd.replace(s.group(), ' ')
        if (n == s.span()[0]):
            word += s.group()
            n = s.span()[1]
        else:
            n = s.span()[1]
            if len(word) != 0:
                ascii_token.add(word)
                word = s.group()
            else:
                word = s.group()

    if len(word) != 0:
        ascii_token.add(word)
        b = b + ' ' + word

    d = ddd.split()

    token.append(d)
    for j in range(len(d)):
        for k in range(len(d[j])):
            if (k == 0) and (k == len(d[j]) - 1):
                b = b + ' ' + "_" + d[j][k] + "_"
            elif (k == 0):
                b = b + ' ' + "_" + d[j][k]
                b = b + ' ' + d[j][k] + d[j][k + 1]
            elif (k == len(d[j]) - 1):
                b = b + ' ' + d[j][k] + "_"
            else:
                b = b + ' ' + d[j][k] + d[j][k + 1]
    bigram.append(b)

    return b



a = open('ascii_token.txt', mode='wt', encoding='utf-8')
t = open('token.txt', mode='wt', encoding='utf-8')
dataList = make_dataList('ratings.txt')
dataList = dataList[1:]
dataList_01 = make_01('ratings.txt')
dataList_01 = dataList_01[1:]
token_bigram=[]

for i in range(len(dataList)):
    b = tokenizer_store_function(dataList[i])
    token_bigram.append(b)
a.close()
t.close()
print(token_bigram[:10])



vect = CountVectorizer(ngram_range=(1,1), lowercase=False)
X = vect.fit_transform(token_bigram)
print("X: ", X.shape)
print("X: ", X[0].A.shape)
vectorizer = TfidfVectorizer(ngram_range=(1,1), lowercase=False)
Z = vectorizer.fit_transform(token_bigram)
print("Z: ", Z.shape)
print("Z: ", Z[0].A.shape)

print("total data token success")
a.close()
t.close()
dicZ = dict(zip(vectorizer.get_feature_names_out(), vectorizer.idf_))

print("train data start")
train_dataList = make_dataList('ratings_train.txt')
train_dataList = train_dataList[1:]
train_01_data = make_01('ratings_train.txt')
train_01_data = train_01_data[1:]
token_bigram=[]
for i in range(len(train_dataList)):
    b = tokenizer_function(train_dataList[i])
    token_bigram.append(b)
vect = CountVectorizer(ngram_range=(1,1), lowercase=False)
X = vect.fit_transform(token_bigram)
Z = vectorizer.fit_transform(token_bigram)
dicZ = dict(zip(vectorizer.get_feature_names_out(), vectorizer.idf_))

f_train = open('train_output.txt', 'wt', encoding='utf-8')
for j in range(X.shape[0]):
    l = train_01_data[j]
    for i in range(len(X[j].A[0])):
        if X[j].A[0][i] != 0:
            l = l + " " + vectorizer.get_feature_names_out()[i]  + "(" + str(i) + "): " + str(X[j].A[0][i]*dicZ[vectorizer.get_feature_names_out()[i]]) + ", "
    print(j, l)
    print(l, file=f_train)
f_train.close()
print("train data end")

test_dataList = make_dataList('ratings_test.txt')
test_dataList = test_dataList[1:]
test_01_data = make_01('ratings_test.txt')
test_01_data = test_01_data[1:]
token_bigram=[]
for i in range(len(train_dataList)):
    b = tokenizer_function(train_dataList[i])
    token_bigram.append(b)
vect = CountVectorizer(ngram_range=(1,1), lowercase=False)
X = vect.fit_transform(token_bigram)
Z = vectorizer.fit_transform(token_bigram)
dicZ = dict(zip(vectorizer.get_feature_names_out(), vectorizer.idf_))

f_test = open('test_output.txt', 'wt', encoding='utf-8')
for j in range(X.shape[0]):
    l = test_01_data[j]
    for i in range(len(X[j].A[0])):
        if X[j].A[0][i] != 0:
            l = l + " " + vectorizer.get_feature_names_out()[i]  + "(" + str(i) + "): " + str(X[j].A[0][i]*dicZ[vectorizer.get_feature_names_out()[i]]) + ", "
    print(j, l)
    print(l, file=f_test)
f_test.close()
print("test data end")





"""
#vectorizer = TfidfVectorizer(tokenizer=tokenizer_function, lowercase=False)

#Z = vectorizer.fit_transform(dataList)
print("Z: ", Z.shape)
print("Z: ", Z[0].A.shape)
print("total data token success")
a.close()
t.close()

for j in range(Z.shape[0]):
    l = dataList_01[j]

    for i in range(len(Z[j].A[0])):
        if Z[j].A[0][i] != 0:
            l = l + " " + vectorizer.get_feature_names_out()[i] + "(" + str(i) + "): " + str(Z[j].A[0][i]) + ", "
    print(j, l)

"""
"""
t = open('token.txt', mode='rt', encoding='utf-8')
bigram_token = []
while(True):
    line = t.readline().split('\n')[0]
    if not line:
        break
    for i in range(2, len(line), 6):
        bigram_token.append(line[i:i+2])
t.close()
print(bigram_token[:10])


test_dataList = make_dataList('ratings_test.txt')
test_dataList = test_dataList[1:]
test_01_data = make_01('ratings_test.txt')
test_01_data = test_01_data[1:]

train_dataList = make_dataList('ratings_train.txt')
train_dataList = train_dataList[1:]
train_01_data = make_01('ratings_train.txt')
train_01_data = train_01_data[1:]
print("test_data", len(test_dataList))
print(test_dataList[:10])
print("train_data", len(train_dataList))
print(train_dataList[:10])

def tok(data):
    return data
vectorizer = TfidfVectorizer(tokenizer=tok, lowercase=False)


vectorizer = TfidfVectorizer(tokenizer=tokenizer_function, lowercase=False)
Y = vectorizer.fit_transform(train_dataList)
#print(vectorizer.vocabulary_)
print("Y: ", Y.shape)
print("Y: ", Y[0].A.shape)
print(len(train_01_data))
print("train fit_transform success")
f_train = open('output_train.txt', mode='wt', encoding='utf-8')
for j in range(Y.shape[0]):
    l = train_01_data[j]

    for i in range(len(Y[j].A[0])):
        if Y[j].A[0][i] != 0:
            l = l + " " + vectorizer.get_feature_names_out()[i] + "(" + str(i) + "): " + str(Y[j].A[0][i]) + ", "
    print(j, l)
    print(l, file=f_train)
f_train.close()
print("f_train success")


X = vectorizer.fit_transform(test_dataList)
print("X: ", X.shape)
print("X: ", X[0].A.shape)
print(len(test_01_data))
print("test fit_transform success")




f_test = open('output_test.txt', mode='wt', encoding='utf-8')
for j in range(X.shape[0]):
    l = test_01_data[j]

    for i in range(len(X[j].A[0])):
        if X[j].A[0][i] != 0:
            l = l + " " + vectorizer.get_feature_names_out()[i] + "(" + str(i) + "): " + str(X[j].A[0][i]) + ", "
    print(j, l)
    print(l, file=f_test)
f_test.close()
print("f_test success")

print("DONE")
#print(
#    'fit_transform, (sentence {}, feature {})'.format(X.shape[0], X.shape[1])
#)
"""