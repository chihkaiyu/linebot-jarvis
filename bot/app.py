#!/usr/bin/env python3
# -*- coding: utf8 -*-

import sys
import os
from weatherParser import weather
from metroParser import metro
from dbOperator import dbOperator

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
    
    def __del__(self):
        print('Destroyed')

    def callback(self, environ, start_response):
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
        
        # database connect
        db = dbOperator.DBConnector()
        tableName = 'USER'
        userID = events[0].source.user_id
        
        # create user if not in database
        if not db.isRecord(tableName, 'userID', userID):
            data = {'userID': userID}
            db.insert(tableName, data)

        # if event is MessageEvent and message is TextMessage, then echo text
        for event in events:
            if not isinstance(event, MessageEvent):
                continue
            if not isinstance(event.message, TextMessage):
                continue

            command = event.message.text.split()
            
            data = {'lastCmd': event.message.text}
            db.update(tableName, data, 'userID=\'{}\''.format(userID))
            
            if command[0] == '天氣':
                if len(command) == 1:
                    fav = db.query(tableName, 'lastCmd', 'userID=\'{}\''.format(userID))
                    command += [fav]
                elif len(command) == 2:
                    command.append(command[-1])
                display = weather.getWeather(command[1:])
            elif command[0] == '捷運':
                if len(command) < 3:
                    display = '請輸入兩個車站。'    
                else:
                    display = metro.getDuration(command[1:])
            elif command[0] == '設定':
                data = {'favorite': ' '.join(command[1:])}
                db.update(tableName, data, 'userID=\'{}\''.format(userID))
                display = '已經您的常用地點設為：{}'.format(' '.join(command[1:]))
            else:
                display = '我聽不懂你在說什麼，你可以試試：天氣 台北 大安'
            
            # Especially for Lion
            if userID == 'U90101030d70543c2eb06911da7c7f93b':
                display = '獅子主人，底下是您查詢的結果：\n' + display
                
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
