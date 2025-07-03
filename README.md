# StressAway App
An app to learn about LLM and run it locally

# Testin the LLaMA API

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is gravity?"}'
  ```


# Running the docker container

```
docker run -p 8000:8000 -v $(pwd)/models:/app/models backend
```

# To create the docker image 

```
docker build -t backend
```

# If docker compose is present, the command to build will be
```
docker-compose up --build
```

# To rebuild the docker image
```
docker-compose build --no-cache
```

# To create a virtual environment in mac
```
python3 -m venv ./venv
```

# To activate a virtual environment
```
source venv/bin/activate
```

# To deactivate the environment 
```
deactivate
```
