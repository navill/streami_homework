#!/bin/bash



echo '도커를 이용해 game of life를 실행하기 위한 환경을 구축합니다.'

# pull docker
docker pull afmadadns/streami:1

# run docker - 종류 후 컨테이너 삭제 
docker run -it --rm afmadadns/streami:1

