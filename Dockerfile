# use Red Hat recommended base
# https://docs.openshift.com/enterprise/3.0/creating_images/guidelines.html
FROM registry.access.redhat.com/ubi8/python-38 AS compile-image

# Default user is: uid=1001(default) gid=0(root) groups=0(root)
USER root
ENV APP_HOME /kaavoitus-api
WORKDIR $APP_HOME

# Copy local code to the container image.
COPY setup.py .
COPY api_project api_project/
COPY common_auth common_auth/
COPY geoserver_api geoserver_api/
COPY kaavapino_api kaavapino_api/
COPY facta_api facta_api/

# Install dependencies.
RUN pip install --upgrade pip ; pip install wheel
RUN pip install -e .

# Download and unpack Oracle libraries
RUN cd /tmp ; wget https://download.oracle.com/otn_software/linux/instantclient/211000/instantclient-basiclite-linux.x64-21.1.0.0.0.zip ; mkdir /oracle ; cd /oracle ; unzip /tmp/instantclient-basiclite-linux.x64-21.1.0.0.0.zip

# WFS fix into Python owslib:
COPY Deployment/owslib/owslib.patch /tmp/
RUN patch -d /opt/app-root/lib64/python3.8/site-packages/ -p0 < /tmp/owslib.patch



FROM registry.access.redhat.com/ubi8/python-38 AS build-image

# Default user is: uid=1001(default) gid=0(root) groups=0(root)
USER root
ENV APP_HOME /kaavoitus-api
WORKDIR $APP_HOME

# Service must listen to $PORT environment variable.
# This default value facilitates local development.
ENV PORT 8000

# Setting this ensures print statements and log messages
# promptly appear in Cloud Logging.
ENV PYTHONUNBUFFERED TRUE

# Security: Non-root execution of gunicorn
RUN adduser --uid 991 app-user

# Oracle dependencies:
RUN dnf install -y libaio
ENV LD_LIBRARY_PATH=/oracle/instantclient_21_1

# Copy pre-compiled stuff
COPY --from=compile-image /opt/app-root/lib/python3.8/site-packages /opt/app-root/lib/python3.8/site-packages
COPY --from=compile-image /oracle /oracle
COPY --from=compile-image /opt/app-root/bin /opt/app-root/bin
ENV PATH=/opt/app-root/bin:$PATH

# Copy local code to the container image.
COPY api_project api_project/
COPY common_auth common_auth/
COPY geoserver_api geoserver_api/
COPY kaavapino_api kaavapino_api/
COPY facta_api facta_api/
COPY manage.py .
COPY api_project/gunicorn_config.py .
COPY setup.py .

# Security: Non-root execution of gunicorn
USER app-user

# Run the web service on container startup. Here we use the gunicorn webserver
ENTRYPOINT ["gunicorn", "--config", "gunicorn_config.py", "api_project.wsgi:application"]
