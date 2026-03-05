# API Reference - IBM MDM Match Decision Explorer

This document provides detailed API reference for developers working with or extending the MDM Match Decision Explorer.

## Table of Contents

- [MDM Client API](#mdm-client-api)
- [Authentication API](#authentication-api)
- [Data Models](#data-models)
- [UI Components](#ui-components)
- [Utility Functions](#utility-functions)
- [Configuration](#configuration)

---

## MDM Client API

### `MDMClient`

Main client for interacting with IBM MDM (Match 360) API.

**Location**: `src/mdm/client.py`

#### Constructor

```python
MDMClient(
    base_url: str,
    api_token: Optional[str] = None,
    api_key: Optional[str] = None,
    timeout: int = 30
)
```

**Parameters**:
- `base_url` (str): MDM API base URL (e.g., `https://instance.appdomain.cloud`)
- `api_token` (Optional[str]): Bearer token for authentication (expires hourly)
- `api_key` (Optional[str]): IBM Cloud API key for automatic token management
- `timeout` (int): Request timeout in seconds (default: 30)

**Example**:
```python
# Using API key (recommended)
client = MDMClient(
    base_url="https://mdm-instance.appdomain.cloud",
    api_key="your_ibm_cloud_api_key"
)

# Using bearer token
client = MDMClient(
    base_url="https://mdm-instance.appdomain.cloud",
    api_token="your_bearer_token"
)
```

#### Methods

##### `compare_entities()`

Compare two person entities and return match decision.

```python
def compare_entities(
    entity1: Dict[str, Any],
    entity2: Dict[str, Any],
    crn: str,
    record_number1: Optional[str] = None,
    record_number2: Optional[str] = None,
    debug: bool = False
) -> Optional[Dict[str, Any]]
```

**Parameters**:
- `entity1` (Dict): First entity data
- `entity2` (Dict): Second entity data
- `crn` (str): Cloud Resource Name
- `record_number1` (Optional[str]): Record number for entity 1 (if existing)
- `record_number2` (Optional[str]): Record number for entity 2 (if existing)
- `debug` (bool): Include debug information in response

**Returns**:
- `Dict[str, Any]`: Match result containing:
  - `similarity` (float): Match probability (0.0 to 1.0)
  - `match_decision` (bool): Whether entities match
  - `field_scores` (Dict): Individual field match scores
  - `debug_info` (Optional[Dict]): Debug details if enabled
- `None`: If comparison fails

**Raises**:
- `ValueError`: Invalid entity data
- `ConnectionError`: API unreachable
- `requests.HTTPError`: HTTP error from API

**Example**:
```python
result = client.compare_entities(
    entity1={
        "legal_name": {
            "given_name": "John",
            "last_name": "Smith"
        },
        "birth_date": "1980-01-15"
    },
    entity2={
        "legal_name": {
            "given_name": "Jon",
            "last_name": "Smith"
        },
        "birth_date": "1980-01-15"
    },
    crn="crn:v1:bluemix:public:mdm-oc:us-south:a/account:instance::",
    debug=True
)

print(f"Match probability: {result['similarity']:.2%}")
print(f"Match decision: {result['match_decision']}")
```

##### `test_connection()`

Test connectivity to MDM API.

```python
def test_connection() -> bool
```

**Returns**:
- `bool`: True if connection successful, False otherwise

**Example**:
```python
if client.test_connection():
    print("Connected to MDM API")
else:
    print("Connection failed")
```

---

## Authentication API

### `TokenManager`

Manages IBM Cloud IAM token lifecycle with automatic refresh.

**Location**: `src/mdm/auth.py`

#### Constructor

```python
TokenManager(
    api_key: str,
    cache_file: Optional[str] = None
)
```

**Parameters**:
- `api_key` (str): IBM Cloud API key
- `cache_file` (Optional[str]): Path to token cache file (default: `~/.mdm_token_cache.json`)

**Example**:
```python
manager = TokenManager(api_key="your_api_key")
```

#### Methods

##### `get_token()`

Get current valid token, refreshing if necessary.

```python
def get_token() -> str
```

**Returns**:
- `str`: Valid bearer token

**Raises**:
- `AuthenticationError`: If token refresh fails

**Example**:
```python
token = manager.get_token()
headers = {"Authorization": f"Bearer {token}"}
```

##### `refresh_token()`

Manually refresh the token.

```python
def refresh_token() -> str
```

**Returns**:
- `str`: New bearer token

**Example**:
```python
new_token = manager.refresh_token()
```

##### `get_token_status()`

Get current token status information.

```python
def get_token_status() -> Dict[str, Any]
```

**Returns**:
- `Dict[str, Any]`: Status containing:
  - `valid` (bool): Whether token is valid
  - `expires_in_minutes` (int): Minutes until expiration
  - `expires_at` (str): Expiration timestamp

**Example**:
```python
status = manager.get_token_status()
print(f"Token valid: {status['valid']}")
print(f"Expires in: {status['expires_in_minutes']} minutes")
```

---

## Data Models

### `PersonEntity`

Pydantic model for person entity data.

**Location**: `src/mdm/models.py`

```python
class PersonEntity(BaseModel):
    legal_name: Optional[LegalName] = None
    birth_date: Optional[str] = None
    gender: Optional[str] = None
    primary_residence: Optional[PrimaryResidence] = None
    home_telephone: Optional[str] = None
    mobile_telephone: Optional[str] = None
    personal_email: Optional[str] = None
    social_security_number: Optional[str] = None
    drivers_license_number: Optional[str] = None
    passport_number: Optional[str] = None
    record_last_updated: Optional[int] = None
```

**Example**:
```python
from src.mdm.models import PersonEntity, LegalName

entity = PersonEntity(
    legal_name=LegalName(
        given_name="John",
        last_name="Smith"
    ),
    birth_date="1980-01-15",
    gender="M"
)

# Validate and convert to dict
entity_dict = entity.model_dump(exclude_none=True)
```

### `LegalName`

```python
class LegalName(BaseModel):
    given_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    prefix: Optional[str] = None
    suffix: Optional[str] = None
    generation: Optional[str] = None
```

### `PrimaryResidence`

```python
class PrimaryResidence(BaseModel):
    address_line1: Optional[str] = None
    city: Optional[str] = None
    province_state: Optional[str] = None
    zip_postal_code: Optional[str] = None
    country: Optional[str] = None
    county: Optional[str] = None
    residence_number: Optional[str] = None
```

### `CompareRequest`

```python
class CompareRequest(BaseModel):
    do_matching: bool = True
    record_type: str = "person"
    records: List[PersonEntity]
```

### `CompareResponse`

```python
class CompareResponse(BaseModel):
    similarity: float
    match_decision: bool
    field_scores: Optional[Dict[str, float]] = None
    debug_info: Optional[Dict[str, Any]] = None
```

---

## UI Components

### Entity Input Forms

**Location**: `src/ui/entity_input.py`

#### `render_entity_form()`

Render entity input form with all fields.

```python
def render_entity_form(
    key_prefix: str,
    title: str
) -> Dict[str, Any]
```

**Parameters**:
- `key_prefix` (str): Unique prefix for form widgets (e.g., "entity1")
- `title` (str): Form title

**Returns**:
- `Dict[str, Any]`: Entity data dictionary

**Example**:
```python
entity1_data = render_entity_form(
    key_prefix="entity1",
    title="Entity 1"
)
```

### Visualizations

**Location**: `src/ui/visualizations.py`

#### `render_match_results()`

Display match results with visualizations.

```python
def render_match_results(
    result: Dict[str, Any],
    entity1: Dict[str, Any],
    entity2: Dict[str, Any]
) -> None
```

**Parameters**:
- `result` (Dict): Match result from API
- `entity1` (Dict): First entity data
- `entity2` (Dict): Second entity data

**Example**:
```python
render_match_results(
    result=comparison_result,
    entity1=entity1_data,
    entity2=entity2_data
)
```

#### `create_gauge_chart()`

Create a gauge chart for match score.

```python
def create_gauge_chart(
    value: float,
    title: str,
    max_value: float = 1.0
) -> go.Figure
```

**Parameters**:
- `value` (float): Current value
- `title` (str): Chart title
- `max_value` (float): Maximum value (default: 1.0)

**Returns**:
- `go.Figure`: Plotly figure object

**Example**:
```python
fig = create_gauge_chart(
    value=0.85,
    title="Match Probability",
    max_value=1.0
)
st.plotly_chart(fig)
```

### Sample Data

**Location**: `src/ui/sample_data.py`

#### `load_sample_scenarios()`

Load sample entity scenarios from JSON.

```python
def load_sample_scenarios() -> Dict[str, Dict[str, Any]]
```

**Returns**:
- `Dict[str, Dict]`: Dictionary of scenarios

**Example**:
```python
scenarios = load_sample_scenarios()
fuzzy_match = scenarios["fuzzy_match"]
```

#### `get_scenario_names()`

Get list of available scenario names.

```python
def get_scenario_names() -> List[str]
```

**Returns**:
- `List[str]`: Scenario names

---

## Utility Functions

### Configuration

**Location**: `src/utils/config.py`

#### `get_config()`

Get application configuration from environment.

```python
def get_config() -> AppConfig
```

**Returns**:
- `AppConfig`: Configuration object

**Example**:
```python
config = get_config()
print(config.mdm_api_base_url)
print(config.mdm_crn)
```

#### `AppConfig`

```python
class AppConfig(BaseModel):
    mdm_api_base_url: str
    mdm_api_key: Optional[str] = None
    mdm_api_token: Optional[str] = None
    mdm_crn: str
    mdm_entity_type: str = "person_entity"
    mdm_record_type: str = "person"
    app_title: str = "IBM MDM Match Decision Explorer"
    app_icon: str = "🔍"
    debug_mode: bool = False
```

### Helpers

**Location**: `src/utils/helpers.py`

#### `format_timestamp()`

Format Unix timestamp to readable string.

```python
def format_timestamp(
    timestamp_ms: int,
    format: str = "%Y-%m-%d %H:%M:%S"
) -> str
```

**Parameters**:
- `timestamp_ms` (int): Unix timestamp in milliseconds
- `format` (str): Output format string

**Returns**:
- `str`: Formatted timestamp

**Example**:
```python
formatted = format_timestamp(1709632800000)
# Output: "2024-03-05 10:00:00"
```

#### `validate_entity_data()`

Validate entity data structure.

```python
def validate_entity_data(
    entity: Dict[str, Any]
) -> Tuple[bool, Optional[str]]
```

**Parameters**:
- `entity` (Dict): Entity data to validate

**Returns**:
- `Tuple[bool, Optional[str]]`: (is_valid, error_message)

**Example**:
```python
is_valid, error = validate_entity_data(entity_data)
if not is_valid:
    print(f"Validation error: {error}")
```

---

## Configuration

### Environment Variables

All configuration is managed through environment variables in `.env` file.

#### Required Variables

```bash
# MDM API endpoint
MDM_API_BASE_URL=https://your-instance.appdomain.cloud

# Authentication (choose one)
MDM_API_KEY=your_api_key          # Recommended
# OR
MDM_API_TOKEN=your_bearer_token   # Alternative

# MDM instance identifier
MDM_CRN=crn:v1:bluemix:public:mdm-oc:region:a/account:instance::
```

#### Optional Variables

```bash
# Entity configuration
MDM_ENTITY_TYPE=person_entity     # Default: person_entity
MDM_RECORD_TYPE=person            # Default: person

# Application settings
APP_TITLE=MDM Match Explorer      # Default: IBM MDM Match Decision Explorer
APP_ICON=🔍                       # Default: 🔍
DEBUG_MODE=false                  # Default: false
```

### Accessing Configuration

```python
from src.utils.config import get_config

config = get_config()

# Access values
base_url = config.mdm_api_base_url
api_key = config.mdm_api_key
crn = config.mdm_crn
```

---

## Error Handling

### Exception Types

#### `AuthenticationError`

Raised when authentication fails.

```python
from src.mdm.auth import AuthenticationError

try:
    token = manager.get_token()
except AuthenticationError as e:
    print(f"Auth failed: {e}")
```

#### `ValidationError`

Raised when data validation fails (from Pydantic).

```python
from pydantic import ValidationError

try:
    entity = PersonEntity(**data)
except ValidationError as e:
    print(f"Invalid data: {e}")
```

### Error Response Format

API errors return structured responses:

```python
{
    "error": {
        "code": "INVALID_REQUEST",
        "message": "Invalid entity data",
        "details": {
            "field": "birth_date",
            "issue": "Invalid date format"
        }
    }
}
```

---

## Best Practices

### 1. Use API Keys Over Tokens

```python
# Good - automatic token refresh
client = MDMClient(
    base_url=base_url,
    api_key=api_key
)

# Avoid - manual token management
client = MDMClient(
    base_url=base_url,
    api_token=bearer_token  # Expires hourly!
)
```

### 2. Validate Data Before API Calls

```python
from src.mdm.models import PersonEntity

# Validate using Pydantic
try:
    entity = PersonEntity(**entity_data)
    validated_data = entity.model_dump(exclude_none=True)
except ValidationError as e:
    print(f"Invalid data: {e}")
    return
```

### 3. Handle Errors Gracefully

```python
try:
    result = client.compare_entities(entity1, entity2, crn)
    if result:
        print(f"Match: {result['similarity']}")
    else:
        print("Comparison failed")
except ConnectionError:
    print("Cannot connect to MDM API")
except ValueError as e:
    print(f"Invalid data: {e}")
```

### 4. Use Debug Mode for Development

```python
# Enable debug mode
result = client.compare_entities(
    entity1, entity2, crn,
    debug=True  # Get detailed API response
)

if result and "debug_info" in result:
    print(result["debug_info"])
```

### 5. Cache Token Manager Instance

```python
# Good - reuse token manager
@st.cache_resource
def get_token_manager():
    return TokenManager(api_key=config.mdm_api_key)

manager = get_token_manager()

# Avoid - creating new instance each time
manager = TokenManager(api_key=api_key)  # Don't do this repeatedly
```

---

## Examples

### Complete Comparison Workflow

```python
from src.mdm.client import MDMClient
from src.mdm.models import PersonEntity, LegalName
from src.utils.config import get_config

# 1. Load configuration
config = get_config()

# 2. Create client
client = MDMClient(
    base_url=config.mdm_api_base_url,
    api_key=config.mdm_api_key
)

# 3. Prepare entities
entity1 = PersonEntity(
    legal_name=LegalName(
        given_name="John",
        last_name="Smith"
    ),
    birth_date="1980-01-15"
).model_dump(exclude_none=True)

entity2 = PersonEntity(
    legal_name=LegalName(
        given_name="Jon",
        last_name="Smith"
    ),
    birth_date="1980-01-15"
).model_dump(exclude_none=True)

# 4. Compare
result = client.compare_entities(
    entity1=entity1,
    entity2=entity2,
    crn=config.mdm_crn,
    debug=True
)

# 5. Process results
if result:
    print(f"Similarity: {result['similarity']:.2%}")
    print(f"Match: {result['match_decision']}")
    
    if "field_scores" in result:
        for field, score in result["field_scores"].items():
            print(f"  {field}: {score:.2f}")
```

---

## Support

For questions or issues:
- Check [README.md](README.md) for general documentation
- See [QUICKSTART.md](QUICKSTART.md) for setup help
- Review [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines
- Create an issue in the repository

---

**Last Updated**: 2026-03-05  
**Version**: 1.0.0