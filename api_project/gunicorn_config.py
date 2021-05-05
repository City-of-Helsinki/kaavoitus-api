import os

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.

# See: Dockerfile PORT=
# and https://cloud.google.com/run/docs/configuring/environment-variables
# and https://cloud.google.com/run/docs/reference/container-contract#env-vars
if "PORT" in os.environ:
    port = int(os.environ["PORT"])
else:
    port = 8000

bind = "0.0.0.0:%d" % port
workers = 1
threads = 8
timeout = 0
