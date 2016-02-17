from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/execute')
def write_to_local():
    f = open('test.txt', 'w')
    f.write('Executed!\n')
    f.close()

if __name__ == '__main__':
    app.run()
