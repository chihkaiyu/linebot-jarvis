# -*- coding: utf-8 -*-

import sys
import os
from weatherParser.weather import *

from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)
from linebot.utils import PY3

channel_secret = os.getenv('CHANNEL_SECRET', None)
channel_access_token = os.getenv('CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

def callback(environ, start_response):
    # for ELB
    if environ['PATH_INFO'] == '/callback' and environ['REQUEST_METHOD'] == 'GET':
        start_response('200 OK', [])
        return create_body('OK')

    # check request path
    if environ['PATH_INFO'] != '/callback':
        start_response('404 Not Found', [])
        return create_body('Not Found')

    # check request method
    if environ['REQUEST_METHOD'] != 'POST':
        start_response('405 Method Not Allowed', [])
        return create_body('Method Not Allowed')

    # get X-Line-Signature header value
    signature = environ['HTTP_X_LINE_SIGNATURE']

    # get request body as text
    wsgi_input = environ['wsgi.input']
    content_length = int(environ['CONTENT_LENGTH'])
    body = wsgi_input.read(content_length).decode('utf-8')
    
    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        start_response('400 Bad Request', [])
        return create_body('Bad Request')

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        command = event.message.text.split(' ')
        if command[0] == u'天氣':
            res = getWeather(command[1:])
            display = ''.join(command[1:]) + '\n'
            if res['numCol'] == 8:
                display += ''.join(res['date']) + '\n'
                display += u'時間    ' + u'溫度   ' + u'降雨機率' + '\n'
                for i in range(8):
                    display += res['time'][i] + '  ' + res['temp'][i] + '     ' + res['rainprob'][i] + '\n'
            else:
                for j in range(2):
                    display += ''.join(res['date'][j]) + '\n'
                    display += u'時間    ' + u'溫度   ' u'降雨機率' + '\n'
                    for i in range(res['numCol'][j]):
                        display += res['time'][i] + '  ' + res['temp'][i] + '     ' + res['rainprob'][i] + '\n'

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=display)
        )

    start_response('200 OK', [])
    return create_body('OK')

def create_body(text):
    if PY3:
        return [bytes(text, 'utf-8')]
    else:
        return text
