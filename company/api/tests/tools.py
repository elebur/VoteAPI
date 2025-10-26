import json

from django.test import Client


def send_json(client: Client, url: str, payload: dict):
    resp = client.post(url,
                       json.dumps(payload),
                       content_type="application/json")
    return json.loads(resp.text)
