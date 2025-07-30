# ALO Agent SDK - Agent Registry Service Dockerfile
# Based on alo_agent_sdk/templates/docker/Dockerfile.registry.template

# Specify the Python version you want to use
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# 1. Copy requirements.sdk.txt (which should list alo-agent-sdk==0.1.2)
#    This file will be copied from the generated project's agent_registry directory.
COPY requirements.sdk.txt .

# 2. Install alo-agent-sdk and its dependencies from PyPI.
#    This also installs other dependencies listed in requirements.sdk.txt.
RUN pip install --no-cache-dir -r requirements.sdk.txt

# Note: The specific COPY lines for 'registry_service' and 'core' are no longer needed
# as the entire SDK (which includes them) will be installed as a dependency.

# Google Cloud Run expects the application to listen on the port specified by $PORT
# Default port for the registry, can be overridden by Cloud Run's $PORT environment variable.
ENV PORT 8081
EXPOSE $PORT

# Command to run the Uvicorn server for the FastAPI Registry Service application
# This should point to the FastAPI 'app' instance in alo_agent_sdk.registry_service.main
# This assumes 'alo_agent_sdk' is installed via requirements.sdk.txt and available in PYTHONPATH.
CMD ["uvicorn", "alo_agent_sdk.registry_service.main:app", "--host", "0.0.0.0", "--port", "$PORT"]
