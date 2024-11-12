import os
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from azure.ai.ml.entities import (
    ManagedOnlineEndpoint,
    ManagedOnlineDeployment,
    Model,
    CodeConfiguration,
    Environment,
)

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
env_name = os.environ["AZURE_ENVIRONMENT"]
model_name = os.environ["AZURE_MODEL"]


# endpoint configuration
endpoint = ManagedOnlineEndpoint(
    name=endpoint_name,
    auth_mode="key",
)
client.online_endpoints.begin_create_or_update(endpoint, local=True)


# environment configuration
img = "mcr.microsoft.com/azureml/minimal-ubuntu22.04-py39-cpu-inference:latest"

env = Environment(
    name=env_name,
    version="1",
    image=img,
    conda_file="assets/env_spec.yaml",
)
#env = client.environments.create_or_update(env)


# model configuration
model = Model(
    name=model_name,
    version="1",
    type="custom_model",
    path="assets/model.joblib",
)
#model = client.models.create_or_update(model)


# deployment configuration
# first run the compute node that is responsible for image build!
# az ml workspace update --name ws --resource-group rg --image-build-compute mycompute
deployment = ManagedOnlineDeployment(
    name=deployment_name,
    endpoint_name=endpoint_name,
    model=model,
    code_configuration=CodeConfiguration(
        code="assets",
        scoring_script="score.py",
    ),
    #environment=f"azureml:{env.name}:{env.version}",
    environment=env,
    #egress_public_network_access="disabled",
)

deployment = client.online_deployments.begin_create_or_update(
    deployment, local=True
)

endpoint = client.online_endpoints.get(endpoint_name, local=True)
scoring_uri = endpoint.scoring_uri
print(scoring_uri)


#endpoint.traffic = {deployment_name: 100}
#client.create_or_update(endpoint)