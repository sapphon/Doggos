from flask import *
import requests
import slack
import shutil
import os
import random
import sys

slack_token = os.environ['SLACK_API_TOKEN']
slack_bot_token = os.environ['SLACK_BOT_TOKEN']
try:
    proxy = os.environ['HTTP_PROXY']
except KeyError:
    proxy = ""
slack_client = slack.WebClient(token=slack_token, proxy=proxy)
labs_pets_channel_id = 'C7U8RMRC1'
app = Flask(__name__)

model = {
    'title': 'Pets of Fordlabs',
    'image_url': 'https://preview.redd.it/be1fc3tlo5031.jpg?width=640&crop=smart&auto=webp&s=8c9d0eff07da7f6eac8142c3bdfc13b2ab658e3c',
    'let_them_down_gently': "We're sorry, but the service you are using encountered a problem.",
    'heres_a_doggo': "To make up for it, we've got this cute pet to show you.",
    'error_intro': "If you'd like to know more about the error you encountered, here's what we've got:",
    'max_image_height': '600',
    'max_image_width': '600'
}


def choose_pet_image():
    return "static/" + random.choice(get_all_image_files_in_dir('static'))


def get_all_image_files_in_dir(dir):
    candidate_files = os.listdir('static')
    return list(filter(filename_denotes_image, candidate_files))


def filename_denotes_image(filename):
    file_types = ['jpg', 'jpeg', 'png', 'bmp', 'tif', 'tiff', 'gif']
    for type in file_types:
        if filename.endswith(type):
            return True
    return False


@app.route('/doggo', methods=['GET'])
def doggo():
    model['error_message'] = choose_error_message(request)
    model['image_url'] = choose_pet_image()
    return render_template('index.html', **model)


@app.route('/refresh', methods=['GET'])
def refresh():
    try:
        retrieve_pet_images()
    except:
        print("Unexpected error:", sys.exc_info()[1])
        return "failure"
    return "success"


def retrieve_pet_images():
    pets_history = slack_client.channels_history(channel=labs_pets_channel_id)
    file_messages = [x for x in pets_history['messages'] if is_image_message(x)]
    for n in range(len(file_messages)):
        doggo_private_slack_url = file_messages[n].get('files')[0].get('url_private')
        (_, file_extension) = os.path.splitext(doggo_private_slack_url)
        write_url_to_raw_file(doggo_private_slack_url, "testimage" + str(n) + file_extension)


def choose_error_message(error_page_request):
    return error_page_request.args.get('error') if error_page_request.args.get(
        'error') else '(Sorry, no additional information is available.)'


def is_image_message(message):
    return message.get('files') and message.get('files')[0].get('mimetype').startswith('image')


def write_url_to_raw_file(url, desired_file_name):
    response = requests.get(url, stream=True, headers={"Authorization": "Bearer " + slack_bot_token})
    print(response.status_code)
    print(response.headers['content-type'])
    with open('static/' + desired_file_name, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response


if __name__ == '__main__':
    port = int(os.getenv("PORT", 8080))
    app.run(host='0.0.0.0', debug=False, port=port)
