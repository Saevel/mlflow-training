import mlflow

# NOTE: Change this is you changed the host and / or port for MLFlow
client = mlflow.tracking.MlflowClient(tracking_uri="http://localhost:5000")


def test_experiment_exists():

    experiment = client.get_experiment_by_name("Tracking-Exercise")

    print("Experiment: " + repr(experiment))

    assert experiment is not None, "The experiment Tracking-Example should exist"


def test_multiple_runs():
    experiment = client.get_experiment_by_name("Tracking-Exercise")

    runs = client.list_run_infos(experiment.experiment_id)

    print("Runs: " + repr(runs))

    assert runs is not None, "There should be runs data"
    assert len(runs) > 0, "There should be some runs"
