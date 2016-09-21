import os
import requests
import operator
import re
import nltk
from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from stop_words import stops
from collections import Counter
from bs4 import BeautifulSoup
from nltk import FreqDist
import json
from flask import Flask, jsonify

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


@app.route('/<name>')
def hello_name(name):
    print (name)
    return "Hello {}!".format(name)


@app.route('/nltk', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}

    if 'url' in request.args:
         url = request.args['url']
         print (url)
    if request.method == "GET":
        # get url that the person has entered
        try:
            #url = urlParse
	        r = requests.get(url)
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
            return render_template('index.html', errors=errors)
        if r:
            # text processing
            raw = BeautifulSoup(r.text, 'html.parser').get_text()
            nltk.data.path.append('./nltk_data/')  # set the path
            tokens = nltk.word_tokenize(raw)
            text = nltk.Text(tokens)
            # remove punctuation, count raw words
            nonPunct = re.compile('.*[A-Za-z].*')
            raw_words = [w for w in text if nonPunct.match(w)]
            raw_word_count = Counter(raw_words)
            # stop words
            no_stop_words = [w for w in raw_words if w.lower() not in stops]
            #no_stop_words_count = Counter(no_stop_words)
            no_stop_words_count = FreqDist(no_stop_words).most_common(5)
            #print ("raw:", raw_word_count)
            rs1 =list(map(lambda x: {'word': x[0], 'count':x[1] }, no_stop_words_count))
            rs = {'data': rs1}
            print (rs)

    return  jsonify(rs)


if __name__ == '__main__':
    app.run()
