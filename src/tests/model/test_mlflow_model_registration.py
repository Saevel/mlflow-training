import mlflow

# TODO: Change this if you changed the host and / or port for MLFlow
client = mlflow.tracking.MlflowClient(tracking_uri="http://localhost:5000")


def test_mlflow_model():
    model_data = client.get_registered_model("IrisModel")

    print("\nModel Data: " + repr(model_data));

    assert model_data is not None, "There should be a registered model under that name"
    assert model_data.latest_versions is not None, "The model should have published versions"

    staged_version = None

    for version in model_data.latest_versions:
        if version.current_stage == 'Staging':
            staged_version = version

    assert staged_version is not None, "There should be a version of the model currently in 'Staging' phase"
