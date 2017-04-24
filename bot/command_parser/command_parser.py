from weather_parser.weather import WeatherParser
from metro_parser.metro import MetroParser
from db_operator.db_operator import DatabaseConnector
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)

class CommandParser(object):
    """Parse incoming command"""

    def __init__(self):
        self.weather = WeatherParser()
        self.metro = MetroParser()
        pass

    def parse_command(self, events, line_bot):
        """Parse jarvis command"""

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

            data = {'lastCmd': event.message.text}
            db.update(table_name, data, 'userID=\'{}\''.format(user_id))
            command = event.message.text.split()
            if command[0] == '天氣':
                # parse command
                if len(command) == 1:
                    fav = db.query(table_name, ['favorite'],
                                   'userID=\'{}\''.format(user_id))
                    command += fav.split()
                elif len(command) == 2:
                    command.append(command[-1])

                # weather parser progress
                self.weather.approximate_matching(command[1:])
                three_raw_data = self.weather.request_weather(
                    self.weather.three_hour_website.format(
                        CODE=self.weather.county_code))
                seven_raw_data = self.weather.request_weather(
                    self.weather.seven_day_website.format(
                        CODE=self.weather.county_code))
                air_raw = self.weather.request_weather(self.weather.air_website)
                air_res = self.weather.air_quality(air_raw)
                three_parsed_data = self.weather.parse_three_hours_data(three_raw_data)
                seven_parsed_data = self.weather.parse_seven_days_data(seven_raw_data)
                three_collected_data = self.weather.collect_data(three_parsed_data)
                seven_collected_data = self.weather.collect_data(seven_parsed_data)
                if three_collected_data[1]['date'] == seven_collected_data[0]['date']:
                    seven_display = self.weather.typesetting(seven_collected_data[1:])
                else:
                    seven_display = self.weather.typesetting(seven_collected_data[2:])
                three_display = self.weather.typesetting(three_collected_data[:2],
                                                         '    時間    溫度     降雨機率\n')
                return self.weather.query + air_res + three_display + seven_display

            elif command[0] == '捷運':
                if len(command) < 3:
                    display = '請輸入兩個車站。'
                else:
                    url = self.metro.approximate_matching(command[1:])
                    raw_data = self.metro.request_metro(url)
                    parsed_data = self.metro.parsed_data(raw_data)
                    display = self.metro.typesetting(parsed_data)
            elif command[0] == '設定':
                data = {'favorite': ' '.join(command[1:])}
                db.update(table_name, data,
                          'userID=\'{}\''.format(user_id))
                display = '已經您的常用地點設為：{}'.format(' '.join(command[1:]))
            else:
                display = '我聽不懂你在說什麼，你可以試試：天氣 台北 大安'

            # Especially for Lion
            if user_id == 'U90101030d70543c2eb06911da7c7f93b':
                display = '獅子主人，底下是您查詢的結果：\n' + display

            line_bot.reply_message(
                event.reply_token,
                TextSendMessage(text=display))
