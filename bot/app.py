#!/usr/bin/env python3
# -*- coding: utf8 -*-

import sys
import os
from configparser import ConfigParser
from command_parser.command_parser import CommandParser
from db_operator.db_operator import DatabaseConnector


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


class LineServer(object):
    """Line bot server"""

    def __init__(self):
        line_config = ConfigParser()
        # root_dir = os.environ.get('ROOT_DIR')
        folder_name = os.path.dirname(os.path.abspath(__file__))
        line_config_path = os.path.join(folder_name, 'credential',
                                        'line_config.ini')
        line_config.read(line_config_path)
        if not line_config.has_option('Line Config', 'ACCESS_TOKEN'):
            print('Specify LINE_CHANNEL_SECRET as environment variable.')
            sys.exit(1)
        if not line_config.has_option('Line Config', 'SECRET'):
            print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
            sys.exit(1)
        channel_secret = line_config['Line Config']['SECRET']
        channel_access_token = line_config['Line Config']['ACCESS_TOKEN']
        self.line_bot_api = LineBotApi(channel_access_token)
        self.parser = WebhookParser(channel_secret)

        # parser instance
        self.command = CommandParser()

    def __del__(self):
        print('Destroyed')

    def callback(self, environ, start_response):
        """Process every line message"""

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

        db = DatabaseConnector()
        table_name = 'USER'
        user_id = events[0].source.user_id

        # create user if not in database
        if not db.is_record(table_name, 'userID', user_id):
            data = {'userID': user_id}
            db.insert(table_name, data)

        for event in events:
            if not isinstance(event, MessageEvent):
                display = 'WOW, that\'s new!'
                continue
            if not isinstance(event.message, TextMessage):
                display = 'WOW, that\'s new!'
                continue
            # command = event.message.text
            display = self.command.parse_command(event, db)

            self.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=display))
        del db
        start_response('200 OK', [])
        return self.create_body('OK')

    def create_body(self, text):
        if PY3:
            return [bytes(text, 'utf-8')]
        else:
            return text

line_instance = LineServer()
callback = line_instance.callback
