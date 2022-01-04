from flask import Flask
import os

port = os.getenv("PORT")
app = Flask(__name__)

@app.route('/test', methods=['GET'])
def test():
    return 'Hello World ! '

if __name__ == '__main__':
    print("Webhook démarré")
    app.run(host='0.0.0.0', port=port)