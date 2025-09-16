## Airflow setup with Docker-compose (provided by airflow)

##### Create your virtual environment and then activate it (then,install requirements if needed)-

<!-- To activate your virtual environment named 'airflow' -->

`source .airflow/bin/activate`

### 1. Run this on your terminal inside project at base root :

#### This docker-compose.yaml uses the official apache/airflow images and sets up scheduler, webserver (API), workers, triggerer, DB (Postgres), Redis, and an airflow-init service used for initialization

`curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'`

### 2. Create host folders & .env :

Run on terminal -
a. `  mkdir -p ./dags ./logs ./plugins ./config`

b. `  echo -e "AIRFLOW_UID=50000" > .env`

### 3. Initialize database & create the first user : (But make sure you have Docker Desktop and its running on your system)

```
docker compose up airflow-init
```

This will cause - The default account created by the quickstart is airflow / airflow.
But If you want the airflow.cfg locally before first run:

```
docker compose run --rm airflow-cli airflow config list
```

// That will create a `config/airflow.cfg` seeded with defaults.

### 4. Start the entire stack : (After airflow-init succeeds, start everything)

```
docker compose up -d
```

#### or for logs in foreground:

`docker compose up`

#### Check containers running :

`docker ps`

### 5. The web UI is available at http://localhost:8080 :

you can log in with airflow / airflow

## Anytime you want to run the docker container (if not running):

`docker compose up -d`

Now, you can see the Airflow UI at localhost:8080

## Stop your running containers and docker compose :

`docker compose down`

## Stop + remove containers and volumes (DB/logs reset):

`docker compose down --volumes`

## Stop + remove containers, volumes, and images (fresh start next time):

`docker compose down --volumes --rmi all --remove-orphans`

## To stop a specific container from the running containers list :

#### 1. check running containers -

`docker ps`

#### 2. stop a running container by its id or name -

`docker stop <container_id_or_name>`

## Know more about AI/LLM/ML projects handling and setup end-to-end : [AI/ML end-to-end project Readme](./src/SRC_Readme.md).
