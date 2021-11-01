from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime

app = Flask(__name__)
app.msg_json_data = {}
app.result = {}
CORS(app)

@app.route('/AndroidChatMessage', methods=['POST'])
def messageAccept():
    print("success accept message")
    app.msg_json_data[0] = request.get_json()
    msg = request.get_json()

    text_body = msg['body']
    '''
    텍스트 전처리나 preprocessing
    '''
    result = modelPrediction(text_body) # model 예측
    current_date = str(datetime.datetime.now())
    isClear = True
    symptoms = None
    drugs = None
    predicts = None
    probs = None

    result_obj = jsonify({"type": "1", "body": result, "date" : current_date,
                          "isClear": isClear, "predicts": predicts, "probs:": probs,
                          "symptoms": symptoms, "drugs": drugs})

    print(result_obj.get_json())
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
    app.run()


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

