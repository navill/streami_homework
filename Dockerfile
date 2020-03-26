FROM ubuntu:16.04

RUN apt-get -y update
# RUN python3-pip python3-venv
RUN apt-get -y install python3-dev
RUN useradd -b /home -m -s /bin/bash streami
RUN usermod -a -G www-data streami
RUN mkdir -p /var/www/streami/game_of_life/dump

ADD ./game_of_life/game_of_life.py /var/www/streami/game_of_life/game_of_life.py
ADD ./game_of_life/plus.txt /var/www/streami/game_of_life/plus.txt
ADD ./test.py /var/www/docker/streami/test.py

## 필요할 겨우 패키지 리스트 도 추가하고 설치
# ADD ./docker/requirements.txt /var/www/docker/streami/requirements.txt
# RUN python3 -m venv /var/www/docker/streami/venv
# RUN source /var/www/docker/streami/venv/bin/activate
# RUN pip3 install -r /var/www/django/requirements.txt

# RUN apt-get -y install supervisor
