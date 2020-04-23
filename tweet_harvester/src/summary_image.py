from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
import time
import PIL_example

import db_utils
#step 1.Create the word frequency table
def _create_frequency_table(text_string) -> dict:

    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text_string)
    ps = PorterStemmer()

    freqTable = dict()
    for word in words:
        word = ps.stem(word)
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    return freqTable

# step 2. Tokenize the sentences
#sent_tokenize(text_string)

# step 3. Score the sentences: Term frequency
def _score_sentences(sentences, freqTable) -> dict:
    sentenceValue = dict()

    for sentence in sentences:
        word_count_in_sentence = (len(word_tokenize(sentence)))
        for wordValue in freqTable:
            if wordValue in sentence.lower():
                if sentence[:10] in sentenceValue:
                    sentenceValue[sentence[:10]] += freqTable[wordValue]
                else:
                    sentenceValue[sentence[:10]] = freqTable[wordValue]

        sentenceValue[sentence[:10]] = sentenceValue[sentence[:10]] // word_count_in_sentence

    return sentenceValue

# step 4. Find the threshold
def _find_average_score(sentenceValue) -> int:
    sumValues = 0
    for entry in sentenceValue:
        sumValues += sentenceValue[entry]

    # Average value of a sentence from original text
    average = int(sumValues / len(sentenceValue))

    return average

# step 5. Generate the summary
def _generate_summary(sentences, sentenceValue, threshold):
    sentence_count = 0
    summary = ''

    for sentence in sentences:
        if sentence[:10] in sentenceValue and sentenceValue[sentence[:10]] > (threshold):
            summary += " " + sentence
            sentence_count += 1

    return summary


# let us all above functions and summarize the text_string
#with open('raw_text.txt','r',encoding="utf8") as mf:
#    text = mf.read()
#print(len(text))

#from pymongo import MongoClient

#client = MongoClient()
#updates_coll = client.tweeter_db.updates
#main_col = client.tweeter_db.news_tweets

def main():
    client = db_utils.connect()
    data=[]
    dat_for_filter = time.strftime("%Y%m%d")
    data.append( " ".join([item['cleaned_text'] for item in client.tweeter_db.news_tweets.find({'$and':[{'cleaned_text':{'$regex':'lockdown','$options':'i'}},
                                                                    {'tmstamp':{'$regex':'^'+dat_for_filter+'.*'}}]},{'cleaned_text':1,'_id':0})]))
    data.append( ". ".join([item['cleaned_text'] for item in client.tweeter_db.news_tweets.find({'$and':[{'cleaned_text':{'$regex':'lockdown','$options':'i'}},
                                                                    {'tmstamp':{'$regex':'^'+dat_for_filter+'.*'}}]},{'cleaned_text':1,'_id':0})]))
    client = None
    summary_text = ""
    if len(data) >0:
        for text in data:
            # 1 Create the word frequency table
            freq_table = _create_frequency_table(text)

            '''
            We already have a sentence tokenizer, so we just need
            to run the sent_tokenize() method to create the array of sentences.
            '''

            # 2 Tokenize the sentences
            sentences = sent_tokenize(text)

            # 3 Important Algorithm: score the sentences
            sentence_scores = _score_sentences(sentences, freq_table)

            # 4 Find the threshold
            threshold = _find_average_score(sentence_scores)

            # 5 Important Algorithm: Generate the summary
            summary = _generate_summary(sentences, sentence_scores, 1.5 * threshold)
            summary_text = summary_text+" "+summary
            #print(summary)


    print(f"lenght of the text: {len(summary_text)} complete summary : {summary_text}")
    PIL_example.generate_image(summary_text)

if __name__=="__main__":
    main()
