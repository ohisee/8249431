# -*- coding: utf-8 -*-
import logging;
import json;
import codecs;
from flask import Flask, render_template, request, Response, jsonify;

app = Flask(__name__)

@app.route('/')
def welcome():
    return 'hello first page';

@app.route('/see', methods=['GET'])
def render_home():
    return render_template('react.html');

@app.route('/es6', methods=['GET'])
def render_another_home():
    return render_template('reactes6.html');

@app.route('/visual', methods=['GET'])
def render_visualization():
    return render_template('d3chart.html');

@app.route('/seepost', methods=['GET', 'POST'])
def render_comments():
    newComment = [];
    if request.method == 'POST':
        data = request.form.to_dict();
        if data:
            newComment.append(data);

    with codecs.open('comments.json', 'r', encoding = 'utf-8') as fin:
        comments = fin.read();
        if comments:
            newComment = newComment + (json.loads(comments));

        if newComment:
            with codecs.open('comments.json', 'w', encoding = 'utf-8') as fout:
                fout.write(json.dumps(newComment, indent=2, separators=(',', ': ')));

    return Response(json.dumps(newComment if newComment else []),
                    mimetype='application/json',
                    headers={'Cache-Control': 'no-cache'});

# Run server with debug
if __name__ == '__main__':
    app.run(threaded=True,
    debug=True,
    host='0.0.0.0');
