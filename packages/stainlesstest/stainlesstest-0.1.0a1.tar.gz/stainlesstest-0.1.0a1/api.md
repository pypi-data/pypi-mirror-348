# Collections

Methods:

- <code title="get /collections/{collection_slug}">client.collections.<a href="./src/stainlesstest/resources/collections.py">retrieve</a>(collection_slug) -> None</code>
- <code title="get /collections">client.collections.<a href="./src/stainlesstest/resources/collections.py">list</a>() -> None</code>

# Deployments

Types:

```python
from stainlesstest.types import (
    DeploymentResponse,
    PredictionRequest,
    PredictionResponse,
    DeploymentListResponse,
)
```

Methods:

- <code title="post /deployments">client.deployments.<a href="./src/stainlesstest/resources/deployments.py">create</a>(\*\*<a href="src/stainlesstest/types/deployment_create_params.py">params</a>) -> <a href="./src/stainlesstest/types/deployment_response.py">DeploymentResponse</a></code>
- <code title="get /deployments/{deployment_owner}/{deployment_name}">client.deployments.<a href="./src/stainlesstest/resources/deployments.py">retrieve</a>(deployment_name, \*, deployment_owner) -> <a href="./src/stainlesstest/types/deployment_response.py">DeploymentResponse</a></code>
- <code title="patch /deployments/{deployment_owner}/{deployment_name}">client.deployments.<a href="./src/stainlesstest/resources/deployments.py">update</a>(deployment_name, \*, deployment_owner, \*\*<a href="src/stainlesstest/types/deployment_update_params.py">params</a>) -> <a href="./src/stainlesstest/types/deployment_response.py">DeploymentResponse</a></code>
- <code title="get /deployments">client.deployments.<a href="./src/stainlesstest/resources/deployments.py">list</a>() -> <a href="./src/stainlesstest/types/deployment_list_response.py">DeploymentListResponse</a></code>
- <code title="delete /deployments/{deployment_owner}/{deployment_name}">client.deployments.<a href="./src/stainlesstest/resources/deployments.py">delete</a>(deployment_name, \*, deployment_owner) -> None</code>
- <code title="post /deployments/{deployment_owner}/{deployment_name}/predictions">client.deployments.<a href="./src/stainlesstest/resources/deployments.py">create_prediction</a>(deployment_name, \*, deployment_owner, \*\*<a href="src/stainlesstest/types/deployment_create_prediction_params.py">params</a>) -> <a href="./src/stainlesstest/types/prediction_response.py">PredictionResponse</a></code>

# Files

Types:

```python
from stainlesstest.types import File, FileListResponse
```

Methods:

- <code title="post /files">client.files.<a href="./src/stainlesstest/resources/files.py">create</a>(\*\*<a href="src/stainlesstest/types/file_create_params.py">params</a>) -> <a href="./src/stainlesstest/types/file.py">File</a></code>
- <code title="get /files/{file_id}">client.files.<a href="./src/stainlesstest/resources/files.py">retrieve</a>(file_id) -> <a href="./src/stainlesstest/types/file.py">File</a></code>
- <code title="get /files">client.files.<a href="./src/stainlesstest/resources/files.py">list</a>() -> <a href="./src/stainlesstest/types/file_list_response.py">FileListResponse</a></code>
- <code title="delete /files/{file_id}">client.files.<a href="./src/stainlesstest/resources/files.py">delete</a>(file_id) -> None</code>
- <code title="get /files/{file_id}/download">client.files.<a href="./src/stainlesstest/resources/files.py">download</a>(file_id, \*\*<a href="src/stainlesstest/types/file_download_params.py">params</a>) -> BinaryAPIResponse</code>

# Hardware

Types:

```python
from stainlesstest.types import HardwareListResponse
```

Methods:

- <code title="get /hardware">client.hardware.<a href="./src/stainlesstest/resources/hardware.py">list</a>() -> <a href="./src/stainlesstest/types/hardware_list_response.py">HardwareListResponse</a></code>

# Models

Types:

```python
from stainlesstest.types import ModelListResponse, ModelGetReadmeResponse
```

Methods:

