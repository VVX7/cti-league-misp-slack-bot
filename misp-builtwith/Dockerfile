FROM python:3.7-slim-stretch AS builder

# Build the dependencies on the builder container.
COPY requirements.txt /requirements.txt

# Setup the venv.
RUN python3 -m venv /venv

# Use python and pip executables from the venv.
ENV PATH="/venv/bin:$PATH"

# Install git
RUN apt update
RUN apt install git -y

# Install pip requirements.
RUN pip3 install --no-cache-dir -r /requirements.txt

# Build latest PyMISP
RUN pip3 install git+https://github.com/MISP/PyMISP.git

FROM python:3.7-slim-stretch AS base

# Copy the venv from builder.
COPY --from=builder /venv /venv

# Use python and pip executables from the venv.
ENV PATH="/venv/bin:$PATH"

# Copy the app folder to the container.
COPY ./app /app
WORKDIR /app

# Create non-root user and group.
RUN groupadd -r flask -g 7000
RUN useradd -u 7000 -r -g flask -M -d /twitter_misp -s /sbin/nologin flask

# Switch to non-root user.
USER flask

# Start a worker and Flask.
CMD ["bash", "prestart.sh"]
