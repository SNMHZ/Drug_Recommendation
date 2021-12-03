from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import model
from mapping_drug import getDrugByCondition
from symptom_logic import getSymptoms
#from symptom_gpt import getSymptomsByCondition

app = Flask(__name__)
app.msg_json_data = {}
app.result = {}
CORS(app)

@app.route('/AndroidChatMessage', methods=['POST'])
def messageAccept():
    print("======================\nsuccess accept message\n======================")
    msg = request.get_json()
    print('--')
    print(msg)
    print('--')

    seq = msg['seq']
    text_body = msg['body']
    no_symptoms = list(map(lambda x: x[1:-1], msg['no_symptoms']))
    yes_symptoms = list(map(lambda x: x[1:-1], msg['yes_symptoms']))#msg['yes_symptoms']
    
    if app.debug:
        print("======================\ntext_body")
        print(seq)
        print(text_body)
        print(no_symptoms)
        print(yes_symptoms)
        print("======================")

    #text_body = """Weight loss Cramping Diarrhea Itchy skin Joint and muscle pain Nausea and vomiting Headaches"""
    try:
        for i, yes in enumerate(yes_symptoms):
            if i>0:
                text_body += 'and '
            else:
                text_body += '. '
            text_body += ' I have '+yes+'. '
        print('text_body:', text_body)
        result = model.pred_condition(text_body, seq, 20)
    except:
        result = {'res_type':'-1', 'symptoms':[], 'predict':{0:{'condition':'', 'prob':0.0}}}
    
    # if app.debug:
    #     print("======================\nresult")
    #     print(result)
    #     print("======================")
    
    current_date = str(datetime.datetime.now())
    type = result['res_type']
    predicts = result['predict']
    
    predicts_res = {}
    sym_word = ''
    print('--')
    print(type)
    print('--?')
    if seq == 10:
        type = 0
    if type == 0: # 예측 완료
        predicts_res[0] = predicts[0]
        predicts_res[1] = predicts[1]
        predicts_res[2] = predicts[2]
        predicts = predicts_res
    elif type == 1: # 예측 미완료
        sym_word = getSymptoms(predicts, no_symptoms, yes_symptoms)

    try:
        drugs = getDrugByCondition(predicts[0]['condition'])
    except:
        drugs = ["알 수 없는 질병입니다."]

    result_obj = jsonify({
                            "type": type,                 # -1: 에러, 0 : (예측 완료)예측 메시지, 1 : (예측 미완료)증상 리스트 전송
                            "seq": seq+1,                 # 이전 메시지 seq + 1
                            "date" : current_date,        # 서버 시간
                            "predicts": predicts,         # 예측 결과 top3 'condition', 'probability'
                            "no_symptoms": no_symptoms,   # 부정적 대답 증상 리스트
                            "yes_symptoms": yes_symptoms, # 긍정적 대답 증상 리스트
                            "sym_word": sym_word,         # 증상 단어
                            "drugs": drugs                # 약 정보
                        })
    
    if app.debug:
        print("result_obj:")
        print(result_obj.get_json())
        print()

    return result_obj

@app.route('/GetResult', methods=['GET'])
def getResult():
    if app.result[0] is not None:
        return app.result[0]
    else:
        error_msg = jsonify({"type": "-1", "body": "waiting", "date": 1,
                              "isClear": 1, "predicts": 1, "probs:": 1,
                              "symptoms": 1, "drugs": 1})
        return error_msg

'''
하단은 디버깅용 기능
'''

@app.route('/hello_world')
def hello_world():
    return 'Hello, World!'

@app.route('/GetTest1', methods=['GET'])
def get_test_one():
    jsonObj = app.msg[0]
    if jsonObj['body'] == 'symptom list':
        obj = jsonify({"type": "selection_msg", "body": "ADHD, Sore, Sick, Headache"})
        print("증상 리스트 전송")
        return obj
    else :
        obj = jsonify({"type": "result_msg", "body": jsonObj['body']+"에 대한 결과"})
        print("모델 예측 결과 메시지 전송")
        return obj

@app.route('/GetTest2', methods=['GET'])
def get_test_two():
    return jsonify({"msg" : "hellow android - from flask"})

@app.route('/users', methods=['GET']) #get echo api
def get_echo_call(param):
    print("client post 확인")
    return jsonify({"param": param})

@app.route('/echo_call', methods=['POST']) #post echo api
def post_echo_call():
    param = request.get_json()
    return jsonify(param)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    # app.run()


'''
import asyncio
import json

import websockets

async def accept(websocket, path):
    while True:
        print("server is running")
        data = await websocket.recv()
        json_object = json.loads(data)
        print("receive : " + json_object["body"])
        #await websocket.send(data)

start_server = websockets.serve(accept, "0.0.0.0", 9889)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
'''

