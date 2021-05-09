from flask import Flask, request
from flask_cors import CORS
import predictor_model3 as pm

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/test', methods=['POST'])
def test():
    msg = request.get_json(force=True)

    lemed_msg = pm.lemlem(msg['text'])
    tmp = pm.predictConditionSum(lemed_msg)
    m_sorted_res = sorted(list(tmp.items()), key=lambda x:x[1], reverse=True)[:1000]

    r_msg=''
    for res in m_sorted_res[:1]:
        r_msg+='( condition : '+res[0]+" / "+pm.findDrugName(res[0])+' ) \n '
        
    #컨디션만 리턴
    # r_msg=''
    # for i, res in enumerate(m_sorted_res):
    #     if pm.isincheck(res[0]):
    #         r_msg+=res[0]+' '

    return {
        "text" : r_msg
    }


if __name__ == '__main__':
    app.debug = True
    app.run()