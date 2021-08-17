from flask_restful import Resource, fields, reqparse, marshal
from tensorflow import keras
import tensorflow as tf
from APP.models import Result, RespBean
import tensorflow_addons as tfa
import pickle

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

def get_model():
    input = keras.layers.Input(shape=(max_len,))

    x = keras.layers.Embedding(4001, 100, input_length=max_len)(input)
    # [batch_size,max_length,2*units]
    h = keras.layers.Bidirectional(keras.layers.LSTM(100, return_sequences=True, recurrent_dropout=0.2))(x)
    fc = keras.layers.Dense(128, activation='relu')(h)
    fc = keras.layers.Dense(128, activation='relu')(fc)
    output = keras.layers.Dense(9, activation='softmax')(fc)
    model = keras.models.Model(input, output)
    # model.compile(optimizer=tfa.optimizers.RectifiedAdam(0.001),
    #               loss='categorical_crossentropy',
    #               metrics=['acc'])
    return model

class NerResource(Resource):
    def get(self):
        args = parser.parse_args()
        sentence = args.get('sentence')

        tag2label = {"O": 0,
                     "B-LOC": 1, "I-LOC": 2,
                     "B-KNG": 3, "I-KNG": 4,
                     "B-ORG": 5, "I-ORG": 6,
                     "B-PER": 7, "I-PER": 8,
                     }

        with open('APP/Api/NerModel/ner_dictionary.pkl','rb') as f:
            dictionary = pickle.load(f)
        f.close()

        model = get_model()
        model.load_weights('APP/Api/NerModel/ner_model.h5')

        send_id = []
        sentenceId = sentence2id(sentence, dictionary)
        send_id.append(sentenceId)
        padded_x = keras.preprocessing.sequence.pad_sequences(send_id, max_len)
        result = model.predict(padded_x)
        classes = get_classes(result[0], len(sentence))
        label2tag = dict(zip(tag2label.values(), tag2label.keys()))
        entities_tag = [label2tag[x] for x in classes]

        entities = list()

        entity = ''
        for i in range(len(entities_tag)):
            if entities_tag[i][0] == 'B':
                if entity != '':
                    entities.append(entity)
                entity = ''
                entity += sentence[i]
            elif entities_tag[i][0] == 'I':
                entity += sentence[i]
            else:
                if entity != '':
                    entities.append(entity)
                entity = ''

        if entity != '':
            entities.append(entity)
        final_entities = []
        for e in entities:
            final_entities.append(e)

        r = Result(final_entities)
        resp_bean = RespBean(200, 'success', r)

        return marshal(resp_bean,resp_bean_fields)