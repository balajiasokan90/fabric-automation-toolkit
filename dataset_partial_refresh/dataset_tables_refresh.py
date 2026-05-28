import sempy.fabric as fabric
import json

#Get the fabric client
client = fabric.PowerBIRestClient()

#Define input parameters
input_tables = "Table_1,Table_2,Table_3"
input_ws_name = "Workspace Name"
input_ds_name = "Dataset Name"

#Get the workspace ID and dataset ID based on the input names
workspace_response = client.get(f"v1.0/myorg/groups")
groups = workspace_response.json().get("value", [])

workspace_id = next(
    (g["id"] for g in groups if g["name"].lower() == input_ws_name.lower()), 
    None
    )

dataset_response = client.get(f"v1.0/myorg/groups/{workspace_id}/datasets")
datasets = dataset_response

dataset_id = next(
    (d["id"] for d in datasets if d["name"].lower() == input_ds_name.lower()), 
    None
    )

print(f"Dataset ID: {dataset_id}")

tables = [table.strip() for table in input_tables.split(",")]
objects_list = [{"table": table} for table in tables]

print(objects_list)

datasetId = dataset_id

#Construct the request body for the API call
request_body = {
    "type": "Full",
    "commitMode": "transactional",
    "objects": objects_list
}

#API call to trigger the dataset refresh with the specified tables
response = client.post(f"v1.0/myorg/datasets/{datasetId}/refreshes", json=request_body)
