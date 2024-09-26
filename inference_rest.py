import ssl
import json
import certifi
import urllib.error
import urllib.request
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

ml_client = MLClient.from_config(
    credential=DefaultAzureCredential(),
    path="config.json",
)


endpoint_name = "furlanp-test-endpoint"
deployment_name = "furlanp-test-deployment"

endpoint = ml_client.online_endpoints.get(name=endpoint_name)
scoring_uri = endpoint.scoring_uri
key = ml_client.online_endpoints.get_keys(name=endpoint_name).primary_key

print(scoring_uri, key)

with open("sample_data.json", "r") as file:
    json_str = json.dumps(json.load(file))
    bytes_obj = bytes(json_str, encoding="utf-8")


headers = {
    'Content-Type':'application/json', 
    'Authorization':('Bearer ' + key),
    "azureml-model-deployment": deployment_name
}

context = ssl.create_default_context(cafile=certifi.where())
req = urllib.request.Request(scoring_uri, bytes_obj, headers)

try:
    resp = urllib.request.urlopen(req, context=context)
    result = resp.read()
    print(result)
except urllib.error.HTTPError as error:
    print(str(error))