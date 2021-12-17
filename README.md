Coin info pipeline
=====

This is an ETL pipeline that runs an endpoint to receive requests. It does the following:
- The extract step parses the request to get data
- The transform step adds more data by getting information from the coinGecko api
- The load step writes the output to files in json format

Design
=====

Choices for infrastructure and storage
----
Since this is a pipeline, each of extract, transform, load components could be separate apps
while storing state in an external store like a DB. For simplicity, we will combine these 3
into one app. To store state that is needed across the steps, we will use a simple key-value
store like redis.
Normally pipelines have multiple extract, transform, load steps where the load step of the first
ETL could be chained to the extract step of the next ETL. In those cases, it would be best to
store the results in a database for easy querying. Since this ETL process has only one load step,
we choose to just write to files.

Storing intermediate state
---
We will use redis to store things we need to track:
- Request number  : A `request_num` key with an integer value that will be incremented everytime we get a request
- Duplicate coins : A key with the `id` every coin will be stored once the coin is processed. The value of the key will be the request number it was first seen in.


Installation
====

1. cd to the pipelineapp directory

2. Create a virtual environment to install  dependencies to and activate it:
```
$ python3 -m venv myvenv
$ source ./myvenv/bin/activate
```

3. Install dependencies:
```
$ pip install -r requirements.txt
```

4. Spin up redis
```
$ docker run -d --name some-redis -p 6379:6379 redis
```

5. Start the API

```
$ FLASK_APP=pipeline FLASK_DEBUG=1 flask run
```

6. You can do a quick healthcheck by running:
```
$ curl http://localhost:5000/
```
and it should return a json like so:
```
{
  "status": "OK"
}
```

Using the pipeline
========

1. You will need 2 terminals: One that has the flask server started and the other to use for calling the api endpoint.

2. The api endpoint to hit for the pipeline is `http://localhost:5000/runtasks`. This only allows POST requests.
You can start feeding the data to the pipeline like so (maybe feed only a small amount of requests to verify it works):
```
cargo run -- -e http://localhost:5000/runtasks -r 10
```

3. Observe the output in the other terminal which prints some information about what records were processed, whether
the id was already processed before, and if there were some coin ids that were incorrect.

4. You should also see an increasing number of files generated in the same directory with name `output_file_<timestamp>` which will have the results (coin exchange details) for each request.

