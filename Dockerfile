# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9

# Target Python environment variable to bind to pip.conf
ENV PIP_CONFIG_FILE /pip.conf

# Copy local code to the container image.
WORKDIR .
COPY . ./

# Install production dependencies.
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Run the web service on container startup using gunicorn webserver.
# working with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec opentelemetry-instrument --traces_exporter gcp_trace --propagator gcp_trace gunicorn --bind 0.0.0.0:$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker --threads 8 --timeout 0 main:app
