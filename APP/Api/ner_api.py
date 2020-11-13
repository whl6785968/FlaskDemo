from flask_restful import Resource, fields, reqparse, marshal
from tensorflow import keras

from APP.models import Result, RespBean

result_fields = {
    "result": fields.String
}

resp_bean_fields = {
    "status_code": fields.Integer,
    "msg": fields.String,
    "data": fields.Nested(result_fields)
}

parser = reqparse.RequestParser()
parser.add_argument("sentence",type=str,required=True,help="please input a sentence")
max_len=100

def sentence2id(seq, dictionary):
    sentence_id = []
    for word in seq:
        if word.isdigit():
            word = '<NUM>'
        elif ('\u0041' <= word <= '\u005a') or ('\u0061' <= word <= '\u007a'):
            word = '<ENG>'
        if dictionary.get(word, 0) == 0:
            index = 0
        else:
            index = dictionary[word]
        sentence_id.append(index)
    return sentence_id

def get_classes(output,sentence_len):
    classes = []
    for i in range(len(output)):
        max_index = 0
        for j in range(1,len(output[i])):
            if output[i][j] > output[i][max_index]:
                max_index = j
        classes.append(max_index)

    pad_len = max_len - sentence_len
    classes = classes[pad_len:]

    return classes

class NerResource(Resource):
    def get(self):
        args = parser.parse_args()
        sentence = args.get('sentence')

        tag2label = {"O": 0,
                      "B-PER": 1, "I-PER": 2,
                      "B-LOC": 3, "I-LOC": 4,
                      "B-ORG": 5, "I-ORG": 6
                      }

        filename = r'E:\PycharmProjects\smallFlaskDemo\APP\Api\NerModel\word2id.pkl'
        f = open(filename,'r',encoding='utf-8')
        a = f.read()
        dictionary =  eval(a)
        # words, target = self.get_data(dictionary)
        loaded_model = keras.models.load_model(r'E:\PycharmProjects\smallFlaskDemo\APP\Api\NerModel\ner_model.h5')
        send_id = []
        sentenceId = sentence2id(sentence, dictionary)
        send_id.append(sentenceId)
        padded_x = keras.preprocessing.sequence.pad_sequences(send_id, max_len)
        result = loaded_model.predict(padded_x)
        classes = get_classes(result[0], len(sentence))
        print(classes)
        label2tag = dict(zip(tag2label.values(), tag2label.keys()))
        final_result = [label2tag[x] for x in classes]

        r = Result(final_result)
        resp_bean = RespBean(200, 'success', r)

        return marshal(resp_bean,resp_bean_fields)