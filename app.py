from flask import Flask, render_template, request, jsonify
from auth import *
import asyncio
from multiprocessing import Process


app = Flask(__name__, static_folder='static', template_folder='templates', static_url_path='')

client = None
api = None
loop = None
# app.static_folder = "templates"

@app.route('/')
def index():
    return render_template('index.html', context=None)

@app.route('/send_code', methods=['GET', 'POST'])
def send_code():

    global client, api, loop

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)    
    
    phone_number = request.json['phone']
    
    client, api = auth_send_code(phone_number, loop)

    return "OK"

@app.route('/confirm_code', methods=['GET', 'POST'])
def confirm_code():

    global client, api, loop

    code = request.json['code']
    phone_number = request.json['phone']

    auth_create_session((client, api), phone_number, code, loop)

    return "OK"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)