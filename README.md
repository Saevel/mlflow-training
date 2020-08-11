# MLFlow Training

## Who is this tutorial for

The tutorial is for Data Scientists and Data Engineers who wish to learn how use MLFlow to boost and strenghten their ML
and DataScience work, as well as integrate it with external programs, such as batch jobs and / or streaming pipelines.

To make correct use of it, you must know:

* Python 3.x

* Jupyter

* Basics of Scikit-Learn (as the examples are done using it, although general familiarity with Python and popular ML
concepts can largely get you through)

* Basics of PySpark (but you can more or less skip doing the PySpark exercise and still get the model exposure part)

## Requirements

To run this training you will require: 

 * Installation of Python 3.6 (3.x should do, but the project was tested against 3.6 so far) as your main python, on the
   PATH variable
   
  * Corresponding installation of PyPi available under "pip" on the command line 
 
  * Installation of SQLite: https://www.servermania.com/kb/articles/install-sqlite/
  
  * An installation of Anaconda compliant with your version of Python for this virtual environment
 
  * Installation of Spark 2.4.4 (2.x.x should do, but the project was tested against 2.4.4) with SPARK_HOME
  variable correctly set to that installation, and the installation using the same Python version as you will
  be using for this tutorial
 
## Setup and run

NOTE: If you are using Windows, please go to the "environment.bat" file and insert your Anaconda installation path there:
https://docs.anaconda.com/anaconda/user-guide/faq/#:~:text=If%20you%20accept%20the%20default,See%20installing%20on%20macOS
so that MLFlow is able to find Anaconda-based environments later on.
    
Run either the "setup.bat" or "setup.sh" script, depending on your operating system.
    
To start MLFlow, use the following command: 
    
    mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root <your_user_folder>/mlflow/artifacts

where you should substitute <your_user_folder> with the path to your actual user folder.
    
This will start MLFlow on host: 127.0.0.1 and port 5000 by default, but you can override with --host and --port options.
However, if you do so, you need to use the different url consistently in other places in this tutorial.

Once you start MLFlow, go to http://localhost:5000 and verify that the MLFlow UI is visible and both "Experiments" and 
"Models" tabs display correctly.

To run Jupyter, type "jupyter notebook" into the console, preferably from the project's main folder.


## MLFlow Tracking - Example

MLFlow Tracking is MLFlow's API to register all the outputs and side product of your experiments done during the entire
data science process, including but not limited to: data investigation, data cleanup, model fitting and selection. It
helps you save the partials outcomes as you are working, such as:

* arbitrary metrics used for data assessment and purification

* data preprocessing pipelines

* artifacts, such as exported files, graphs saved as images

* machine learning models developed

* metrics related to those models

* arbitrary tags making all the previous easy to identify and browse

As the data science process can be complex and non-linear work, it's better to persist every outocome of your various
approaches as be able to assess them as well as go back to some of them which may prove useful later on.

Open the "src/main/tracking/examples/TrackingExample.ipnyb" file in Jupyter and check out its code, descriptions and 
comments, to understand how a MLFlow interaction is started, ended and how we can use the MLFlow API to register metrics,
parameters, input and output data, trained models and tags.

Once you have executed the entire model, check out the MLFlow UI, to verify the "Tracking-Example" experiment is, in 
fact, created. Then verify that this experiment contains a run with a timestamp matching your Jupyter execution. In that
run, find the parameters, metrics, tags, input data, output data and the saved model.


## MLFlow Tracking - Exercise

Open the "src/main/tracking/exercises/TrackingExercise.ipnyb" notebook in Jupyter to perform this exercise. The file contains
another example of loading data, training a model and metrics evaluation. Add Python / MLFlow code to perform the following:

* Get or create an MLFlow experiment called "Tracking-Exercise"

* Add a tag with name "notebook-type" and value "exercise"

* Add input data as artifact, under the path "input_data"

* Add output data as an artifact, under the path "output_data"

