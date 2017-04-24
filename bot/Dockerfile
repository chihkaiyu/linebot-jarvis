FROM nginx:1.11.9
MAINTAINER Kai Yu rebellionyu@gmail.com

# copy config files
COPY conf/requirements.txt /opt/linebot/requirements.txt
COPY conf/default.conf /etc/nginx/conf.d/default.conf
COPY conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY conf/my.cnf /etc/mysql/my.cnf

# install python3 and required tool
RUN apt-get update && apt-get install -y python3 supervisor python3-pip
RUN pip3 install -r /opt/linebot/requirements.txt

# bot module
COPY app.py /opt/linebot/app.py
COPY weather_parser /opt/linebot/weather_parser
COPY metro_parser /opt/linebot/metro_parser
COPY db_operator /opt/linebot/db_operator
COPY command_parser /opt/linebot/command_parser

# write log into file
#RUN unlink /var/log/nginx/access.log
#RUN unlink /var/log/nginx/error.log

# html
COPY index.html /opt/index.html

# credential
COPY credential /opt/linebot/credential

# ssl
COPY ssl/bundle.crt /etc/ssl/bundle.crt
COPY ssl/linebot.kaiyu.site.key /etc/ssl/linebot.kaiyu.site.key

EXPOSE 443

CMD ["/usr/bin/supervisord"]
