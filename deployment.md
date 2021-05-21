- Create two droplets/server one for database one for api server


# database docker

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


## For Testing

- Create a test database
`docker run --name=test-db -e POSTGRES_USER=test -e POSTGRES_PASSWORD=test -e POSTGRES_DB=test -p 5433:5432 -d postgres:10`

-- you need to copy the same scripts for creation of tables into these as well

- Create a test redis
    - `docker run --name test-redis -d -p 6378:6379 redis`