- <code title="post /models">client.models.<a href="./src/stainlesstest/resources/models/models.py">create</a>(\*\*<a href="src/stainlesstest/types/model_create_params.py">params</a>) -> None</code>
- <code title="get /models/{model_owner}/{model_name}">client.models.<a href="./src/stainlesstest/resources/models/models.py">retrieve</a>(model_name, \*, model_owner) -> None</code>
- <code title="get /models">client.models.<a href="./src/stainlesstest/resources/models/models.py">list</a>() -> <a href="./src/stainlesstest/types/model_list_response.py">ModelListResponse</a></code>
- <code title="delete /models/{model_owner}/{model_name}">client.models.<a href="./src/stainlesstest/resources/models/models.py">delete</a>(model_name, \*, model_owner) -> None</code>
- <code title="post /models/{model_owner}/{model_name}/predictions">client.models.<a href="./src/stainlesstest/resources/models/models.py">create_prediction</a>(model_name, \*, model_owner, \*\*<a href="src/stainlesstest/types/model_create_prediction_params.py">params</a>) -> <a href="./src/stainlesstest/types/prediction_response.py">PredictionResponse</a></code>
- <code title="get /models/{model_owner}/{model_name}/readme">client.models.<a href="./src/stainlesstest/resources/models/models.py">get_readme</a>(model_name, \*, model_owner) -> str</code>
- <code title="get /models/{model_owner}/{model_name}/examples">client.models.<a href="./src/stainlesstest/resources/models/models.py">list_examples</a>(model_name, \*, model_owner) -> None</code>
- <code title="query /models">client.models.<a href="./src/stainlesstest/resources/models/models.py">search</a>(\*\*<a href="src/stainlesstest/types/model_search_params.py">params</a>) -> None</code>

## Versions

Types:

```python
from stainlesstest.types.models import SchemasTraining
```

Methods:

- <code title="get /models/{model_owner}/{model_name}/versions/{version_id}">client.models.versions.<a href="./src/stainlesstest/resources/models/versions.py">retrieve</a>(version_id, \*, model_owner, model_name) -> None</code>
- <code title="get /models/{model_owner}/{model_name}/versions">client.models.versions.<a href="./src/stainlesstest/resources/models/versions.py">list</a>(model_name, \*, model_owner) -> None</code>
- <code title="delete /models/{model_owner}/{model_name}/versions/{version_id}">client.models.versions.<a href="./src/stainlesstest/resources/models/versions.py">delete</a>(version_id, \*, model_owner, model_name) -> None</code>
- <code title="post /models/{model_owner}/{model_name}/versions/{version_id}/trainings">client.models.versions.<a href="./src/stainlesstest/resources/models/versions.py">create_training</a>(version_id, \*, model_owner, model_name, \*\*<a href="src/stainlesstest/types/models/version_create_training_params.py">params</a>) -> <a href="./src/stainlesstest/types/models/schemas_training.py">SchemasTraining</a></code>

# Predictions

Types:

```python
from stainlesstest.types import PredictionListResponse
```

Methods:

- <code title="post /predictions">client.predictions.<a href="./src/stainlesstest/resources/predictions.py">create</a>(\*\*<a href="src/stainlesstest/types/prediction_create_params.py">params</a>) -> <a href="./src/stainlesstest/types/prediction_response.py">PredictionResponse</a></code>
- <code title="get /predictions/{prediction_id}">client.predictions.<a href="./src/stainlesstest/resources/predictions.py">retrieve</a>(prediction_id) -> <a href="./src/stainlesstest/types/prediction_response.py">PredictionResponse</a></code>
- <code title="get /predictions">client.predictions.<a href="./src/stainlesstest/resources/predictions.py">list</a>(\*\*<a href="src/stainlesstest/types/prediction_list_params.py">params</a>) -> <a href="./src/stainlesstest/types/prediction_list_response.py">PredictionListResponse</a></code>
- <code title="post /predictions/{prediction_id}/cancel">client.predictions.<a href="./src/stainlesstest/resources/predictions.py">cancel</a>(prediction_id) -> <a href="./src/stainlesstest/types/prediction_response.py">PredictionResponse</a></code>

# Trainings

Types:

```python
from stainlesstest.types import TrainingListResponse
```

Methods:

- <code title="get /trainings/{training_id}">client.trainings.<a href="./src/stainlesstest/resources/trainings.py">retrieve</a>(training_id) -> <a href="./src/stainlesstest/types/models/schemas_training.py">SchemasTraining</a></code>
- <code title="get /trainings">client.trainings.<a href="./src/stainlesstest/resources/trainings.py">list</a>() -> <a href="./src/stainlesstest/types/training_list_response.py">TrainingListResponse</a></code>
- <code title="post /trainings/{training_id}/cancel">client.trainings.<a href="./src/stainlesstest/resources/trainings.py">cancel</a>(training_id) -> <a href="./src/stainlesstest/types/models/schemas_training.py">SchemasTraining</a></code>

# Webhooks

## Default

Types:

```python
from stainlesstest.types.webhooks import DefaultRetrieveSecretResponse
```

Methods:

- <code title="get /webhooks/default/secret">client.webhooks.default.<a href="./src/stainlesstest/resources/webhooks/default.py">retrieve_secret</a>() -> <a href="./src/stainlesstest/types/webhooks/default_retrieve_secret_response.py">DefaultRetrieveSecretResponse</a></code>
