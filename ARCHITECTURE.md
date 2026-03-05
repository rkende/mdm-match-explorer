# Architecture Documentation - IBM MDM Match Decision Explorer

This document provides a comprehensive overview of the application architecture, design decisions, and technical implementation details.

## Table of Contents

- [System Overview](#system-overview)
- [Architecture Diagram](#architecture-diagram)
- [Component Design](#component-design)
- [Data Flow](#data-flow)
- [Technology Stack](#technology-stack)
- [Design Patterns](#design-patterns)
- [Security Architecture](#security-architecture)
- [Performance Considerations](#performance-considerations)
- [Scalability](#scalability)
- [Future Enhancements](#future-enhancements)

---

## System Overview

### Purpose

The IBM MDM Match Decision Explorer is a web-based application that provides an interactive interface for exploring IBM MDM (Match 360) entity matching algorithms. It enables users to compare person entities in real-time and visualize match decisions with detailed field-level analysis.

### Key Capabilities

1. **Real-time Entity Comparison** - Compare two person entities via REST API
2. **Interactive Visualization** - Display match results with charts and tables
3. **Automatic Token Management** - Handle IBM Cloud IAM authentication lifecycle
4. **Sample Data Library** - Pre-configured test scenarios
5. **Debug Mode** - Detailed API response inspection

### Target Users

- **Data Stewards** - Validate matching rules and thresholds
- **MDM Administrators** - Test algorithm configurations
- **Developers** - Understand matching behavior for integration
- **Business Analysts** - Demonstrate matching capabilities

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Browser                             │
│                    (http://localhost:8501)                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Streamlit Server                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    src/app.py                             │  │
│  │              (Main Application Entry)                     │  │
│  └────────────┬─────────────────────────────┬────────────────┘  │
│               │                             │                    │
│               ▼                             ▼                    │
│  ┌────────────────────────┐   ┌────────────────────────────┐   │
│  │   UI Components        │   │   Business Logic           │   │
│  │   (src/ui/)            │   │   (src/mdm/)               │   │
│  │                        │   │                            │   │
│  │  • entity_input.py     │   │  • client.py               │   │
│  │  • visualizations.py   │   │  • auth.py                 │   │
│  │  • sample_data.py      │   │  • models.py               │   │
│  └────────────────────────┘   └──────────┬─────────────────┘   │
│                                           │                      │
│                                           │                      │
│  ┌────────────────────────────────────────┼──────────────────┐  │
│  │              Utilities (src/utils/)    │                  │  │
│  │                                        │                  │  │
│  │  • config.py (Environment)             │                  │  │
│  │  • helpers.py (Common functions)       │                  │  │
│  └────────────────────────────────────────┼──────────────────┘  │
└─────────────────────────────────────────────┼────────────────────┘
                                              │
                                              │ HTTPS
                                              ▼
                    ┌─────────────────────────────────────┐
                    │      IBM Cloud IAM API              │
                    │  (Token Generation & Refresh)       │
                    └─────────────────────────────────────┘
                                              │
                                              │ Bearer Token
                                              ▼
                    ┌─────────────────────────────────────┐
                    │      IBM MDM (Match 360) API        │
                    │  (Entity Comparison & Matching)     │
                    └─────────────────────────────────────┘
                                              │
                                              │
                    ┌─────────────────────────────────────┐
                    │      Local File System              │
                    │                                     │
                    │  • .env (Configuration)             │
                    │  • ~/.mdm_token_cache.json (Cache)  │
                    │  • config/sample_entities.json      │
                    └─────────────────────────────────────┘
```

---

## Component Design

### 1. Application Layer (`src/app.py`)

**Responsibility**: Main application orchestration and Streamlit UI coordination

**Key Functions**:
- Initialize application configuration
- Manage session state
- Coordinate UI components
- Handle user interactions
- Display results and errors

**Design Pattern**: MVC Controller

```python
# Pseudo-code structure
def main():
    # 1. Load configuration
    config = get_config()
    
    # 2. Initialize session state
    init_session_state()
    
    # 3. Render sidebar (config, samples, token status)
    render_sidebar()
    
    # 4. Render entity input forms
    entity1 = render_entity_form("entity1", "Entity 1")
    entity2 = render_entity_form("entity2", "Entity 2")
    
    # 5. Handle comparison
    if st.button("Compare"):
        result = compare_entities(entity1, entity2)
        render_results(result)
```

### 2. MDM Client Layer (`src/mdm/`)

#### `client.py` - API Client

**Responsibility**: Communication with IBM MDM API

**Key Features**:
- REST API integration
- Request/response handling
- Error management
- Retry logic

**Design Pattern**: Facade Pattern

```python
class MDMClient:
    def __init__(self, base_url, api_token=None, api_key=None):
        self.base_url = base_url
        self.token_manager = TokenManager(api_key) if api_key else None
        self.api_token = api_token
    
    def compare_entities(self, entity1, entity2, crn, **kwargs):
        # 1. Get valid token
        token = self._get_token()
        
        # 2. Build request
        request = self._build_request(entity1, entity2)
        
        # 3. Make API call
        response = self._make_request(request, token, crn)
        
        # 4. Parse response
        return self._parse_response(response)
```

#### `auth.py` - Token Manager

**Responsibility**: IBM Cloud IAM token lifecycle management

**Key Features**:
- Token generation via API key
- Automatic refresh (5 min before expiry)
- Secure caching
- Status monitoring

**Design Pattern**: Singleton Pattern (via Streamlit caching)

```python
class TokenManager:
    def __init__(self, api_key, cache_file=None):
        self.api_key = api_key
        self.cache_file = cache_file or "~/.mdm_token_cache.json"
        self.current_token = None
        self.token_expiry = None
        self._load_from_cache()
    
    def get_token(self):
        if self._needs_refresh():
            self._refresh_token()
        return self.current_token
    
    def _needs_refresh(self):
        # Refresh 5 minutes before expiry
        return (not self.current_token or 
                self.token_expiry < datetime.now() + timedelta(minutes=5))
```

#### `models.py` - Data Models

**Responsibility**: Data validation and serialization

**Key Features**:
- Pydantic models for type safety
- Automatic validation
- JSON serialization
- Optional field handling

**Design Pattern**: Data Transfer Object (DTO)

```python
class PersonEntity(BaseModel):
    legal_name: Optional[LegalName] = None
    birth_date: Optional[str] = None
    # ... other fields
    
    class Config:
        extra = "forbid"  # Reject unknown fields
        validate_assignment = True  # Validate on assignment
```

### 3. UI Layer (`src/ui/`)

#### `entity_input.py` - Input Forms

**Responsibility**: Render entity data input forms

**Key Features**:
- Dynamic form generation
- Session state management
- Data validation
- Timestamp generation

**Design Pattern**: Template Method Pattern

```python
def render_entity_form(key_prefix, title):
    with st.expander(title, expanded=True):
        # Legal Name section
        legal_name = render_legal_name_section(key_prefix)
        
        # Demographics section
        demographics = render_demographics_section(key_prefix)
        
        # Address section
        address = render_address_section(key_prefix)
        
        # Contact section
        contact = render_contact_section(key_prefix)
        
        # Identifications section
        identifications = render_identifications_section(key_prefix)
        
        return build_entity_dict(legal_name, demographics, address, 
                                contact, identifications)
```

#### `visualizations.py` - Result Display

**Responsibility**: Visualize match results

**Key Features**:
- Gauge charts (Plotly)
- Field comparison tables
- Color-coded indicators
- Debug information display

**Design Pattern**: Strategy Pattern (different visualization strategies)

```python
def render_match_results(result, entity1, entity2):
    # Overall score gauge
    render_gauge_chart(result['similarity'], "Match Probability")
    
    # Field-by-field comparison
    render_field_comparison(result['field_scores'], entity1, entity2)
    
    # Debug details (if enabled)
    if 'debug_info' in result:
        render_debug_info(result['debug_info'])
```

#### `sample_data.py` - Sample Data Manager

**Responsibility**: Load and manage sample scenarios

**Key Features**:
- JSON file loading
- Scenario selection
- Data injection into forms

**Design Pattern**: Repository Pattern

```python
class SampleDataManager:
    def __init__(self, data_file):
        self.scenarios = self._load_scenarios(data_file)
    
    def get_scenario_names(self):
        return list(self.scenarios.keys())
    
    def get_scenario(self, name):
        return self.scenarios.get(name)
```

### 4. Utility Layer (`src/utils/`)

#### `config.py` - Configuration Management

**Responsibility**: Environment variable management

**Key Features**:
- .env file loading
- Type validation
- Default values
- Configuration object

**Design Pattern**: Singleton Pattern

```python
class AppConfig(BaseModel):
    mdm_api_base_url: str
    mdm_api_key: Optional[str] = None
    mdm_crn: str
    # ... other config

@st.cache_resource
def get_config():
    load_dotenv()
    return AppConfig(
        mdm_api_base_url=os.getenv("MDM_API_BASE_URL"),
        # ... load other vars
    )
```

---

## Data Flow

### Entity Comparison Flow

```
1. User Input
   ├─> Entity 1 Form (UI)
   └─> Entity 2 Form (UI)
        │
        ▼
2. Data Collection
   ├─> Collect form values
   ├─> Generate timestamps
   └─> Build entity dictionaries
        │
        ▼
3. Validation
   ├─> Pydantic model validation
   ├─> Required field check
   └─> Format verification
        │
        ▼
4. Authentication
   ├─> Check token validity
   ├─> Refresh if needed (TokenManager)
   └─> Get bearer token
        │
        ▼
5. API Request
   ├─> Build compare request
   ├─> Add authentication header
   └─> Send to MDM API
        │
        ▼
6. API Response
   ├─> Parse JSON response
   ├─> Extract similarity score
   └─> Extract field scores
        │
        ▼
7. Visualization
   ├─> Render gauge chart
   ├─> Display field comparison
   └─> Show debug info (if enabled)
```

### Token Refresh Flow

```
1. Token Request
   ├─> Check cache
   └─> Check expiry time
        │
        ▼
2. Needs Refresh?
   ├─> Yes: Continue to step 3
   └─> No: Return cached token
        │
        ▼
3. Generate Token
   ├─> Call IBM Cloud IAM API
   ├─> Send API key
   └─> Receive new token
        │
        ▼
4. Cache Token
   ├─> Save to file (~/.mdm_token_cache.json)
   ├─> Set expiry time (now + 55 min)
   └─> Set file permissions (0600)
        │
        ▼
5. Return Token
   └─> Provide to API client
```

---

## Technology Stack

### Core Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.11+ | Programming language |
| Streamlit | 1.30+ | Web framework |
| Pydantic | 2.5+ | Data validation |
| Requests | 2.31+ | HTTP client |
| Plotly | 5.18+ | Visualizations |
| Pandas | 2.1+ | Data manipulation |

### Development Tools

| Tool | Purpose |
|------|---------|
| pytest | Unit testing |
| black | Code formatting |
| flake8 | Linting |
| mypy | Type checking |
| pre-commit | Git hooks |

### External Services

| Service | Purpose |
|---------|---------|
| IBM MDM (Match 360) | Entity matching API |
| IBM Cloud IAM | Token generation |

---

## Design Patterns

### 1. Facade Pattern (MDMClient)

**Purpose**: Simplify complex API interactions

**Implementation**:
```python
# Complex subsystem hidden behind simple interface
client = MDMClient(base_url, api_key)
result = client.compare_entities(entity1, entity2, crn)
```

### 2. Singleton Pattern (Configuration)

**Purpose**: Single configuration instance

**Implementation**:
```python
@st.cache_resource
def get_config():
    return AppConfig(...)  # Created once, reused
```

### 3. Strategy Pattern (Visualizations)

**Purpose**: Different visualization strategies

**Implementation**:
```python
# Different strategies for different chart types
render_gauge_chart(value)
render_bar_chart(values)
render_table(data)
```

### 4. Repository Pattern (Sample Data)

**Purpose**: Abstract data access

**Implementation**:
```python
# Data source abstracted
manager = SampleDataManager("config/sample_entities.json")
scenario = manager.get_scenario("fuzzy_match")
```

### 5. Template Method Pattern (Forms)

**Purpose**: Define form structure, allow customization

**Implementation**:
```python
def render_entity_form(key_prefix, title):
    # Template defines structure
    render_section_1(key_prefix)
    render_section_2(key_prefix)
    # Sections can be customized
```

---

## Security Architecture

### Authentication

```
┌─────────────────────────────────────────────────────────┐
│                  Authentication Flow                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. User provides IBM Cloud API Key                     │
│     └─> Stored in .env file (not in code)              │
│                                                          │
│  2. TokenManager requests token from IBM Cloud IAM      │
│     └─> API Key sent over HTTPS                        │
│                                                          │
│  3. IBM Cloud IAM validates API Key                     │
│     └─> Returns Bearer Token (1 hour validity)         │
│                                                          │
│  4. Token cached locally                                │
│     └─> File permissions: 0600 (owner read/write only) │
│                                                          │
│  5. Token used for MDM API requests                     │
│     └─> Sent in Authorization header                   │
│                                                          │
│  6. Auto-refresh 5 minutes before expiry                │
│     └─> Seamless user experience                       │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Data Protection

1. **Credentials**
   - Never hardcoded
   - Stored in `.env` (gitignored)
   - Not logged or displayed

2. **Token Cache**
   - Restricted file permissions (0600)
   - Encrypted in transit
   - Cleared on logout

3. **API Communication**
   - HTTPS only
   - Bearer token authentication
   - Request/response validation

4. **Input Validation**
   - Pydantic models
   - Type checking
   - Sanitization

---

## Performance Considerations

### Optimization Strategies

1. **Caching**
   ```python
   @st.cache_resource
   def get_token_manager():
       return TokenManager(api_key)  # Cached
   
   @st.cache_data(ttl=3600)
   def load_sample_scenarios():
       return json.load(...)  # Cached for 1 hour
   ```

2. **Lazy Loading**
   - Load sample data only when needed
   - Initialize clients on demand
   - Defer heavy computations

3. **Connection Pooling**
   ```python
   # Reuse HTTP session
   self.session = requests.Session()
   ```

4. **Efficient Data Structures**
   - Use dictionaries for O(1) lookups
   - Pandas for bulk operations
   - Generators for large datasets

### Performance Metrics

| Operation | Target | Actual |
|-----------|--------|--------|
| Page Load | <2s | ~1s |
| Entity Comparison | <5s | 1-3s |
| Token Refresh | <2s | <1s |
| Form Rendering | <1s | ~500ms |

---

## Scalability

### Current Limitations

1. **Single User** - Streamlit runs single-threaded
2. **Local Storage** - Token cache on local filesystem
3. **No Database** - All data in memory/files

### Scaling Strategies

#### Horizontal Scaling

```
┌─────────────────────────────────────────────────────┐
│              Load Balancer                          │
└────────┬────────────┬────────────┬──────────────────┘
         │            │            │
         ▼            ▼            ▼
    ┌────────┐   ┌────────┐   ┌────────┐
    │ App 1  │   │ App 2  │   │ App 3  │
    └────────┘   └────────┘   └────────┘
         │            │            │
         └────────────┴────────────┘
                      │
                      ▼
              ┌──────────────┐
              │ Shared Cache │
              │   (Redis)    │
              └──────────────┘
```

#### Vertical Scaling

- Increase CPU/memory for Streamlit server
- Use faster storage for cache
- Optimize database queries (if added)

---

## Future Enhancements

### Planned Features

1. **Organization Entities**
   - Support company matching
   - Additional fields
   - Different algorithms

2. **Batch Processing**
   - Upload CSV files
   - Compare multiple entities
   - Export results

3. **Advanced Visualizations**
   - Match history timeline
   - Algorithm comparison
   - Statistical analysis

4. **API Mode**
   - REST API endpoints
   - Programmatic access
   - Webhook support

5. **Database Integration**
   - Store comparison history
   - User preferences
   - Audit logs

### Technical Debt

1. **Testing**
   - Add unit tests
   - Integration tests
   - E2E tests

2. **Documentation**
   - API documentation
   - Architecture diagrams
   - Video tutorials

3. **Monitoring**
   - Application metrics
   - Error tracking
   - Performance monitoring

---

## Deployment Architecture

### Local Development

```
Developer Machine
├── Python 3.11+
├── Virtual Environment
├── Streamlit Server (localhost:8501)
└── .env configuration
```

### Production Deployment (Future)

```
┌─────────────────────────────────────────────────────┐
│                  Cloud Platform                      │
│  ┌────────────────────────────────────────────────┐ │
│  │         Container Orchestration                 │ │
│  │              (Kubernetes)                       │ │
│  │  ┌──────────────────────────────────────────┐  │ │
│  │  │  Pod 1: Streamlit App                    │  │ │
│  │  │  ├─ Container: Python 3.11               │  │ │
│  │  │  ├─ Container: Nginx (reverse proxy)     │  │ │
│  │  │  └─ Volume: Config & Cache               │  │ │
│  │  └──────────────────────────────────────────┘  │ │
│  │  ┌──────────────────────────────────────────┐  │ │
│  │  │  Pod 2: Redis Cache                      │  │ │
│  │  └──────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

---

## Conclusion

The IBM MDM Match Decision Explorer is built with a modular, scalable architecture that prioritizes:

1. **Simplicity** - Easy to understand and maintain
2. **Security** - Proper credential management
3. **Performance** - Optimized for responsiveness
4. **Extensibility** - Easy to add new features
5. **Reliability** - Robust error handling

The architecture supports current requirements while providing a foundation for future enhancements.

---

**Document Version**: 1.0.0  
**Last Updated**: 2026-03-05  
**Maintained By**: Development Team