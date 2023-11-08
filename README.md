# Rome

Everyone says "All roads lead to Rome" but what that really means is "All roads were constructed starting from Rome".

This Repository pretends to be a boilerplate code to create new microservices from scratch (By using Fast API with Python as a web application framework).

![og-home 663159de094c098881b996bd982834c5](https://www.fodors.com/wp-content/uploads/2018/10/HERO_UltimateRome_Hero_shutterstock789412159.jpg)

## How to install Rome

In order to run Rome you will need to install Python 3.9, after this run the following commands:

```sh
python3 -m venv venv/
source venv/bin/activate
cp pip.conf venv/
pip install -r requirements.txt
```

This will create a virtual environment where all the service dependencies are going to be installed.

## How to run Rome

You can run Rome by issuing the following command (opentelemetry-instrument is not required on development, it is needed on both sandbox and production to track problems across services):

```sh
python3 main.py
```

or

```sh
opentelemetry-instrument --traces_exporter gcp_trace --propagator gcp_trace gunicorn --bind 0.0.0.0:5005 --workers 1 --worker-class uvicorn.workers.UvicornWorker --threads 8 --timeout 0 --reload main:app

```

You will need to create a `.env` file or pass several arguments or environment variables to the `main.py` script like:

- `--env` or `ENV`: Possible application environments are `test`, `development`, `sandbox` and `production`.
- `--config_path` or `CONFIG_PATH`: Relative file path where all the configuration files are stored.
- `--google_application_credentials` or `GOOGLE_APPLICATION_CREDENTIALS`: Relative file path to the GCP .json credentials, you don't need to provide this argument or environment variable in you are deploying the application in GCP.
- `--reload` or `RELOAD`:  If you set this argument or the environment variable with any value reload flag for FastAPI will be set to True, do not pass this if you want the reload flag to be False.

## How to deploy Rome

The deployment of this project is performed on Google Cloud Run (https://cloud.google.com/run) which is a managed computing platform that enables you to run containers that are invocable via requests or events. Cloud Run is serverless: it abstracts away all infrastructure management, so you can focus on what matters most — building great applications.

The deployment is made manually by using Google Cloud Build (https://cloud.google.com/build) on the GCP console. Cloud build is a CI/CD tool that will help us to automatically deploy our application to Cloud Run.

You can find the pipeline instructions that are executed during the deployment in the root folder of this project. In the file called `cloudbuild.yaml`. You can also check the **DOCKERFILE** to see the steps that are performed to build the container (which uses python3.9 and runs a server instance by using Unicorn).

The pipeline build instructions involve the following steps:

- Build the docker image
- Push the Docker image to the container registry (located at Google Container Registry)
- Deploy container image to Cloud Run (Specifying the machine requirements, Environment variables and secrets needed)
- Assign the traffic to the new image created
