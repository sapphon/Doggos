from flask import *

app = Flask(__name__)

indexParameters = {
    'title': 'Pets of Fordlabs',
    'corgi_url': 'https://preview.redd.it/be1fc3tlo5031.jpg?width=640&crop=smart&auto=webp&s=8c9d0eff07da7f6eac8142c3bdfc13b2ab658e3c',
    'let_them_down_gently': "We're sorry, but the service you are using encountered a problem.",
    'heres_a_doggo': "To make up for it, we've got this cute pet to show you.",
    'error_intro': "If you'd like to know more about the error you encountered, here's what we've got:"
}
@app.route('/doggo', methods=['GET'])
def hello_world():
    indexParameters['error_message'] = request.args.get('error')
    return render_template('index.html', **indexParameters)


if __name__ == '__main__':
    app.run()
