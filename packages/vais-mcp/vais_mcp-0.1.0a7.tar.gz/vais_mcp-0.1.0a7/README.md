# MCP Server for Vertex AI Search

MCP server to search private data in Vertex AI Search.

## Tools

- `search`: Search for Vertex AI Search and returns result chunks.
  Returns a dictionary with a "response" key. The value of "response" is a list of dictionaries, each containing the title of the source document and the extracted content chunk. Example:

```json
{
  "response": [
    {
      "title": "Sample Document Title 1",
      "content": "Extracted text segment from the document."
    },
    {
      "title": "Sample Document Title 2",
      "content": "Another extracted text segment."
    }
  ]
}
```

## Prerequisites

1. Install uv from [Astral](https://docs.astral.sh/uv/getting-started/installation/) or the [GitHub README](https://github.com/astral-sh/uv#installation)
2. Install Python 3.13 using `uv python install 3.13`
3. Create a Vertex AI Search app  
   i. [Official Document](https://cloud.google.com/generative-ai-app-builder/docs/create-engine-es)

## Configuration

Add the following to your server configuration:

```json
{
  "vais-mcp": {
    "command": "uvx",
    "args": ["vais-mcp@latest"],
    "env": {
      "GOOGLE_CLOUD_PROJECT_ID": "<google_cloud_project_id>",
      "VAIS_ENGINE_ID": "<vais_engine_id>"
    }
  }
}
```

If you want to run with Docker, you will need to obtain a service account credential key beforehand and mount its path into the Docker container.

```json
{
  "vais-mcp": {
    "command": "docker",
    "args": [
      "run",
      "-i",
      "--rm",
      "-e",
      "GOOGLE_CLOUD_PROJECT_ID",
      "-e",
      "VAIS_ENGINE_ID",
      "-v",
      "/full/path/to/sa-key.json:/app/secrets/sa-key.json:ro",
      "mrmtsntr/vais-mcp:latest"
    ],
    "env": {
      "GOOGLE_CLOUD_PROJECT_ID": "<google_cloud_project_id>",
      "VAIS_ENGINE_ID": "<vais_engine_id>"
    }
  }
}
```

Note: You can find the Vertex AI Search engine ID in the app url.

```
https://console.cloud.google.com/gen-app-builder/locations/<location>/engines/<engine_id>/overview/system...
```

### Optional Parameters

You can configure the following optional parameters in the environment or server configuration:

- `vais_location`: The location of the Vertex AI Search engine. (Default: "global")
- `page_size`: The number of documents to retrieve as search results. (Default: 5)
- `max_extractive_segment_count`: The maximum number of extractive chunks to retrieve from each document. (Default: 2)
- `log_level`: Specifies the logging level. (Default: "WARNING")
- `IMPERSONATE_SERVICE_ACCOUNT`: The email address of a service account to impersonate for Google Cloud authentication. See the "Google Cloud Authentication" section for details.
- `SOURCE_SA_KEY_PATH`: The path to a service account key file used either directly for authentication or as source credentials for impersonation. See the "Google Cloud Authentication" section for details.

Example:

```json
  "env": {
    "GOOGLE_CLOUD_PROJECT_ID": "<google_cloud_project_id>",
    "VAIS_ENGINE_ID": "<vais_engine_id>",
    "VAIS_LOCATION": "us-central1",
    "PAGE_SIZE": "20",
    "MAX_EXTRACTIVE_SEGMENT_COUNT": "8",
    "LOG_LEVEL": "DEBUG",
    "IMPERSONATE_SERVICE_ACCOUNT": "target-sa@project.iam.gserviceaccount.com",
    "SOURCE_SA_KEY_PATH": "/full/path/to/source-sa-key.json"
  }
```

## Google Cloud Authentication

This MCP server authenticates to Google Cloud using the following methods, taking into account the `IMPERSONATE_SERVICE_ACCOUNT` and `SOURCE_SA_KEY_PATH` environment variables:

- **Service Account Impersonation**:

  - If the `IMPERSONATE_SERVICE_ACCOUNT` environment variable is set to the email address of a target service account, the server will attempt to impersonate that service account.
    - If `SOURCE_SA_KEY_PATH` is also set, the service account key file specified by `SOURCE_SA_KEY_PATH` will be used as the source credentials for impersonation.
    - If `SOURCE_SA_KEY_PATH` is **not** set, Application Default Credentials (ADC) will be used as the source credentials for impersonation.

- **Direct Authentication (No Impersonation)**:
  - If `IMPERSONATE_SERVICE_ACCOUNT` is **not** set:
    - If `SOURCE_SA_KEY_PATH` is set, the server will directly use the service account key file specified by `SOURCE_SA_KEY_PATH` for authentication.
    - If `SOURCE_SA_KEY_PATH` is also **not** set, the server will use ADC for authentication.

ADC automatically find credentials from the environment, such as your local user credentials (set up via `gcloud auth application-default login`) or a service account attached to the compute resource. For more details, see the [official documentation](https://cloud.google.com/docs/authentication/provide-credentials-adc).

**Note:**

- The account used for authentication **must** have the "Discovery Engine Viewer" role (`roles/discoveryengine.viewer`).
  This is required to access Vertex AI Search resources. For more information about roles, see [Vertex AI roles and permissions](https://cloud.google.com/vertex-ai/docs/general/access-control).

- If you are running locally, you can set up ADC by running:
  ```bash
  gcloud auth application-default login
  ```
- For production environments, it is recommended to use a service account with the minimum required permissions.

## Development

### Building

To prepare this package for distribution:

1. Sync dependencies and update lockfile:

```bash
uv sync
```

### Debugging

You can launch the MCP Inspector using following command:

```bash
npx @modelcontextprotocol/inspector uvx vais-mcp@latest GOOGLE_CLOUD_PROJECT_ID=<google_cloud_project_id> VAIS_ENGINE_ID=<vais_engine_id>
```
