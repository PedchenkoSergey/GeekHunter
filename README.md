GeekHunter
==========
----------
Интернет-портал, который позволяет связать между собой сотрудников, ищущих работу и работодателей, которые ищут подходящих сотрудников по средствам размещения и подбора вакансий и резюме.


##Testing
`python manage.py test`

Запуск из директории GeekHunter на сервере:
Добавляем пользователя в группу докера:
`sudo groupadd docker`
Используем утилиту docker-compose без sudo, если пользователь в группе docker: 
`docker-compose down && docker-compose build && docker-compose up -d`

Используем утилиту docker-compose, если пользователь не в группе docker: 
`sudo docker-compose down && sudo docker-compose build && sudo docker-compose up -d`

Том GeekHunter/data - для постоянного хранения информации БД Postgres из докера.
