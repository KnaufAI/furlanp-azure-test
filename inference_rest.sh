# USING CLI:
GROUP="rg-ki-ds-s"
WORKSPACE="mlw-ki-ds-s"
ENDPOINT="furlanp-test-endpoint"
DEPLOYMENT="furlanp-test-deployment"
KEY=$(az ml online-endpoint get-credentials -n "$ENDPOINT" -g "$GROUP" -w "$WORKSPACE" -o tsv --query primaryKey) 
API=$(az ml online-endpoint show -n "$ENDPOINT" -g "$GROUP" -w "$WORKSPACE" -o tsv --query scoring_uri)
curl --request POST "$API" -L -H "Authorization: Bearer $KEY" -H "Content-Type: application/json"  -H "azureml-model-deployment: $DEPLOYMENT" -d @sample_data.json