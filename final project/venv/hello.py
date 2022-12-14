from flask import Flask, jsonify, request, render_template
from elasticsearch import Elasticsearch
from elasticsearch_dsl import analyzer, tokenizer

es = Elasticsearch("http://localhost:9200")
app = Flask(__name__)

es.info()

# @app.route("/")
# def index():
#     print("hello world")
#     return 'Hello world'

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')

# @app.route("/create", methods=['GET', 'POST'])
# def create():
#     text = request.form.get("text")
#     print(text)
#     return render_template('search_result.html', par_1=text)

@app.route("/index", methods=['GET'])
def index():
    results = es.get(index='index_test8',id = "RH0B-YQB76KBthn_tPQo")
    print(results)
    return jsonify(results['_source'])

@app.route("/test", methods=['GET'])
def test():
    results = es.search(index='index_test8',size= 1000)
    print(len(results))
    return jsonify(results['hits']['hits'])

@app.route("/search", methods = ['GET','POST'])
def search():
    text_list = []
    text_list.append(request.form.get("text1"))
    text_list.append(request.form.get("text2"))
    text_list.append(request.form.get("text3"))
    # print(text_list)
    es.indices.refresh(index="index_test8")

    new_text_list = []
    for text in text_list:
        # print(text)
        new_text = "\"" + text + "\""
        new_text_list.append(new_text)
    print(new_text_list)
    text_string = '  OR  '.join(new_text_list)
    
    analyzer = analyzer{
        "analyzer": "stop",
        "tokenizer": "ngram",
        "lowercase": "true",
    }
    ranking = mappings{
    "properties": {
      "pagerank": {
        "type": "rank_feature"
      },
      "num_of_times_applied": {
        "type": "rank_feature",
        "positive_score_impact": "false"
      },
      "date_posted": {
        "type": "rank_features"
      }
    }
  }

    res = es.search(index = 'index_test8', size= 1000, _source=["Company","Title","Link"], analyzer=analyzer, ranking = ranking,
        query = {
            "bool":{
                "should":[
                    {
                    "query_string": {
                        "query": text_string                          
                    }},
                    {"range": {
                    "_timestamp": {
                            "gte": "2020-01-01T00:00:00",
                            "lte": "now"
                    }}
                }],
                "must_not":[
                    # { "query_string": {
                    #     "query": "\"years of experience\" OR \"years experience\" OR \"years of \" "                         
                    # }},
                    {"match": {
                        "Title": "Senior"            
                    }},
                    {"match": {
                        "Title": "Principal"            
                    }},
                    {"match": {
                        "Title": "Lead"            
                    }},
                    {"match": {
                        "Title": "Professor"            
                    }},
                    {"match": {
                        "Title": "Head"            
                    }},
                    {"match": {
                        "Title": "Sr"            
                    }},
                    {"match": {
                        "Title": "Manager"            
                    }},
                    {"match": {
                        "Title": "Intern"            
                    }},
                    {"match": {
                        "Title": "Data Scientist"            
                    }},
                    {"match": {
                        "Description": "years"            
                    }},
                    {"match": {
                        "Description": "Years"            
                    }},
                 ],
                }
            })
    # list = []
    # for hit in res['hits']['hits']:
    #     list.append(hit["_source"])
    print(len(res['hits']['hits']))
    return render_template('search_result.html', response_dict= res['hits']['hits'])
    # return jsonify(list)

if __name__ == '__main__':
    app.debug = True
    app.run()
