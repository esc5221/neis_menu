# 학교 식단 정보 API 서버
* NEIS Open API를 활용해 local db에 학교 정보, 학교별 식단 정보를 crawling 후, 해당 정보를 API로 서빙

## API Docs
[NEIS Menu API Documentation](https://documenter.getpostman.com/view/17269577/VUjSGPQ1#02e30990-a9c8-46ed-b289-823ac4b4c2de)
## Install
### Default
``` shell
git clone https://github.com/esc5221/neis_menu
cd neis_menu
touch .secrets.json
docker-compose up -d
source django_loaddata.sh
```
* `docker-compose up -d` 실행 시, `127.0.0.1:8000`에서 runserver 실행
* `source django_loaddata.sh` : db에 initial data(_dumped_data)를 load
### NEIS API key 설정 (.secrets.json)
``` json
{
    "NEIS_API_KEY": "..."
}
```
* NEIS API 인증 key를 복사해주어야 NEIS API를 사용가능

## Utils
### `django_runserver.sh`
``` shell
docker start neis_menu_django_1
docker logs -f neis_menu_django_1
```
* container에서 runserver 실행 후, log를 터미널에 출력하여 runserver 실행 log 확인
  
### `django_cmd.sh`
``` shell
docker exec -it neis_menu_django_1 /bin/bash
```
* docker container에 접속하여 내부에서 django command 실행 가능

## Django runscript (from django-extensions)
### `crawl_menus`
``` shell
./manage.py runscript crawl_menus --script-args [run_mode] [start_date] [end_date]
```
1. runmode : `test`
    * NEIS API 응답을 test합니다.
2. runmode : `prod`
    * db에 저장되어 있는 모든 학교를 대상으로 `start_date`부터 `end_date`까지의 식단을 크롤링합니다.
      * `start_date`를 지정하지 않으면, 가장 최근 메뉴 날짜부터 시작
      * `end_date`를 지정하지 않으면, 오늘로 지정
