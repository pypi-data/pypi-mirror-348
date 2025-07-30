# AzWrap

A Python package that provides a streamlined wrapper for Azure resource management, making it easier to work with Azure services including:

- Azure Storage
- Azure AI Search
- Azure OpenAI

## Installation

```bash
pip install azwrap
```

## Configuration

AzWrap requires Azure credentials to be set either as environment variables or in a `.env` file:

```
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
AZURE_SUBSCRIPTION_ID=your-subscription-id
```

## CLI Usage

Once installed, you can use the CLI to manage Azure resources. The CLI is structured around resource types and operations.

### General Options

```bash
# Get help on CLI usage
azwrap --help

# Change output format (text, json, table)
azwrap --output json <command>

# Enable verbose output
azwrap --verbose <command>
```

### Subscription Management

```bash
# List all available subscriptions
azwrap subscription list

# Get details of a specific subscription
azwrap subscription get --subscription-id your-subscription-id
```

### Resource Group Management

```bash
# List resource groups in a subscription
azwrap resource-group list

# Create a new resource group
azwrap resource-group create --name my-resource-group --location eastus

# Get details of a specific resource group
azwrap resource-group get --name my-resource-group
```

### Storage Management

```bash
# List storage accounts
azwrap storage list

# Create a storage account
azwrap storage create --name mystorageacct --resource-group my-resource-group --location eastus

# List containers in a storage account
azwrap storage containers --name mystorageacct --resource-group my-resource-group

# List blobs in a container
azwrap storage blobs --account mystorageacct --resource-group my-resource-group --container mycontainer

# View folder structure in a container
azwrap storage folder-structure --account mystorageacct --resource-group my-resource-group --container mycontainer
```

### Azure AI Search

```bash
# List search services
azwrap search list

# Create a search service
azwrap search create --name mysearchservice --resource-group my-resource-group --location eastus --sku basic

# List indexes in a search service
azwrap index list --search-service mysearchservice --resource-group my-resource-group

# Create an index (with JSON fields definition)
azwrap index create --name myindex --search-service mysearchservice --resource-group my-resource-group --fields '[{"name":"id","type":"SimpleField","key":true,"type_name":"Edm.String"},{"name":"content","type":"SearchableField","type_name":"Edm.String"}]'

# Copy an index
azwrap index copy --source sourceindex --target targetindex --search-service mysearchservice --resource-group my-resource-group
```

### Data Sources and Indexers

```bash
# List data sources
azwrap datasource list --search-service mysearchservice --resource-group my-resource-group

# Create a data source connection
azwrap datasource create --name mydatasource --type azureblob --connection-string "DefaultEndpointsProtocol=https;AccountName=myaccount;AccountKey=key;EndpointSuffix=core.windows.net" --container mycontainer --search-service mysearchservice --resource-group my-resource-group

# Create an indexer
azwrap indexer create --name myindexer --data-source mydatasource --target-index myindex --search-service mysearchservice --resource-group my-resource-group

# Run an indexer
azwrap indexer run --name myindexer --search-service mysearchservice --resource-group my-resource-group

# Check indexer status
azwrap indexer status --name myindexer --search-service mysearchservice --resource-group my-resource-group
```

### Skillsets

```bash
# List skillsets
azwrap skillset list --search-service mysearchservice --resource-group my-resource-group

# Create a skillset
azwrap skillset create --name myskillset --search-service mysearchservice --resource-group my-resource-group --skills '[{"@odata.type": "#Microsoft.Skills.Text.EntityRecognitionSkill", "name": "entity-recognition", "description": "Extracts entities", "context": "/document", "categories": ["Person", "Location", "Organization"], "defaultLanguageCode": "en", "inputs": [{"name": "text", "source": "/document/content"}], "outputs": [{"name": "persons", "targetName": "people"}, {"name": "locations", "targetName": "places"}, {"name": "organizations", "targetName": "organizations"}]}]'
```

### Azure OpenAI Service

```bash
# List OpenAI services
azwrap ai list

# Get details of an OpenAI service
azwrap ai get --name myopenai --resource-group my-resource-group

# List available models
azwrap ai models --name myopenai --resource-group my-resource-group

# List deployments
azwrap ai deployments --name myopenai --resource-group my-resource-group

# Create a deployment
azwrap ai deploy --name gpt35turbo --model gpt-35-turbo --service myopenai --resource-group my-resource-group --capacity 1

# Generate embeddings
azwrap ai embedding --text "This is a sample text" --service myopenai --resource-group my-resource-group --model text-embedding-3-small --api-version 2023-12-01-preview

# Generate chat completion
azwrap ai chat --message "Tell me about Azure" --service myopenai --resource-group my-resource-group --model gpt35turbo --api-version 2023-12-01-preview --system "You are a helpful assistant"
```

## Python API Usage

### Identity Management

```python
from azwrap import Identity

# Create an identity with your Azure credentials
identity = Identity(tenant_id, client_id, client_secret)

# Get a list of subscriptions
subscriptions = identity.get_subscriptions()

# Get a specific subscription
subscription = identity.get_subscription(subscription_id)
```

### Resource Management

```python
from azwrap import Subscription, ResourceGroup

# Work with resource groups
resource_group = subscription.get_resource_group(group_name)

# Create a new resource group
new_group = subscription.create_resource_group(group_name, location)
```

### Storage Management

```python
from azwrap import StorageAccount, Container

# Get a storage account
storage_account = resource_group.get_storage_account(account_name)

# Create a new storage account
new_account = resource_group.create_storage_account(account_name, location)

# Work with blob containers
container = storage_account.get_container(container_name)
blobs = container.get_blobs()
```

### Azure AI Search

```python
from azwrap import SearchService, SearchIndex, get_std_vector_search
from azure.search.documents.indexes.models import (
    SearchField, SearchFieldDataType, SimpleField, SearchableField
)

# Get a search service
search_service = subscription.get_search_service(service_name)

# Create a new search service
new_service = resource_group.create_search_service(name, location)

# Define fields for an index
fields = [
    SimpleField(name="id", type=SearchFieldDataType.String, key=True),
    SearchableField(name="content", type=SearchFieldDataType.String, analyzer_name="en.microsoft")
]

# Create a search index
index = search_service.create_or_update_index("my-index", fields)

# Add vector search capability
vector_search = get_std_vector_search()
```

### Azure OpenAI

```python
from azwrap import AIService, OpenAIClient

# Get an OpenAI service
ai_service = resource_group.get_ai_service(service_name)

# Get OpenAI client with Azure credentials
openai_client = ai_service.get_OpenAIClient(api_version="2023-05-15")

# Generate embeddings
embeddings = openai_client.generate_embeddings("Your text here", model="deployment-name")

# Generate chat completions
response = openai_client.generate_chat_completion(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Tell me about Azure."}
    ],
    model="deployment-name",
    temperature=0.7,
    max_tokens=800
)
```

## Development

To set up the development environment:

```bash
# Clone the repository
git clone https://github.com/yourusername/azwrap.git
cd azwrap

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies for development
uv sync

# Build the package
python -m build

# Install in development mode
pip install -e .
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.