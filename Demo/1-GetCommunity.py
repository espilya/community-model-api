import requests
import json

def main():
    # Perform a get request
    response = requests.get("http://localhost:8080/v1.1/communities")
    print(response)
    print(response.text)
    print(response.status_code)

    if response.status_code == 202:
        # Check Job
        jobId = json.loads(response.text)["path"]
        print(jobId)
        response = requests.get("http://localhost:8080/v1.1" + jobId)
        print(response)
        print(response.text)


main()