* Register the "n_estimators" model parameter as "num_trees"

* Register the trained Scikit-Learn model as an artifact, called "model"

* Register the "accuracy_score" metric as as "accuracy"

One this is done, use PyTest (installed in virtual environment) to execute tests in the 
"src/tests/tracking/test_mlflow_tracking.py" file to check correctness of your implementation


## MLFlow Models

Once you have finished experimentation and found the right model, MLFlow Models gives you the possibility to promote it
to an "official" model to be validated, tested and eventually, productionized into applications such as Python pipelines,
Spark big data / streaming pipelines or pretty much any application that can make a HTTP call. 

Check the of the runs you have registered for the Iris data in the first exercise, specifically its model artifact. If
you click on it in the runs UI, you will see a button saying "register model". Click it and register you model under the
name "IrisModel"

This registers an official model, which you can then check in the "Models" tab in your MLFlow UI. You can see that this
model has multiple versions (bumped up each time you register the model as described above), so you can work on it
iteratively and add new ones when you achieve good enough results. Those versions can then be promoted between stages of
their lifecycle:

* None

* Staging

* Production

* Archived

In commercial MLFlow deployment, this possibility is available to different users based on their permissions, so it
enables implementing a roles + acceptance based model lifecycle management. 

On top of that, those state transitions can expose HTTP hooks, which can be tapped into by various MLFlow pluggins, for 
instance for CI tools, which would then react to lifecycle changes accordingly. For instance, once you, as a Data 
Scientist, put a new model version into "Staging", this can trigger the CI, to run a task where this would be integrated
into the production-ready code for a Spark Job and tested against a larger, carefully prepred dataset to verify 
production readiness of your model and correctness of its integration into said Spark Job. If this succeeds, the CI task
would automatically move it to your PROD environment and transition it's MLFlow to "Production" and your older model 
version to "Archived", which would dump its contents to special storage. Otherwise, the CI job could transition your 
new model to "None" state and send you an email notifying of failure.

Use the MLFlow Models UI to move your model into the "Staging" state.

To check you performed this correctly, use PyTest to run the "src/tests/model/test_mlflow_model_registration.py" test 
cases.


## MLFlow Model Exposure

One of the key facilities of MLFlow is the ability to expose a model via HTTP under a given URL. Such model can then be 
called, passing the input data in a JSON, both single record (which gives a single response) and with vectorized input
(which gives vectorized responses). This ensure the facility is suitable for apply the model both in batch and streaming
applications.

Note that when you look up your model in your run as an artifact, it comes with a set of additional files, like:
* "MLModel" - a YAML descriptor of the environment, from which your project was registered
* "conda.yaml" - a detailed description of the Anaconda environment attached to your Jupyter instance

Of course, MLFlow supports other types of environments, such a virtuals envs, or even dockerized ones. 

MLFlow will create those descriptors to then be able to automatically run your model and expose it via HTTP.

Use the following command to expose your model via HTTP: 

    mlflow serve -p 5050 --model=uri models:/IrisModel/Staging
    
which will expose your model via HTTP on the 5050 port. The "Staging" state, can also be replaced by a version in this 
URI. You can then call your model by sending a POST request to the "http://localhost:5050/invocations" URL, with an
example body like this:

    {"data":[[6.0, 2.2, 5.0, 1.5], [5.7, 2.9, 4.2, 1.3]]}

this will be assembled to an two-dimensional NumPy ndarray and passed through the model, producing a response in a 
corresponding format. If your preprocessing pipeline is bundled with the model, and uses Pandas DataFrame column names,
you can add a "columns" JSONArray, which will then be factored into assembling a DataFrame for your input and work 
correctly with such a pipeline.

Obviously, models exposed like this can then be integrated, through HTTP, into many different envrionments.

Once you have done this, test the correctness of your implementation by running PyTest + the cases from 
"src/tests/exposure/test_http_model.py"


## Model integration with Spark.

    TODO







 