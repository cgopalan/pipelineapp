import json
from datetime import datetime


def write_results(results):
    """Write results to file. To keep the file name unique add a timestamp"""
    with open(f'output_file_{datetime.now().strftime("%Y%m%d%H%M%f")}', "w") as f:
        f.write(json.dumps(results))
