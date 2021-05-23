- Create two droplets/server one for database one for api server


# setting up database and redis docker

- Creating a docker image for the database
    `docker run --name=bookstore-db -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=ADMIN -e POSTGRES_DB=bookstore -p 5432:5432 -d postgres:10`


- Database visualization tool
    - DataGrip (Paid)
    - pgAdmin: server ip + login details
 
- Database ERP and Schema Creation
    - https://dbdiagram.io/d

- Redis on Serve
    - `docker run --name my-redis -d -p 6379:6379 redis`
    - It can be persisted too


## Unit Testing

- Create a test database
`docker run --name=test-db -e POSTGRES_USER=test -e POSTGRES_PASSWORD=test -e POSTGRES_DB=test -p 5433:5432 -d postgres:10`

-- you need to copy the same scripts for creation of tables into these as well

- Create a test redis
    - `docker run --name test-redis -d -p 6378:6379 redis`

## Load Testing
    # Important Parameter is the RPS: Request Per Seconds
- load testing
    - locust -f tests/locust_load_test.py

- apache bench test
    comes by default or you install apache-utils 
    - ab -n 100 -c 5 -H "Authorization: Bearer <TOKEN>" -p tests/ab_json/post_user.json http://localhost:3000/v1/user

    - ab -n 100 -c 5 -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJTb2xvbW9uIiwiZXhwaXJhdGlvbiI6MTYyMjIzODY5NC4wNDk1OTEsInJvbGUiOiJBRE1JTiJ9.zz_RU2PJWWrxQcHz6YF1TfVoZrxTqUXWiv1f0hxfX88" -p tests/ab_json/post_user.json http://143.244.222.147/v1/user
    
     - ab -n 100 -c 5 -H -p tests/ab_json/token.json http://localhost:3000/v1/token

     - ab -n 100 -c 5 -H -g http://localhost:3000/v1/get/something/2

    
## Deploying

    ### for semi-automate deploy
        # remove the old files

  - ### docker build -t bookstore-api-build .
   

   ### now run it
    - change the Environment variables are correct wtih the ones expected by the base image
    -   https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker
 - ### docker run  -dit --name=bookstore-api -e MODULE_NAME="run" -e PORT='3000' -e PRODUCTION=true -p 3000:3000 bookstore-api-build 

 ### When developing on to digital ocean and your database is separate from the codes, you need to create a private network
 

 Use Floating IP to access the api.
 Use Private IP to access database droplet: Private Network in Networking