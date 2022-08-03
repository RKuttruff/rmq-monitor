
import requests
from requests.auth import HTTPBasicAuth
import time

auth = HTTPBasicAuth('user', 'bitnami')

waiting = True

while True:
    response = requests.get("http://localhost:15672/api/queues/%2f/nexus", auth=auth)

    if response.ok:
        data = response.json()

        print(f"\r{data['messages_unacknowledged']} in progress, {data['messages_ready']} waiting.", end='', flush=True)

        if data['messages_unacknowledged'] == 0 and data['messages_ready'] == 0 and not waiting:
            print()
            break
        elif data['messages_unacknowledged'] > 0 or data['messages_ready'] > 0:
            waiting = False
    else:
        print(f"RMQ request failed: {response.status_code}")

    time.sleep(10)
