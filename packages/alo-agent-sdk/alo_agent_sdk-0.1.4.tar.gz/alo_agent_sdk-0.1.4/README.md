# alo-agent-sdk

SDK for building and deploying AI agents.

## Overview

This SDK provides tools and utilities to:
- Standardize the creation of AI agents as FastAPI services.
- Define agent capabilities using the Model Context Protocol (MCP) via `python_a2a`.
- Containerize agents using Docker.
- Deploy agents and an Agent Registry Service to Google Cloud Run.

## Features

- **AgentBuilder**: Simplifies the creation of `python_a2a` compatible agents.
- **RegistryClient**: For agent interaction with the Agent Registry Service.
- **AgentRegistryService**: A FastAPI-based implementation of an agent registry.
- **Deployment Scripts**: Utilities for deploying to Google Cloud Run.
- **Templates**: Dockerfile templates for agents and the registry service.

## Getting Started

This guide will walk you through installing the ALO Agent SDK, creating a simple agent, and deploying it.

### Prerequisites

*   Python 3.8+
*   Docker installed locally (for building container images)
*   Google Cloud SDK (`gcloud` CLI) installed and configured (for Cloud Run deployment)
    *   Ensure you have authenticated with `gcloud auth login` and `gcloud auth application-default login`.
    *   Set your default project with `gcloud config set project YOUR_PROJECT_ID`.
    *   Enable the Cloud Run API, Artifact Registry API, and Cloud Build API in your GCP project.

### 1. Installation

Currently, the SDK is under development. To use it, you would typically clone the repository and install it in editable mode:

```bash
git clone https://github.com/yourusername/alo_agent_sdk.git # Replace with actual repo URL
cd alo_agent_sdk
pip install -e .
```
*(Once published, it would be `pip install alo-agent-sdk`)*

### 2. Create your First Agent

Let's create a simple "Echo Agent" that echoes back any message it receives.

1.  **Create a project directory for your agent:**
    ```bash
    mkdir my_echo_agent
    cd my_echo_agent
    ```

2.  **Create your main agent file (e.g., `main.py`):**
    ```python
    # my_echo_agent/main.py
    from alo_agent_sdk.core import AgentBuilder
    import os

    # Configure the agent
    # For Cloud Run, ALO_AGENT_BASE_URL will be derived from the service URL.
    # ALO_REGISTRY_URL should be set as an environment variable in Cloud Run.
    agent = AgentBuilder(
        name="EchoAgent",
        version="0.1.0",
        description="A simple agent that echoes messages.",
        registry_url=os.getenv("ALO_REGISTRY_URL", "http://localhost:8001") # Default for local
    )

    @agent.tool(description="Echoes back the input message.")
    async def echo(message: str) -> str:
        """
        Receives a message and returns it prefixed with 'Echo: '.
        """
        print(f"Echoing message: {message}")
        return f"Echo: {message}"

    # Get the FastAPI app instance from the builder
    app = agent.get_fastapi_app()

    # For local execution (optional, Uvicorn is usually run by Docker CMD)
    if __name__ == "__main__":
        import uvicorn
        port = int(os.getenv("PORT", 8080))
        print(f"Starting EchoAgent locally on http://localhost:{port}")
        # Note: For local testing with registration, ensure the registry service is running.
        # The agent_base_url for local registration might need to be explicitly set
        # if not using the default http://localhost:PORT.
        # e.g., agent = AgentBuilder(..., agent_base_url="http://your-local-ip:8080")
        uvicorn.run(app, host="0.0.0.0", port=port)
    ```

3.  **Create a `requirements.txt` for any specific dependencies (optional):**
    For this simple agent, it might be empty if it only relies on the SDK.
    ```
    # my_echo_agent/requirements.txt
    # Add any specific dependencies for your agent here
    ```

4.  **Prepare your `Dockerfile`:**
    *   Copy `alo_agent_sdk/templates/docker/requirements.sdk.txt` to your agent's project directory (`my_echo_agent/requirements.sdk.txt`).
    *   Copy `alo_agent_sdk/templates/docker/Dockerfile.agent.template` to `my_echo_agent/Dockerfile`.
    *   Ensure the `CMD` in your `Dockerfile` correctly points to your FastAPI app instance (e.g., `main:app` if your file is `main.py` and instance is `app`).

