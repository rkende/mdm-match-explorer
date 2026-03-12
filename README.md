![Project Banner](https://github.com/user-attachments/assets/d459c0b0-2b07-4869-9c39-c3ab0ca5dfb9)
# IBM MDM Match Decision Explorer 🔍

[![Version](https://img.shields.io/badge/version-1.1.0-brightgreen.svg)](https://github.com/your-repo/mdm-match-explorer/releases/tag/v1.1.0)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.30+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An interactive Streamlit web application for exploring IBM MDM (Match 360) matching algorithms. Compare entity records in real-time, visualize match decisions, and understand field-level contributions with an intuitive interface.

> **🎉 New in v1.1.0:** Load records directly from database using Record IDs + Configurable detail levels (low/high/debug)

![MDM Match Explorer Demo](https://via.placeholder.com/800x400?text=MDM+Match+Explorer+Demo)

## 📚 Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get up and running in 5 minutes
- **[API Reference](API_REFERENCE.md)** - Complete API documentation
- **[Architecture Guide](ARCHITECTURE.md)** - Technical architecture and design
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute to the project
- **[Deployment Checklist](DEPLOYMENT_CHECKLIST.md)** - Pre-demo preparation
- **[Changelog](CHANGELOG.md)** - Version history and release notes
- **[Implementation Plan](IMPLEMENTATION_PLAN.md)** - Original technical specification

## 🌟 Features

### Core Functionality
- **🔄 Real-Time Comparison** - Compare two person entities instantly via IBM MDM API
- **📊 Visual Match Results** - Clear display of match decisions with confidence scores
- **🎯 Field-Level Analysis** - See which fields contributed to the match score
- **🔍 Load from Database** - NEW! Load entity records directly from MDM using Record IDs
- **📝 Sample Data Library** - Pre-loaded scenarios for quick testing
- **⚙️ Configurable Parameters** - Adjust query settings and thresholds

### Advanced Features
- **🔐 Automatic Token Management** - API keys with auto-refresh (no hourly token updates!)
- **💾 Token Caching** - Secure local caching for improved performance
- **🎨 Interactive UI** - Side-by-side entity forms with color-coded comparisons
- **📈 Score Visualization** - Gauge charts and detailed breakdowns
- **🔄 Live Updates** - Real-time token status monitoring
- **📊 Detail Levels** - NEW! Choose between low, high, or debug output levels
- **🔀 Mixed Comparisons** - NEW! Compare database records vs manual entries

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- IBM MDM (Match 360) instance with API access
- IBM Cloud API key or Bearer token

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd mdm-match-explorer

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials (see Configuration section)

# Run the application
streamlit run src/app.py
```

The application will open in your browser at `http://localhost:8501`

### Quick Launch Scripts

**Windows:**
```cmd
run.bat
```

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# IBM MDM API Configuration
MDM_API_BASE_URL=https://your-mdm-instance.appdomain.cloud

# Authentication (choose ONE):
# Option 1: IBM Cloud API Key (RECOMMENDED - auto-renews tokens)
MDM_API_KEY=your_ibm_cloud_api_key_here

# Option 2: Bearer Token (Legacy - expires every hour)
# MDM_API_TOKEN=your_bearer_token_here

# MDM Instance Configuration
MDM_CRN=crn:v1:bluemix:public:mdm-oc:region:a/account-id:instance-id::
MDM_ENTITY_TYPE=person_entity
MDM_RECORD_TYPE=person

# App Configuration (optional)
APP_TITLE=IBM MDM Match Decision Explorer
APP_ICON=🔍
DEBUG_MODE=false
```

### Getting Your Credentials

#### IBM Cloud API Key (Recommended)
1. Go to [IBM Cloud Console](https://cloud.ibm.com)
2. Navigate to **Manage → Access (IAM) → API keys**
3. Click **"Create an IBM Cloud API key"**
4. Name it (e.g., "MDM Match Explorer")
5. Copy the key immediately (you can't see it again!)
6. Paste into `.env` as `MDM_API_KEY`

#### Bearer Token (Alternative)
1. Use IBM Cloud CLI or API to generate a token
2. Token expires after 1 hour
3. Must be manually updated
4. Use `MDM_API_KEY` instead for automatic renewal

#### Cloud Resource Name (CRN)
1. Go to your MDM instance in IBM Cloud
2. Find the CRN in instance details
3. Format: `crn:v1:bluemix:public:mdm-oc:region:a/account:instance::`

## 📖 Usage

### Basic Workflow

1. **Choose Input Method**
   - **Option A: Manual Entry** - Enter entity data directly in the forms
   - **Option B: Load from Database** - Enter Record ID and check "🔍 Load data from Record Number"
   - **Option C: Sample Data** - Select a scenario from the sidebar dropdown

2. **Configure Parameters** (Optional)
   - Adjust CRN if needed
   - Choose detail level (low/high/debug)
   - Enter Record IDs if loading from database

3. **Compare Entities**
   - Click the "🔍 Compare Entities" button
   - View match results and score breakdown

4. **Analyze Results**
   - Review match decision and confidence
   - Examine field-by-field comparison
   - Explore debug details if enabled

### Loading Records from Database (NEW in v1.1.0)

The application now supports loading entity records directly from the MDM database:

1. **Enter Record ID**
   - In the sidebar, enter the Record ID (e.g., "12345")
   - Record IDs are unique identifiers for entities in your MDM system

2. **Enable Loading**
   - Check the "🔍 Load data from Record Number" checkbox
   - Fields will automatically populate with data from the database
   - Loaded fields become read-only to prevent accidental changes

3. **Comparison Modes**
   - **Both Manual**: Enter data in both forms (checkboxes unchecked)
   - **Both from Database**: Enter Record IDs, check both checkboxes
   - **Mixed Mode**: Load one from database, enter the other manually

4. **Edit Loaded Data**
   - Uncheck the "Load data" checkbox to edit the loaded record
   - Useful for testing "what-if" scenarios

### Detail Levels (NEW in v1.1.0)

Choose the appropriate detail level for your needs:

- **Low** (Default) - Clean UI with just match results
  - Best for: Quick comparisons, demos, production use
  - Shows: Match decision, score, field comparison

- **High** - More information without overwhelming details
  - Best for: Understanding match logic, troubleshooting
  - Shows: Everything in Low + additional match metadata

- **Debug** - Full debug information
  - Best for: Development, deep troubleshooting, API testing
  - Shows: Everything + API requests, responses, internal state

### Sample Scenarios

The application includes 4 pre-configured scenarios:

1. **Fuzzy Match - Name Typo**
   - Similar entities with typo (Bobby vs Boby)
   - Slight address difference
   - Demonstrates fuzzy matching

2. **Exact Match**
   - Identical entities
   - Perfect match score
   - Shows exact matching

3. **No Match**
   - Completely different entities
   - Low match score
   - Clear non-match decision

4. **Partial Match - Missing Fields**
   - Same person with incomplete data
   - Shows impact of missing fields
   - Demonstrates data quality importance

### Field Types Supported

**Legal Name**
- Given Name, Middle Name, Last Name
- Prefix, Suffix, Generation

**Demographics**
- Birth Date
- Gender

**Primary Residence**
- Address Line 1
- City, Province/State, Zip/Postal Code
- Country, County, Residence Number

**Contact Information**
- Home Telephone
- Mobile Telephone
- Personal Email

**Identifications**
- Social Security Number
- Driver's License
- Passport

## 🏗️ Architecture

### Project Structure

```
mdm-match-explorer/
├── src/
│   ├── app.py                      # Main Streamlit application
│   ├── mdm/
│   │   ├── client.py               # MDM API client
│   │   ├── models.py               # Data models (Pydantic)
│   │   └── auth.py                 # Token management
│   ├── ui/
│   │   ├── entity_input.py         # Entity input forms
│   │   ├── visualizations.py       # Match visualizations
│   │   └── sample_data.py          # Sample data manager
│   └── utils/
│       ├── config.py               # Configuration management
│       └── helpers.py              # Utility functions
├── config/
│   └── sample_entities.json        # Sample entity records
├── tests/                          # Test files
├── .streamlit/
│   └── config.toml                 # Streamlit configuration
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
├── README.md                       # This file
├── QUICKSTART.md                   # Quick start guide
├── IMPLEMENTATION_PLAN.md          # Technical specification
└── DEPLOYMENT_CHECKLIST.md         # Pre-demo checklist
```

### Technology Stack

- **Frontend**: Streamlit 1.30+
- **API Client**: Requests with automatic token management
- **Data Validation**: Pydantic 2.5+
- **Visualizations**: Plotly 5.18+
- **Data Processing**: Pandas 2.1+

### Key Components

1. **TokenManager** - Automatic IBM Cloud IAM token lifecycle management
2. **MDMClient** - REST API client with retry logic and error handling
3. **Entity Forms** - Dynamic Streamlit forms with validation
4. **Visualizations** - Interactive charts and comparison tables
5. **Sample Data** - JSON-based scenario management

## 🔐 Security

### Best Practices

- **API Keys**: Stored only in `.env` file (never in code)
- **Token Caching**: Secure file permissions (0600)
- **No Logging**: Credentials never logged or displayed
- **HTTPS Only**: All API communications encrypted
- **Input Validation**: All user inputs sanitized

### Token Management

- **Automatic Refresh**: Tokens renewed 5 minutes before expiry
- **Secure Storage**: Cached tokens protected with file permissions
- **Error Handling**: Graceful fallback on token refresh failures
- **Status Monitoring**: Real-time token validity display

## 🧪 Testing

### Manual Testing

```bash
# Run the application
streamlit run src/app.py

# Test scenarios:
1. Load "Fuzzy Match" scenario
2. Click Compare
3. Verify results display
4. Check token status in sidebar
```

### Unit Tests (Future)

```bash
pytest tests/
```

## 📊 Performance

- **Response Time**: 1-3 seconds per comparison
- **Token Refresh**: <1 second (cached)
- **UI Rendering**: <500ms
- **Memory Usage**: ~100MB

## 🐛 Troubleshooting

### Common Issues

**Authentication Error (401)**
- Verify API key is correct
- Check CRN format matches your instance
- Ensure API key has proper permissions

**Connection Error**
- Verify MDM API base URL
- Check network connectivity
- Ensure firewall allows HTTPS

**Invalid Request (400)**
- Check entity data format
- Verify all required fields are filled
- Leave record numbers empty for new entities

**Token Not Refreshing**
- Check API key validity
- Verify internet connection
- Clear token cache: delete `~/.mdm_token_cache.json`

### Debug Mode

Enable detailed logging in `.env`:
```bash
DEBUG_MODE=true
```

This shows:
- API request/response details
- Token refresh operations
- Error stack traces

### Getting Help

1. Check [QUICKSTART.md](QUICKSTART.md) for setup issues
2. Review [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) for configuration
3. See [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) for technical details
4. Create an issue in the repository

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Format code
black src/

# Lint code
flake8 src/

# Type checking
mypy src/
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by IBM MDM (Match 360)
- Visualizations by [Plotly](https://plotly.com/)
- Data validation by [Pydantic](https://pydantic.dev/)

## 📮 Contact

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)
- **Email**: your-email@example.com

## 🗺️ Roadmap

### Planned Features

- [ ] Support for organization entities
- [ ] Batch comparison mode
- [ ] Export results to CSV/JSON
- [ ] Custom algorithm configuration UI
- [ ] Historical comparison tracking
- [ ] Integration with watsonx.data
- [ ] Multi-language support
- [ ] Docker containerization
- [ ] Kubernetes deployment manifests

### Version History

**v1.0.0** (2026-03-05)
- Initial release
- Person entity comparison
- Automatic token management
- Sample data library
- Interactive visualizations

---

**Made with ❤️ for the IBM Data & AI Community**

**Star ⭐ this repository if you find it helpful!**
