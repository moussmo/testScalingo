from flask import Flask

app = Flask(__name__)

@app.route('/test', methods=['GET'])
def test():
    return 'Hello World ! '

if __name__ == '__main__':
    print("Webhook démarré")
    app.run()