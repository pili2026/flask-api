# Flask-api
## Environmental requirements
* Ubuntu 18.04
* VScode
* Python 3.9
* Flask 2.0.0
* Docker
* Sqlite(in memory)
## Test tool
* Curl
* Postman

## API
### Get all task
GET `/tasks`
### Get task by id
GET `/task/{id}`
### Create task
POST `/task`

Body: `{"name": "task"}`
### Update task
PUT `/task/{id}`

Body: `{"name": "task", "status": 1}`
### Delete task
DELETE `/task/{id}`


## Docker
### Build image
`docker build -t {image_name} .`

### Run container
`docker run -it -p 5000:5000 --name {container_name} {image_name}`

## Server
### Curl
#### GET
Get all task `curl http://localhost:5000/tasks`

Get task by id `curl http://localhost:5000/task/{id}`
#### POST
`curl -d '{"name": "dinner"}' -H "Content-Type: application/json" -X POST http://localhost:5000/task`
#### PUT
`curl -X PUT -H "Content-Type: application/json" -d '{"status" : true }' http://localhost:5000/task/1"`
#### DELETE
`curl -X DELETE "http://localhost:5000/task/1"`
