import pickle

from flask_restful import Resource, fields, reqparse, marshal
from sklearn.metrics.pairwise import cosine_similarity

from APP.models import Result, RespBean
from py2neo import Graph
import jieba
import requests
import numpy as np

result_fields = {
    "result": fields.String
}

resp_bean_fields = {
    "status_code": fields.Integer,
    "msg": fields.String,
    "data": fields.Nested(result_fields)
}

parser = reqparse.RequestParser()
parser.add_argument("question",type=str,required=True,help="question")

def query_graph(query):
    graph = Graph('bolt://localhost:7687')
    records = graph.run(query).data()
    sents = []

    for record in records:
        type = str(record.get('n').labels).split(":")[1]
        start_node = record.get('n').get('name')
        end_node = record.get('m').get('name')
        if type == 'Knowledge':
            relation = record.get('r').get('real_relation')
            flag = 'kng'
        else:
            l = []
            types = record.get('r').types()
            for t in types:
                l.append(t)
            relation = l[0]
            flag = 'other'

        sents.append((flag,start_node,relation,end_node))
    return sents

class QAApi(Resource):
    def get(self):
        args = parser.parse_args()
        question = args.get('question')
        url = 'http://localhost:5000/ner?sentence=' + question
        response_ner = requests.request('get',url)
        response_ner = response_ner.json()
        ner_res = response_ner.get('data').get('result')
        ner_res = ner_res.replace('[', '').replace(']', '').replace("'", '').split(',')


        entity = ner_res[0]

        templates = ['%s的%s是什么？', '什么是%s的%s', '%s%s', '%s的%s', '%s的%s有哪些', '哪些是%s的%s', '%s需要哪些%s']
        templates_un_kng = ['%s%s哪里？','%s由%s?']
        train_sentence = []
        qa_map = {}
        questions = []

        query = "match (n)-[r]->(m) where n.name = '" + entity + "' or m.name = '" + entity + "' return n,r,m"
        sents = query_graph(query)

        for s in sents:
            flag,start_node,relation,end_node = s
            if flag == 'kng':
                for kt in templates:
                    q = kt % (start_node,relation)
                    qa_map[q] = start_node + '的' + relation + '是' + end_node
                    questions.append(q)
                    train_sentence.append(' '.join(jieba.cut(q)))
            else:
                for ko in templates_un_kng:
                    question = ko % (start_node,relation)
                    qa_map[question] = start_node + relation + end_node
                    questions.append(question)
                    train_sentence.append(' '.join(jieba.cut(question)))

        with open('APP/Api/vecModel/vec_model.pkl','rb') as f:
            vec_model = pickle.load(f)
        f.close()

        sent_list = [' '.join(jieba.cut(question))]
        sl = vec_model.transform(sent_list)
        ts = vec_model.transform(train_sentence)
        sim = cosine_similarity(sl, ts)[0]

        most_sim = np.argsort(-sim)[0:5]

        rs = []
        for i in most_sim:
            rs.append("答案：" + qa_map[questions[i]] + "|相似度分数：" + str(sim[i]))

        r = Result(rs)
        resp_bean = RespBean(200, 'success', r)

        return marshal(resp_bean, resp_bean_fields)