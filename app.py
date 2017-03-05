#!/usr/bin/env python3
# -*- coding: utf8 -*-

import sys
import os
from weatherParser import weather
from metroParser import metro

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

class lineServer(object):
    def __init__(self):
        channel_secret = os.getenv('CHANNEL_SECRET', None)
        channel_access_token = os.getenv('CHANNEL_ACCESS_TOKEN', None)
        if channel_secret is None:
            print('Specify LINE_CHANNEL_SECRET as environment variable.')
            sys.exit(1)
        if channel_access_token is None:
            print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
            sys.exit(1)
        self.line_bot_api = LineBotApi(channel_access_token)
        self.parser = WebhookParser(channel_secret)

    def callback(self, environ, start_response):
        '''
        # for ELB
        if environ['PATH_INFO'] == '/callback' and environ['REQUEST_METHOD'] == 'GET':
            start_response('200 OK', [])
            return create_body('OK')
        '''
        
        # check request path
        if environ['PATH_INFO'] != '/callback':
            start_response('404 Not Found', [])
            return self.create_body('Not Found')

        # check request method
        if environ['REQUEST_METHOD'] != 'POST':
            start_response('405 Method Not Allowed', [])
            return self.create_body('Method Not Allowed')

        # get X-Line-Signature header value
        signature = environ['HTTP_X_LINE_SIGNATURE']

        # get request body as text
        wsgi_input = environ['wsgi.input']
        content_length = int(environ['CONTENT_LENGTH'])
        body = wsgi_input.read(content_length).decode('utf-8')
        
        # parse webhook body
        try:
            events = self.parser.parse(body, signature)
        except InvalidSignatureError:
            start_response('400 Bad Request', [])
            return self.create_body('Bad Request')

        # if event is MessageEvent and message is TextMessage, then echo text
        for event in events:
            if not isinstance(event, MessageEvent):
                continue
            if not isinstance(event.message, TextMessage):
                continue

            command = event.message.text.split(' ')
            if command[0] == '天氣':
                if len(command) < 3:
                    command.append(command[-1])
                display = weather.getWeather(command[1:])
            elif command[0] == '捷運':
                if len(command) < 3:
                    display = '請輸入兩個車站。'    
                else:
                    display = metro.getDuration(command[1:])
            else:
                display = '我聽不懂你在說什麼，你可以試試：天氣 台北 大安'
            
            self.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=display)
            )

        start_response('200 OK', [])
        return self.create_body('OK')

    def create_body(self, text):
        if PY3:
            return [bytes(text, 'utf-8')]
        else:
            return text


lineInstance = lineServer()
callback = lineInstance.callback