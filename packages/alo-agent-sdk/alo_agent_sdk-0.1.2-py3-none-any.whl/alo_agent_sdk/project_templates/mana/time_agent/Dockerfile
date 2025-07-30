# ALO Agent SDK - Agent Dockerfile
# Based on alo_agent_sdk/templates/docker/Dockerfile.agent.template

# Specify the Python version you want to use
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Argument for the agent's specific requirements file
ARG AGENT_REQUIREMENTS_FILE=requirements.txt

# Copy and install SDK requirements first
# This file (requirements.sdk.txt) should be present in the build context (mana/time_agent/)
# and should include alo-agent-sdk==0.1.2.
COPY requirements.sdk.txt .
RUN pip install --no-cache-dir -r requirements.sdk.txt

# Copy the agent's specific requirements file, if it exists, and install them
# The build context should be the root of the agent's project (mana/time_agent/).
COPY ${AGENT_REQUIREMENTS_FILE}* .
RUN if [ -f "${AGENT_REQUIREMENTS_FILE}" ]; then pip install --no-cache-dir -r ${AGENT_REQUIREMENTS_FILE}; fi

# Copy the rest of the agent's application code (e.g., main.py)
COPY . .

# Google Cloud Run expects the application to listen on the port specified by $PORT
# Default port for the agent. Cloud Run will set the $PORT environment variable,
# which Uvicorn will use.
ENV PORT 8080
EXPOSE 8080

# Command to run the Uvicorn server for your FastAPI application
# Assumes your agent's main file is main.py and the FastAPI instance is 'app'.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "$PORT"]
