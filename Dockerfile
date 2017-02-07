FROM nginx:1.11.9
MAINTAINER Kai Yu rebellionyu@gmail.com

ENV CHANNEL_ACCESS_TOKEN S/4X9lo2HMDHCXo+S3PHrihkrJaFNPrRfKyNXPoliEPXX4Tt80aaoALWYeHc25f/sDbvE9McXcv7cHeF0PDmAu2gSegfx1L6dyjeZQ596YlRFBLAcfyQC+dGMNlSAud29Rpe6rlrjCR/lEdDo3DnggdB04t89/1O/w1cDnyilFU=

ENV CHANNEL_SECRET 3a2311af95ef08db962704516fc4c3fd

RUN apt-get update && apt-get install -y supervisor python-pip
COPY requirements.txt /opt/linebot/requirements.txt
COPY default.conf /etc/nginx/conf.d/default.conf
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN pip install -r /opt/linebot/requirements.txt

# bot module
COPY app.py /opt/linebot/app.py
COPY weatherParser /opt/linebot/weatherParser
COPY metroParser /opt/linebot/metroParser

# write log into file
RUN unlink /var/log/nginx/access.log
RUN unlink /var/log/nginx/error.log

# html
RUN mkdir /opt/html
COPY index.html /opt/html/index.html

# ssl
COPY ssl/bundle.crt /etc/ssl/bundle.crt
COPY ssl/linebot.kaiyu.site.key /etc/ssl/linebot.kaiyu.site.key

EXPOSE 443

CMD ["/usr/bin/supervisord"]