### 3. Deploy the Agent Registry Service (One-time setup or if not already running)

The agents need a registry service to register with and for discovery.

1.  **Navigate to the SDK's example for registry deployment:**
    (Assuming you have the `alo_agent_sdk` cloned)
    ```bash
    cd path/to/alo_agent_sdk/examples/example_registry_deploy
    ```
    *   This directory contains a `Dockerfile` based on `Dockerfile.registry.template`.
    *   It also needs `requirements.sdk.txt` (copy it from `alo_agent_sdk/templates/docker/`).
    *   It also needs the `alo_agent_sdk` source code to be in the Docker build context (as per `COPY alo_agent_sdk ./alo_agent_sdk` in its Dockerfile). A simple way is to run the deploy script from the root of the `alo_agent_sdk` checkout, adjusting paths.

2.  **Deploy using the `deploy_cloud_run.sh` script:**
    (Assuming you are in the root of the `alo_agent_sdk` cloned repository)
    ```bash
    ./scripts/gcp/cloud_run/deploy_cloud_run.sh \
      -s alo-registry-service \
      -p YOUR_GCP_PROJECT_ID \
      -c examples/example_registry_deploy # Source path for build context
      # The Dockerfile used will be examples/example_registry_deploy/Dockerfile
    ```
    Take note of the URL of the deployed registry service. You'll need to set this as `ALO_REGISTRY_URL` for your agents.

### 4. Deploy your Echo Agent to Cloud Run

1.  **Navigate to your agent's project directory:**
    ```bash
    cd path/to/my_echo_agent
    ```

2.  **Run the deployment script:**
    (Assuming `deploy_cloud_run.sh` is in your PATH or you provide the full path to it)
    ```bash
    # Path to deploy_cloud_run.sh from alo_agent_sdk
    DEPLOY_SCRIPT_PATH="../path/to/alo_agent_sdk/scripts/gcp/cloud_run/deploy_cloud_run.sh" 
    
    # Ensure your GCP Project ID is set
    GCP_PROJECT_ID="YOUR_GCP_PROJECT_ID"
    # URL of your deployed Agent Registry Service
    REGISTRY_SERVICE_URL="YOUR_REGISTRY_SERVICE_URL" 

    bash $DEPLOY_SCRIPT_PATH \
      -s echo-agent \
      -p $GCP_PROJECT_ID \
      -e "ALO_REGISTRY_URL=$REGISTRY_SERVICE_URL" 
      # -c . (source path defaults to current directory)
      # The script expects 'Dockerfile' in the current directory.
    ```
    This will build your agent's Docker image, push it to Google Artifact Registry, and deploy it to Cloud Run. The `ALO_REGISTRY_URL` environment variable tells your agent where to find the registry. The agent will also try to determine its own public URL (e.g., from `ALO_AGENT_SERVICE_URL` which can be set based on Cloud Run's `K_SERVICE` URL or similar).

### 5. Test your Agent

Once deployed, you can find your agent's URL in the Cloud Run console or from the output of the deploy script.

*   **Agent Card:** Access `https://your-echo-agent-url.a.run.app/agent.json`
*   **MCP Tool:** You can call the `echo` tool via a POST request to `https://your-echo-agent-url.a.run.app/tools/echo` with a JSON body like:
    ```json
    {
      "message": "Hello from ALO SDK!"
    }
    ```

### Next Steps

*   Explore the `alo_agent_sdk.core.AgentBuilder` to add more complex tools and resources.
*   Check the `examples/` directory in the SDK for more usage patterns.
*   Implement more sophisticated agents!

## Project Structure

```
alo_agent_sdk/
├── core/
│   ├── agent_builder.py
│   └── registry_client.py
├── registry_service/
│   ├── main.py
│   └── models.py
├── templates/
│   └── docker/
│       ├── Dockerfile.agent.template
│       ├── Dockerfile.registry.template
│       └── requirements.sdk.txt
├── scripts/
│   └── gcp/
│       └── cloud_run/
│           └── deploy_cloud_run.sh
├── examples/
│   ├── example_agent/
│   └── example_registry_deploy/
├── docs/
├── pyproject.toml
└── README.md
```

## Contributing

*(Contribution guidelines to be added)*

## License

*(License information to be added, e.g., MIT License)*
