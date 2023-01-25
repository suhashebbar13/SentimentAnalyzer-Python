import requests
import csv
from lxml import html
from nltk.tokenize import sent_tokenize, word_tokenize, WordPunctTokenizer,SyllableTokenizer
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
import re

tl = SyllableTokenizer()
tk = WordPunctTokenizer()
filtered_list=[]
with open('Input.csv','r') as f:
    reader1= list(csv.reader(f))
    filename=''
    for i in reader1[1:]:
        filename = i[0] + '.txt'
        print(filename)
        headers = {
            'authority': 'insights.blackcoffer.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            # 'cookie': '___utma=2',
            # 'if-modified-since': 'Mon, 02 Jan 2023 06:19:56 GMT',
            'referer': 'https://www.google.com/',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        }

        response = requests.get(i[1],
            headers=headers,
        ).text
        tree = html.fromstring(response)
        path = tree.xpath("//header[@class='td-post-title']/h1[@class='entry-title']/text()")
        # subheading = tree.xpath("//div[@class='td-ss-main-content']/div[@class='td-post-content']/p/strong/text()")
        text1 = tree.xpath("//div[@class='td-ss-main-content']/div[@class='td-post-content']/p/text()")
        text2 = tree.xpath("//div[@class='td-ss-main-content']/div[@class='td-post-content']/p/span/text()")
        if len(text2)>1:
            text = text2
        else:
            text = text1
        if path:
            for k in text:
                open(filename, "a", encoding="utf-8").write(k)
                # print(str(k[0])+str(k[1]) + '\n')
            pos_count = 0
            neg_count = 0
            sent_count = 0
            neg_list = []
            pos_list = []
            syllable_count = 0
            cleanwords_count = 0
            vowels_count = 0
            personal_pronouns_count = 0
            total_no_words = 0
            vowels = {"a", "e", "i", "o", "u", "A", "E", "I", "O", "U"}
            with open('negative-words.txt', 'r') as neg:
                for neg_line in neg.readlines():
                    neg_list.append(neg_line.strip())
            with open('positive-words.txt', 'r') as pos:
                for pos_line in pos.readlines():
                    pos_list.append(pos_line.strip())
            for sentence in text:
                g = re.sub('[^a-zA-Z’.]+', ' ', sentence)
                sentence_in_text = sent_tokenize(g)
                sent_count += len(sentence_in_text)
                for k in sentence_in_text:
                    cleaned_text = re.sub('[^a-zA-Z’]+', ' ', k)
                    words_in_sent = re.sub('[^a-zA-Z’]+', ' ', cleaned_text).strip().split(' ')
                    # print(words_in_sent)
                    sia = SentimentIntensityAnalyzer()
                    stop_words = set(stopwords.words("english"))
                    for word in words_in_sent:
                        if (re.match(r"\bus\b|\bI\b|\bwe\b|\bmy\b|\bours\b", word)):
                            personal_pronouns_count += 1
                        if word not in stop_words:
                            total_no_words += len(word)
                            if vowels.intersection(word) and ('es' not in word or 'ed' not in word):
                                vowels_count += 1
                            cleanwords_count += 1
                        syllable = tl.tokenize(word)
                        if len(syllable) > 1:
                            syllable_count += 1
                        a = sia.polarity_scores(word)
                        filtered_list.append(word)
                        if word in neg_list:
                            neg_count += 1
                        if word in pos_list:
                            pos_count += 1

            pol_score = (pos_count - neg_count) / ((pos_count + neg_count) + 0.000001)
            subjectivity_score = (pos_count + neg_count) / ((cleanwords_count) + 0.000001)
            avg_sent_len = len(filtered_list) / sent_count
            per_complex_word = (syllable_count / len(filtered_list))
            fog_index = 0.4 * (avg_sent_len + per_complex_word)
            avg_word_len = total_no_words / cleanwords_count
            word_count = len(filtered_list)
            print([pos_count,neg_count, pol_score,subjectivity_score, avg_sent_len, per_complex_word, fog_index, avg_sent_len, syllable_count,word_count, vowels_count,personal_pronouns_count,avg_word_len])