import os
import ssl
import json
import certifi
import urllib.error
import urllib.request
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

from dotenv import load_dotenv
load_dotenv()


client = MLClient(
    credential=DefaultAzureCredential(),
    subscription_id=os.environ["SUBSCRIPTION_ID"],
    resource_group_name=os.environ["RESOURCE_GROUP_NAME"],
    workspace_name=os.environ["WORKSPACE_NAME"],
)


endpoint_name = os.environ["AZURE_ENDPOINT"]
deployment_name = os.environ["AZURE_DEPLOYMENT"]

endpoint = client.online_endpoints.get(name=endpoint_name, local=True)
scoring_uri = endpoint.scoring_uri
#endpoint_keys = client.online_endpoints.get_keys(endpoint_name)
#key = endpoint_keys.primary_key

#print(scoring_uri, key)


data = [[0.5 for i in range(18)]]
bytes_obj = bytes(json.dumps(data), encoding="utf-8")

headers = {
    'Content-Type':'application/json', 
    #'Authorization':('Bearer ' + key),
    "azureml-model-deployment": deployment_name
}

context = ssl.create_default_context(cafile=certifi.where())
req = urllib.request.Request(scoring_uri, bytes_obj, headers)

try:
    resp = urllib.request.urlopen(req, context=context)
    result = json.loads(resp.read())
    print(result)
except urllib.error.HTTPError as error:
    print(str(error))