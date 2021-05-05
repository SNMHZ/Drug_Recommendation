from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/test', methods=['GET', 'POST'])
def test():
    return 'TEST'


if __name__ == '__main__':
    # app.debug = True
    app.run()
