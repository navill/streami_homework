FROM ubuntu:16.04

# 파이썬 설치
RUN apt-get -y update
# RUN python3-pip && python3-venv
RUN apt-get -y install python3-dev
# 권한 설정
RUN useradd -b /home -m -s /bin/bash streami
RUN usermod -a -G www-data streami

RUN mkdir -p /var/www/streami/game_of_life/dump
# 한글 출력을 위한 패키지
RUN apt-get install locales
RUN apt-get install -y \
    language-pack-ko && \
    dpkg-reconfigure locales && \
    locale-gen ko_KR.UTF-8 && \
    /usr/sbin/update-locale LANG=ko_KR.UTF-8
# 한글을 출력하기 위해 환경변수 등록
ENV LANG=ko_KR.UTF-8
ENV LANGUAGE=ko_KR.UTF-8
ENV LC_ALL=ko_KR.UTF-8
# 파이썬에서 한글을 사용할 수 있도록 환경변수 등록
ENV PYTHONIOENCODING=UTF-8

# 파일 복사
ADD ./game_of_life/game_of_life.py /var/www/streami/game_of_life/game_of_life.py
ADD ./game_of_life/plus.txt /var/www/streami/game_of_life/plus.txt
