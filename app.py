from flask import *
import slack

app = Flask(__name__)
#client = Slack.WebClient(token=TOKENGOESHERE)
corgi_url = 'https://preview.redd.it/be1fc3tlo5031.jpg?width=640&crop=smart&auto=webp&s=8c9d0eff07da7f6eac8142c3bdfc13b2ab658e3c'

@app.route('/doggo', methods=['GET'])
def hello_world():
    error_message = request.args.get('error')
    return error_message


if __name__ == '__main__':
    app.run()
