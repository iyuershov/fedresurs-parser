# HTTP-сервис для получения списка сообщений с fedresurs.ru

### 1. Запуск
```bash
git clone https://github.com/iyuershov/fedresurs-parser.git && docker-compose up
```

### 2. Работа с сервисом
* Создание задачи:
  ```HTTP
  POST /tasks HTTP/1.1
  Content-Type: application/json
  Host: localhost:5000

  {
	  "keyword": "[Название организации, ИНН или ОГРН]"
  }
  ```
  Возвращаемое значение:
  ```
  {
    "task": "[guid задания]"
  }
* Получение списка заданий:
  ```HTTP
  GET /tasks HTTP/1.1
  Host: localhost:5000
  ```
  Возваращаемое значение:
  ```
  {
  "finished": [
    {
      "guid": "d0148fd5-c6fa-4f4d-8254-d9fc166e7973"
    }
  ],
  "tasks": []
}
