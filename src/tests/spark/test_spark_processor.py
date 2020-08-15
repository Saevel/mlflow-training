from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score

import pandas as pd
import mlflow.sklearn
import findspark

from pyspark.sql import SparkSession

from src.main.spark.spark_processor import predict_label_with_mlflow_udf


def test_spark_integration():

    findspark.init()

    session = SparkSession.builder \
        .appName("mlflow_spark_integration_test") \
        .master("local[*]") \
        .config("spark.sql.execution.arrow.pyspark.enabled", "false") \
        .getOrCreate()

    iris = load_iris()

    iris_pd_data_frame = pd.DataFrame(iris.data, columns=iris.feature_names)

    iris_data_frame = session.createDataFrame(iris_pd_data_frame)

    result = predict_label_with_mlflow_udf(session, iris_data_frame)

    assert result is not None, "The result DataFrame should not be none"

    for column in iris.feature_names:
        assert column in result.columns, "The result DataFrame columns should contain: '" + column + "'"

    assert "predicted_label" in result.columns, "The result DataFrame columns should contain: 'predicted_label'"

    # TODO: Change this if using different tracking URI
    mlflow.set_tracking_uri("http://localhost:5000")

    model = mlflow.sklearn.load_model("models:/IrisModel/Staging")

    assert model is not None, "The IrisModel should have a version in the 'Staging' stage in MLFlow"

    expected_predictions = model.predict(iris_pd_data_frame)

    actual_predictions = result.select("predicted_label").collect()

    accuracy = accuracy_score(expected_predictions, actual_predictions)

    assert accuracy >= 0.85, "The identicity between model application from UDF and loaded model should be at " \
                                   "least 85%"



