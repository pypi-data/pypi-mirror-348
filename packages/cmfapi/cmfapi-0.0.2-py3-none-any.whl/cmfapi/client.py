
from .conn import cmfConnection

class cmfClient:
    def __init__(self,base_url):
        """
        Initialize the CMF API client wrapper

        :param base_url: CMF Server base URL
        """
        self.connection = cmfConnection(base_url)

        #Space for additional API modules if necessary
        #self.artifacts = cmfArtifacts(self.connection)

    def get_pipelines(self):
        """
        Retrieve currently registered pipelines.

        :return: API response containing registered pipelines.
        """
        return self.connection.get("/pipelines")

    def get_executions_list(self, pipeline_name):
        """
        Retrieve executions for a pipeline.

        :return: API response containing executions for a pipeline.
        """
        return self.connection.get(f"/list-of-executions/{pipeline_name}")

    def get_executions(self, pipeline_name):
        """
        Retrieve executions for a pipeline.

        :return: API response containing executions for a pipeline.
        """
        return self.connection.get(f"/executions/{pipeline_name}")

    def get_artifact_types(self):
        """
        Retrieve a list of artifact types.

        :return: API response containing artifact types.
        """
        return self.connection.get("/artifact_types")

    def get_artifacts(self, pipeline_name, artifact_type):
        """
        Retrieve artifacts of a specific type for a given pipeline.

        :param pipeline_name: Name of the pipeline.
        :param artifact_type: Type of the artifact.
        :return: API response containing artifacts of the specified type.
        """
        return self.connection.get(f"/artifacts/{pipeline_name}/{artifact_type}")

    def get_artifact_lineage_tangled_tree(self, pipeline_name):
        """
        Retrieve the artifact lineage for a given pipeline.

        :param pipeline_name: Name of the pipeline.
        :return: API response containing the artifact lineage tangled tree.
        """
        return self.connection.get(f"/artifact-lineage/tangled-tree/{pipeline_name}")

    def get_execution_lineage_tangled_tree(self, uuid, pipeline_name):
        """
        Retrieve the execution lineage tangled tree for a given UUID and pipeline.

        :param uuid: Unique identifier for the execution.
        :param pipeline_name: Name of the pipeline.
        :return: API response containing the execution lineage tangled tree.
        """
        return self.connection.get(f"/execution-lineage/tangled-tree/{uuid}/{pipeline_name}")

    def get_model_card(self, model_id):
        """
        Retrieve the model card information.
        :param model_id: Unique identifier for the model (as int).
        :return: API response containing the model card details.
        """
        model_id_int = int(model_id)
        return self.connection.get("/model-card", params={"modelId": model_id_int})

    def get_python_env(self):
        """
        Retrieve the Python environment details.

        :return: API response containing the Python environment details as plain text.
        """
        return self.connection.get("/python-env")
        #headers={"Accept": "text/plain"}
    

    def mlmd_push(self, payload):
        """
        Push metadata to the MLMD server.

        :param payload: The data to be pushed to the MLMD server (as a dictionary).
        :return: API response after pushing the metadata.
        """
        return self.connection.post("/mlmd_push", json=payload)

    def mlmd_pull(self, pipeline_name):
        """
        Retrieve metadata for a specific pipeline.

        :param pipeline_name: The name of the pipeline to retrieve metadata for.
        :return: API response containing the metadata for the pipeline.
        """
        return self.connection.get(f"/mlmd_pull/{pipeline_name}")

    def close_session(self):
        """
        Close the session with the CMF server
        """
        self.connection.exit()