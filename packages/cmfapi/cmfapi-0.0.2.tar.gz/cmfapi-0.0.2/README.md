# cmfapi 
This package provides a simple, modular SDK for the Common Metadata Framework (CMF) REST API.


## Installation

**Install using `pip`:**

```bash
pip install cmfapi
```

**Install from source:**

```bash
git clone https://github.com/atripathy86/cmfapi.git
cd cmfapi
pip install -e .
```

**Build/Upload for pypi:**

```bash
pip install build
# Build the package
python -m build 
#Creates dist/ with tar.gz and .whl 
```
- Verify ~/.pypirc has PyPi token
```bash 
pip install twine
twine upload dist/*
```

## Quick Start

### Initialize the Client

```python
from cmfapi import cmfClient
client = cmfClient("http://192.168.2.143:8080")
```

### Example Usage
See test.py 

#### Get CMF API Server Pipelines

```python
pipelines = client.get_pipelines()
print(pipelines)  
```

#### Get list of executions for a pipeline
```
if pipelines:  # Check if the list is not empty
    first_pipeline = pipelines[0]

executions_list = client.get_executions_list(first_pipeline)
print(f"Executions List for {first_pipeline}:")
print(json.dumps(executions_list, indent=4))
```

#### Get Execution details for a pipeline
```
executions = client.get_executions(first_pipeline)
print(f"Executions for {first_pipeline}:")
print(json.dumps(executions, indent=4))
```

#### Get Artifact Types in DB
```
artifact_types = client.get_artifact_types()
print("Artifact Types in DB:")
print(json.dumps(artifact_types, indent=4))
```

#### Display Artifacts for a pipeline
```
if artifact_types: 
    first_artifact_type = artifact_types[0]
    print(f"First Artifact Type: {first_artifact_type}")

artifacts = client.get_artifacts(first_pipeline, first_artifact_type)
print(f"Artifacts for {first_pipeline} of type {first_artifact_type}:")
print(json.dumps(artifacts, indent=4))
```

#### Fetch artifact lineage for a pipeline
```
artifact_lineage_tree = client.get_artifact_lineage_tangled_tree(first_pipeline)
print(f"Artifact Lineage Tree for {first_pipeline}:")
print(json.dumps(artifact_lineage_tree, indent=4))
```
#### Fetch execution lineage for a pipeline
```
#Select a particular UUID
if "items" in executions and len(executions["items"]) > 0:
    first_execution = executions["items"][0]  # Get the first execution item
    execution_uuid = first_execution["Execution_uuid"]  # Access the Execution_uuid field
    selected_uuid = execution_uuid[:4]  # Slice the first 4 characters
    print(f"Selected Execution UUID (First 4 characters): {selected_uuid}")
else:
    print("No executions found.")
 
uuid = selected_uuid # Example UUID
pipeline_name = first_pipeline  # Use the first pipeline from the pipelines list

execution_lineage_tree = client.get_execution_lineage_tangled_tree(uuid, pipeline_name)
print(f"Execution Lineage Tree for UUID {uuid} and Pipeline {pipeline_name}:")
print(json.dumps(execution_lineage_tree, indent=4))
```