# TODO: Use MLFlow UDFs to append a column called "predicted_label" to the input DataFrame, where the predictions should
# TODO: come from the "IrisModel" version currently in the "Staging" stage


def predict_label_with_mlflow_udf(spark_session, data_frame):
    return data_frame