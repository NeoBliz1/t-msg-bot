# import everything
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from telebot.credentials import bot_token, chat_id, app_url, telegram_api_url
import requests
import time
import datetime

recived_msgs = {}

app= Flask(__name__)
allow_origin = 'https://neobliz1.github.io'
CORS(app, resources={r'/*': {'origins': allow_origin}})
#CORS(app)
#post msg to telegramm
@app.route('/post_msg',  methods=['POST'])
def send_message():
        get_request_origin = request.environ.get('HTTP_ORIGIN', 'default value')
        #print(get_request_origin)
        if allow_origin == get_request_origin:
                content = request.get_json(force=True)
                # print('origins are identical')
                # print(f'A {content[0]["value"]} is is calling you master')
                # print(f'He told you: {content[1]["value"]}')          
                # url for the send msg
                get_url = f'{telegram_api_url}/bot{bot_token}/sendMessage'
                # print(get_url)
                bot_msg1 = f'A {content[0]["value"]} is calling you master'
                bot_msg2 = f'He wrote you: {content[1]["value"]}'
                PARAMS1={}
                PARAMS2={}
                PARAMS1 = {'chat_id':chat_id,
                        'text':bot_msg1
                }
                PARAMS2 = {'chat_id':chat_id,
                        'text':bot_msg2
                }
                r1 = requests.get(url = get_url, params = PARAMS1)
                r2 = requests.get(url = get_url, params = PARAMS2)
                # print(r1)
                # print(r2)
                # data1 = r1.json()
                # data2 = r2.json()
                # print(data1)
                # print(data2)
                response = {}
                response["MESSAGE"] = f"The {content} is sending!!"
return jsonify(response)
        else:
                #print('origins are not identical')
                response = {}
                response["MESSAGE"] = f"The {get_request_origin} is not allowed!!"
                return jsonify(response)        

@app.route('/get_msg',  methods=['GET'])
def get_message():
        get_request_origin = request.environ.get('HTTP_ORIGIN', 'default value')
        if allow_origin == get_request_origin:          
                response = {}           
                response = recived_msgs.copy()
                recived_msgs.clear()
                return jsonify(response)
        else:
                return "<h1>You can't access the data</h1>"             
        

route_to_post_from_telegramm = f'/{bot_token}'
@app.route(route_to_post_from_telegramm, methods=['POST'])
def respond():  
        tCurrent = time.time()
        # print (tCurrent)
        st = datetime.datetime.fromtimestamp(tCurrent).strftime('%Y-%m-%d %H:%M:%S')
        # print (st)
        # retrieve the message in JSON and then transform it to Telegram object
        update = request.get_json(force=True)           
        #print(update)
        # Telegram understands UTF-8, so encode text for unicode compatibility
        text = update['message']['text'].encode('utf-8').decode()       
        #print(text)
        recived_msgs[st] = text
        #print(recived_msgs)
        return 'ok'

@app.route('/setup_webhook', methods=['GET'])
def set_webhook():
        set_webhook_url = f'{telegram_api_url}/bot{bot_token}/setWebhook'       
        PARAMS = {}
        url_post_response = f'{app_url}/{bot_token}'
        PARAMS = {'url':url_post_response}
        s = requests.get(url = set_webhook_url, params = PARAMS)
        if s:
                return "<h1>webhook setup ok!</h1>"
        else:
                return "<h1>webhook setup failed</h1>"

@app.route('/remove_webhook', methods=['GET', 'POST'])
def remove_webhook():
        remove_webhook_url = f'{telegram_api_url}/bot{bot_token}/deleteWebhook'         
        r = requests.get(url = remove_webhook_url)
        if r:
                return "<h1>webhook remove success</h1>"
        else:
                return "<h1>webhook remove failed</h1>"

@app.route('/webhook_info', methods=['GET', 'POST'])
def get_webhook_info():
        #return "<h1>webhook info working</h1>"
        set_webhook_url = f'{telegram_api_url}/bot{bot_token}/getWebhookInfo'           
        w_i = requests.get(set_webhook_url)
        data = w_i.json() 
        if w_i:
                return data
        else:
                return "<h1>webhook info failed</h1>"


# A welcome message to test our server
@app.route('/')
def index():
        return "<h1>Resending botApp has been started!!</h1>"
# check msg
@app.route('/check_msg')
def check_msg():
        return "<h1>Another tab is working!!</h1>"
                 
if __name__ == '__main__':
        app.run(threaded=True)


