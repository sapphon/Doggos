from flask import *
import requests
import slack
import shutil

slack_token = 'xoxp-addarealusertoken'
slack_bot_token = 'xoxb-addarealbottoken_forabotinthechannelyouwannause'
slack_client = slack.WebClient(token=slack_token)
app = Flask(__name__)

indexParameters = {
    'title': 'Pets of Fordlabs',
    'image_url': 'https://preview.redd.it/be1fc3tlo5031.jpg?width=640&crop=smart&auto=webp&s=8c9d0eff07da7f6eac8142c3bdfc13b2ab658e3c',
    'let_them_down_gently': "We're sorry, but the service you are using encountered a problem.",
    'heres_a_doggo': "To make up for it, we've got this cute pet to show you.",
    'error_intro': "If you'd like to know more about the error you encountered, here's what we've got:",
    'max_image_height': '600',
    'max_image_width': '600'
}
@app.route('/doggo', methods=['GET'])
def doggo():
    error_message = request.args.get('error')
    if not error_message:
        error_message = '(Sorry, no additional information is available.)'
    indexParameters['error_message'] = error_message
    pets_history = slack_client.channels_history(channel='C7U8RMRC1')
    file_messages = [x for x in pets_history['messages'] if is_image_message(x)]
    doggo_private_slack_url = file_messages[0].get('files')[0].get('url_private')

    indexParameters['error_message'] = error_message
    write_url_to_raw_file(doggo_private_slack_url, "testimage.jpg")
    indexParameters['image_url'] = "static/testimage.jpg"
    return render_template('index.html', **indexParameters)


def is_image_message(message):
    return message.get('files') and message.get('files')[0].get('mimetype').startswith('image')

def write_url_to_raw_file(url, desired_file_name):
    response = requests.get(url, stream=True, headers={"Authorization": "Bearer "+slack_bot_token})
    print(response.status_code)
    print(response.headers['content-type'])
    with open('static/'+desired_file_name, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

if __name__ == '__main__':
    app.run()

