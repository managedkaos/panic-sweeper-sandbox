# Use an official Python runtime as a parent image
FROM pull rockylinux:9.3-minimal

ARG build_number
ARG build_timestamp
ARG build_url
ARG git_url
ARG git_branch_name
ARG git_sha1
ARG project_name

ENV JAVA_OPTS="" \
    APP_ENV="docker" \
    BUILD_DATE=${build_timestamp} \
    BUILD_NUMBER=${build_number} \
    GIT_SHA_1=${git_sha1} \
    VARNISH_VERSION="7.5.1d12"

ENV WORKDIR=/work
RUN mkdir /work

RUN yum install -y java-1.8.0-openjdk \
                   epel-release \
                   mtr \
                   python3 \
                   python3-pip \
                   traceroute && \
    yum install -y python3-gobject-base \
                   varnish-${VARNISH_VERSION} && \
    pip3 install pydbus

# Set the working directory in the container
WORKDIR ${WORKDIR}

# Install runtime dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy necessary files
COPY main.py /usr/local/bin

# Run the script when the container launches
ENTRYPOINT ["python", "/usr/local/bin/main.py"]
