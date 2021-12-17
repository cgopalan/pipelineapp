from flask import Flask, request
import time
import redis
import extract, transform, load

app = Flask(__name__)

# Use redis to hold state like request number and whether
# a coin was already processed or not.
cache = redis.Redis(host="localhost", port=6379)


@app.route("/")
def healthcheck():
    """Health and sanity check"""
    return {"status": "OK"}


@app.route("/runtasks", methods=["POST"])
def run_tasks():
    """Main endpoint to process requests"""
    start = time.time()
    process_task(request)
    time_taken_ms = (time.time() - start) / 1000
    if time_taken_ms > 400:
        print(f"Warning! Time taken in milliseconds: {time_taken_ms}")
    return "Success", 200


def process_task(request):
    """Pipeline that processes the request"""

    # Keep track of request number
    request_num = cache.incr("request_num", 1)

    # Get coin ids from request
    ids = extract.parse_request(request)
    print(f"ids extracted: {ids}")

    # Process each id
    results = []
    for id in ids:
        id_request_num = cache.get(id)
        if not id_request_num:
            print(f"id {id} not in cache, making api request")
            id_result = transform.get_result_json(id, request_num)
            if id_result:
                results.append(id_result)
            cache.set(id, request_num)
        else:
            print(f"id {id} already exists skipping")

    # Write results to file
    if results:
        load.write_results(results)
