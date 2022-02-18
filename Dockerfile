FROM registry.access.redhat.com/ubi8/python-38

# Default user is: uid=1001(default) gid=0(root) groups=0(root)
USER root

# Copy entitlements
COPY ./etc-pki-entitlement /etc/pki/entitlement

# Delete /etc/rhsm-host to use entitlements from the build container
RUN rm /etc/rhsm-host && \
    # Initialize /etc/yum.repos.d/redhat.repo
    # See <https://access.redhat.com/solutions/1443553>
    yum repolist --disablerepo=* && \
    # Enable the repos you need
    subscription-manager repos --enable codeready-builder-for-rhel-8-$(arch)-rpms && \
    dnf -y update && \
    dnf -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm && \
    dnf install -y \
        git \
        binutils \
        gdal \
        gdal-devel \
        geos \
        proj \
        # for Oracle
        libaio && \
    # Remove entitlements and Subscription Manager configs
    rm -rf /etc/pki/entitlement && \
    dnf clean all

# Copy local code to the container image.
COPY api_project api_project/
COPY common_auth common_auth/
COPY geoserver_api geoserver_api/
COPY kaavapino_api kaavapino_api/
COPY facta_api facta_api/
COPY manage.py .
COPY api_project/gunicorn_config.py .
COPY setup.py .

RUN gdal-config --version
# Install dependencies.
RUN pip install --upgrade pip ; pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -e .

# Download and unpack Oracle libraries
RUN cd /tmp ; \
    wget https://download.oracle.com/otn_software/linux/instantclient/211000/instantclient-basiclite-linux.x64-21.1.0.0.0.zip ; \
    mkdir /oracle ; \
    cd /oracle ; \
    unzip /tmp/instantclient-basiclite-linux.x64-21.1.0.0.0.zip ; \
    rm /tmp/instantclient-basiclite-linux.x64-21.1.0.0.0.zip

# WFS fix into Python owslib:
COPY Deployment/owslib/owslib.patch /tmp/
RUN patch -d /opt/app-root/lib64/python3.8/site-packages/ -p0 < /tmp/owslib.patch
# Service must listen to $PORT environment variable.
# This default value facilitates local development.
ENV PORT 8000

# Setting this ensures print statements and log messages
# promptly appear in Cloud Logging.
ENV PYTHONUNBUFFERED TRUE

# Oracle dependencies:
ENV LD_LIBRARY_PATH="/oracle/instantclient_21_1:$LD_LIBRARY_PATH"

# Security: Non-root execution of gunicorn
USER default

# Run the web service on container startup. Here we use the gunicorn webserver
ENTRYPOINT ["gunicorn", "--config", "gunicorn_config.py", "api_project.wsgi:application"]
