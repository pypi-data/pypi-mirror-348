# MCP Server for Vertex AI Search

MCP server to search private data in Vertex AI Search.

## Tools

- `search`: Search for Vertex AI Search and returns result chunks.
  Returns a list of dictionaries, each containing the title of the source document and the extracted content chunk. Example:

```json
[
  {
    "title": "Sample Document Title 1",
    "content": "Extracted text segment from the document."
  },
  {
    "title": "Sample Document Title 2",
    "content": "Another extracted text segment."
  }
]
```

## Prerequisites

1. Install uv from [Astral](https://docs.astral.sh/uv/getting-started/installation/) or the [GitHub README](https://github.com/astral-sh/uv#installation)
2. Install Python 3.13 using `uv python install 3.13`
3. Create a Vertex AI Search app  
   i. [Official Document](https://cloud.google.com/generative-ai-app-builder/docs/create-engine-es)

## Configuration

Add the following to your server configuration (preferred):

```json
{
  "vais-mcp": {
    "command": "uvx",
    "args": ["vais-mcp@latest"],
    "env": {
      "GOOGLE_CLOUD_PROJECT_ID": "<your_google_cloud_project_id>",
      "VAIS_ENGINE_ID": "<your_vais_engine_id>"
    }
  }
}
```

Create a `.env` file in the working directory with the following required variables:

```
GOOGLE_CLOUD_PROJECT_ID=your_google_cloud_project_id
VAIS_ENGINE_ID=your_vais_engine_id
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

Example:

```json
  "env": {
    "GOOGLE_CLOUD_PROJECT_ID": "<your_google_cloud_project_id>",
    "VAIS_ENGINE_ID": "<your_vais_engine_id>",
    "VAIS_LOCATION": "us-central1",
    "PAGE_SIZE": "20",
    "MAX_EXTRACTIVE_SEGMENT_COUNT": "8",
    "LOG_LEVEL": "DEBUG"
  }
```

## Google Cloud Authentication

This MCP server authenticates to Google Cloud using the following methods:

- If the `IMPERSONATE_SERVICE_ACCOUNT` environment variable is **not** specified, authentication is performed using [Application Default Credentials (ADC)](https://cloud.google.com/docs/authentication/provide-credentials-adc).
  ADC automatically finds your credentials from the environment, such as your local user credentials (set up via `gcloud auth application-default login`) or a service account attached to the compute resource. For more details, see the [official documentation](https://cloud.google.com/docs/authentication).

- If you wish to use a specific service account for authentication, set the `IMPERSONATE_SERVICE_ACCOUNT` environment variable to the email address of the service account you want to impersonate.

Example:

```json
  "env": {
    "GOOGLE_CLOUD_PROJECT_ID": "your_google_cloud_project_id",
    "VAIS_ENGINE_ID": "your_vais_engine_id",
    "IMPERSONATE_SERVICE_ACCOUNT": "your-service-account@your-project.iam.gserviceaccount.com"
  }
```

- The account used for authentication **must** have the "Vertex AI User" role (`roles/aiplatform.user`).
  This is required to access Vertex AI Search resources. For more information about roles, see [Vertex AI roles and permissions](https://cloud.google.com/vertex-ai/docs/general/access-control).

**Note:**

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
npx @modelcontextprotocol/inspector uvx vais_mcp@latest
```
