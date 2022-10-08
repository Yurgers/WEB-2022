backend часть для трека MORE.Tech 4.0  трек WEB.
https://moretech.vtb.ru/

##Закуск в docker

```buildoutcfg
git clone https://github.com/Yurgers/WEB-2022
cd WEB-2022

docker build . -t backend_web_4

docker run -p 8000:8000 -d backend_web_4
```

## Документация
документация в формате swagger будет доступна по адресу
http://127.0.0.1:8000/docs

