#import statements
import re
import nltk
from nltk.corpus import wordnet
from nltk.corpus import stopwords
import math
from collections import Counter
import pandas
from pandas import DataFrame
import openpyxl
import xlrd
#import itertools
#nltk.download()
#All global Varables
c=0
complete_List=[]
strq1=""
q1= " "
q2= " "
ques1=""
ques2=""
word_list=[]
word_list2=[]
q1_list=[]
q2_list=[]
test=[]
final_list=[]
#All functions

def text_to_word_list(text):
    text = str(text)
    text = text.lower()
    # Clean the text
    text = re.sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", text)
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r":"," ",text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "cannot ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text=re.sub(r"!"," ",text)
    text = re.sub(r",", " ", text)
    text = re.sub(r"\.", " ", text)
    text = re.sub(r"!", " ! ", text)
    text = re.sub(r"\/", " ", text)
    text = re.sub(r"\^", " ^ ", text)
    text = re.sub(r"\+", " + ", text)
    text = re.sub(r"\-", " - ", text)
    text = re.sub(r"\=", " = ", text)
    text = re.sub(r"'", " ", text)
    text = re.sub(r"(\d+)(k)", r"\g<1>000", text)
    text = re.sub(r":", " : ", text)
    text = re.sub(r" e g ", " eg ", text)
    text = re.sub(r" b g ", " bg ", text)
    text = re.sub(r"\0s", "0", text)
    text = re.sub(r" 9 11 ", "911", text)
    text = re.sub(r"e - mail", "email", text)
    text = re.sub(r"j k", "jk", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = text.split()
    return text
def ListToString(L):
    clean_input = " "
    for w in L:
        clean_input += w + " "
    return clean_input
def noise_remover(tag, word_list):
    for w in tag:
        if w[1] == 'WP' or w[1] == 'WRB' or w[1] == 'WDT' or w[1] == 'DT' or w[1] == 'IN' or w[1] == 'CC':
            word_list.remove(w[0])
        elif w[1] == 'VBZ' or w[1] == 'PRP$' or w[1] == 'PRP' or w[1] == 'VBP' or w[1] == 'MD' or w[1] == 'TO':
            word_list.remove(w[0])
def get_cosine(v1, v2):
    intersection = set(v1.keys()) & set(v2.keys())
    numerator = sum([v1[x] * v2[x] for x in intersection])
    sum1 = sum([v1[x] ** 2 for x in v1.keys()])
    sum2 = sum([v2[x] ** 2 for x in v2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator
def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)
def calc_syno_checker(l1, l2):
    list = []
    for word1 in l1:
        for word2 in l2:
            wordFromList1 = wordnet.synsets(word1)
            wordFromList2 = wordnet.synsets(word2)
            if wordFromList1 and wordFromList2:
                s = wordFromList1[0].wup_similarity(wordFromList2[0])
                list.append(s)
    return max(list)
def rem_dup(dup_list):
    f_list=[]
    for w in dup_list:
        if w not in f_list:
            f_list.append(w)
    return f_list
def syno_checker(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms.append(l.name())
    #syno=list(synonyms)
    #complete_List.append(syno)
    return synonyms
def syno_common_data(l1,l2):
    counter=0
    for x in l1:
        for y in l2:
            if str(x) == str(y):
                counter=1
    return counter
def string_cleaner(s):
    s2 = " "
    if str(s).startswith("u'"):
        s2 = str(s).replace("u'", " ", 1)
    return s2
df=pandas.read_excel('quora.xlsx')
v=df['question1'].values
v2=df['question2'].values
l=len(df)
for i in range(0,l):
    doc = str(v[i])
    doc2 = str(v2[i])
    text2 = text_to_word_list(doc)
    text_doc2=text_to_word_list(doc2)
    for w in text2:
        q1 += w +" "
        word_list.append(w)
    for w in text_doc2:
        q2 += w +" "
        word_list2.append(w)
    print "Doc1 word list:", word_list
    #print "Q1", q1
    print "Doc2 word lis:", word_list2
    length=len(word_list)
    length2=len(word_list2)
    tok=nltk.word_tokenize(q1)
    tag=nltk.pos_tag(tok)
    tok2=nltk.word_tokenize(q2)
    tag2=nltk.pos_tag(tok2)
    print "Tag 1:", tag
    print "Tag 2:", tag2
    noise_remover(tag, word_list)
    noise_remover(tag2, word_list2)
    print "After noise removal tag1:", tag
    print "Word after noise removal:", word_list
    print "After noise removal tag2:", tag2
    print "Word2 after noise removal:", word_list2
    WORD = re.compile(r'\w+')
    text1 = ListToString(word_list)
    text2 = ListToString(word_list2)
    s=set(stopwords.words('english'))
    text3=filter(lambda w: not w in s, text1.split())
    text4=filter(lambda w:not w in s, text2.split())
    print "cleaned question 1:",text3
    print "Cleaned question 2:",text4
    vector1 = text_to_vector(str(text3))
    vector2 = text_to_vector(str(text4))
    cosine = get_cosine(vector1, vector2)
    print 'Simiarity between q1 and q2 using Cosine similarity:', cosine
    all_q1=[]
    all_q2=[]
    for w in text3:
        all_q1.append(w)
    for w in text4:
        all_q2.append(w)
    print "Question 1"
    print all_q1
    print "Question 2"
    print all_q2
    uniq_q1=[]
    uniq_q2=[]
    uniq_q1=list(set(all_q1) - set(all_q2))
    uniq_q2=list(set(all_q2) - set(all_q1))
    print "Unique in q1"
    print uniq_q1
    print "Unique in q2"
    print uniq_q2
    if(bool(uniq_q1)==True) and (bool(uniq_q2)==True):
        print"both filled"
        for w in uniq_q1:
            q1_list = list(syno_checker(w))
        for w in uniq_q2:
            q2_list = list(syno_checker(w))
        print "Synonm of q1"
        print q1_list
        print "synonm of q2"
        print q2_list
        u_q1_list = rem_dup(q1_list)
        u_q2_list = rem_dup(q2_list)
        print "Unique synonm of q1"
        print u_q1_list
        print "Unique synonm of q2"
        print u_q2_list
        if(bool(u_q1_list) and bool(u_q2_list)):
            c=syno_common_data(u_q1_list,u_q2_list)
            if c==0:
                output=0
            else:
                output=1
        else:
            output=0
    elif(bool(uniq_q1)==False) and (bool(uniq_q2)==False):
        print "Nothing filled"
        output=cosine
    else:
        output=0
    final_list.append(output)
    print "Finale result"
    print final_list
    complete_List = []
    strq1 = ""
    q1 = ""
    q2 = ""
    ques1 = ""
    ques2 = ""
    word_list = []
    word_list2 = []
    q1_list = []
    q2_list = []
    text1 = ""
    text2 = ""
    text3 = ""
    text4 = ""
    all_q1 = []
    all_q2 = []
for i in range(1,l+1):
    test.append(i)
df=DataFrame({'test_id': test,'prob':final_list})
df.to_excel('Quora_output.xlsx',sheet_name='sheet1',index=False)
print "Inserted"