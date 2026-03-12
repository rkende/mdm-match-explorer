# Changelog

All notable changes to the IBM MDM Match Decision Explorer will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-03-12

### 🎉 Major Feature Release - Record Loading & Detail Levels

This release introduces the ability to load entity records directly from the MDM database and adds configurable detail levels for cleaner UI.

### ✨ New Features

#### Record Loading from Database
- **🔍 Load from Record ID** - New checkbox option to load entity data directly from MDM using Record IDs
- **📥 Automatic Data Population** - Fields automatically populate when loading from database
- **🔒 Field Locking** - Loaded fields become read-only to prevent accidental modifications
- **🔄 Mixed Comparison Modes** - Support for comparing:
  - Two manually entered entities
  - Two database-loaded entities
  - One database entity vs one manual entity
- **💾 Smart Caching** - Loaded records are cached to prevent redundant API calls
- **✅ Checkbox State Persistence** - Load state persists across UI interactions

#### Detail Level Control
- **📊 Three Detail Levels**:
  - **Low** (default) - Minimal output, clean UI with just results
  - **High** - More information without overwhelming details
  - **Debug** - Full debug information including API requests and responses
- **🎯 Selective Debug Output** - Debug messages only appear in debug mode
- **🧹 Cleaner Default Experience** - App starts in "low" detail mode for better UX

### 🔧 Improvements

#### API Integration
- **🔄 Smart Parameter Handling** - Conditional use of `record_number` parameters based on comparison mode
- **🛡️ API Behavior Workaround** - Handles MDM API's behavior of ignoring request body when record_numbers are present
- **📝 Request Body Fallback** - Uses request body for mixed scenarios (one DB, one manual)

#### User Experience
- **🎨 Improved Form Layout** - Checkbox for record loading integrated into entity forms
- **💡 Better Visual Feedback** - Clear indication when fields are loaded vs manual
- **📋 Informative Messages** - Debug mode shows which data source is being used

#### Code Quality
- **🔄 Gender Value Mapping** - Bidirectional mapping between API codes (M/F) and display values (Male/Female)
- **📅 Date Format Handling** - Proper birth date format without unnecessary timestamps
- **🔍 Enhanced Validation** - Better error handling for record loading failures
- **🧪 Session State Management** - Improved Streamlit state handling to prevent conflicts

### 🐛 Bug Fixes

- **Fixed**: Invalid "standard" detail level causing 400 API errors
- **Fixed**: Record data not appearing in UI after loading
- **Fixed**: Checkbox state not persisting after data load
- **Fixed**: Compare button not working after record load (removed interfering `st.rerun()`)
- **Fixed**: Gender value mismatch between UI and API
- **Fixed**: Birth date format including unnecessary timestamp
- **Fixed**: API ignoring request body in mixed comparison scenarios
- **Fixed**: Missing `record_last_updated` field causing validation errors

### 📚 Documentation

- **Updated**: README.md with new record loading feature
- **Updated**: CHANGELOG.md with detailed release notes
- **Added**: Technical notes about API behavior and workarounds
- **Enhanced**: Code comments explaining complex logic

### 🔄 API Changes

#### New Methods
- `MDMClient.get_record_by_id(record_id, crn)` - Fetch record from MDM database
- `convert_mdm_record_to_entity(record_data)` - Convert API response to app format
- `load_entity_to_session_state(entity, key_prefix)` - Populate UI widgets with loaded data

#### Modified Behavior
- `compare_entities()` now conditionally uses `record_number` parameters
- Request body always includes both entities for mixed scenarios

### 🏗️ Technical Details

#### Architecture Changes
- Enhanced `src/mdm/client.py` with record loading capability
- Updated `src/app.py` with pre-load logic and conditional parameter passing
- Modified `src/ui/entity_input.py` with checkbox and field disabling logic
- Improved `src/ui/visualizations.py` with valid detail level options

#### State Management
- Added caching mechanism for loaded records (`loaded_record1_{id}`, `loaded_record2_{id}`)
- Checkbox state tracking (`entity1_use_record_number_checkbox`, `entity2_use_record_number_checkbox`)
- Entity data storage (`entity1_data`, `entity2_data`)

### ⚠️ Breaking Changes

None - This release is fully backwards compatible with v1.0.0

### 📊 Performance

- Record loading: <1 second (with caching)
- No performance impact on manual entry mode
- Reduced API calls through smart caching

### 🔒 Security

- No security changes
- Maintains same authentication and credential handling

### 📝 Migration Guide

No migration needed - existing configurations and workflows continue to work unchanged.

### 🎯 Usage Examples

#### Loading from Database
1. Enter a Record ID in the sidebar field
2. Check "🔍 Load data from Record Number"
3. Fields automatically populate and become read-only
4. Uncheck to edit the loaded data

#### Comparison Modes
- **Both Manual**: Enter data in both forms, leave checkboxes unchecked
- **Both from DB**: Enter Record IDs, check both checkboxes
- **Mixed**: Check one checkbox for DB record, leave other unchecked for manual entry

---

## [1.0.0] - 2026-03-05

### 🎉 Initial Release

The first production-ready release of IBM MDM Match Decision Explorer!

### ✨ Features

#### Core Functionality
- **Real-time Entity Comparison** - Compare two person entities via IBM MDM API
- **Interactive UI** - Side-by-side entity input forms with Streamlit
- **Match Visualization** - Gauge charts showing match probability and confidence
- **Field-Level Analysis** - Color-coded comparison of individual fields
- **Sample Data Library** - 4 pre-configured test scenarios
- **Debug Mode** - Detailed API response inspection

#### Authentication & Security
- **Automatic Token Management** - IBM Cloud API key integration with auto-refresh
- **Token Caching** - Secure local storage with proper file permissions
- **Dual Auth Support** - Both API key and bearer token authentication
- **Token Status Monitoring** - Real-time validity display in sidebar

#### User Experience
- **Quick Launch Scripts** - `run.bat` (Windows) and `run.sh` (Linux/Mac)
- **Configuration Management** - Environment-based settings with `.env` file
- **Error Handling** - Clear error messages and troubleshooting guidance
- **Loading Indicators** - Visual feedback during API calls
- **Responsive Design** - Works on various screen sizes

### 📚 Documentation

- **README.md** - Comprehensive project documentation
- **QUICKSTART.md** - 5-minute setup guide
- **CONTRIBUTING.md** - Developer contribution guidelines
- **DEPLOYMENT_CHECKLIST.md** - Pre-demo preparation checklist
- **IMPLEMENTATION_PLAN.md** - Technical architecture documentation
- **LICENSE** - MIT License
- **CHANGELOG.md** - This file

### 🏗️ Technical Implementation

#### Architecture
- **Modular Design** - Separated concerns (UI, API, Auth, Utils)
- **Pydantic Models** - Type-safe data validation
- **Session State Management** - Proper Streamlit state handling
- **Error Recovery** - Graceful degradation on failures

#### API Integration
- **MDM REST API** - Full integration with Match 360 API
- **Request Optimization** - Efficient payload construction
- **Response Parsing** - Robust handling of API responses
- **Retry Logic** - Automatic retry on transient failures

#### Code Quality
- **Type Hints** - Full type annotation coverage
- **Docstrings** - Google-style documentation
- **Code Organization** - Clear module structure
- **Configuration** - Environment-based settings

### 🔧 Configuration

#### Supported Environment Variables
- `MDM_API_BASE_URL` - MDM instance endpoint
- `MDM_API_KEY` - IBM Cloud API key (recommended)
- `MDM_API_TOKEN` - Bearer token (alternative)
- `MDM_CRN` - Cloud Resource Name
- `MDM_ENTITY_TYPE` - Entity type (default: person_entity)
- `MDM_RECORD_TYPE` - Record type (default: person)
- `APP_TITLE` - Application title
- `APP_ICON` - Application icon
- `DEBUG_MODE` - Enable debug output

### 📦 Dependencies

#### Production
- streamlit >= 1.30.0
- requests >= 2.31.0
- pydantic >= 2.5.0
- plotly >= 5.18.0
- pandas >= 2.1.0
- python-dotenv >= 1.0.0

#### Development
- pytest >= 7.4.0
- black >= 23.7.0
- flake8 >= 6.1.0
- mypy >= 1.5.0

### 🐛 Known Issues

None at this time.

### 🔒 Security

- Credentials stored only in `.env` file
- Token cache with restricted permissions
- No credential logging
- HTTPS-only API communication
- Input validation and sanitization

### 📊 Performance

- Response time: 1-3 seconds per comparison
- Token refresh: <1 second (cached)
- UI rendering: <500ms
- Memory usage: ~100MB

### 🎯 Sample Scenarios

1. **Fuzzy Match - Name Typo**
   - Tests fuzzy matching with typos
   - Bobby vs Boby with slight address difference

2. **Exact Match**
   - Tests exact matching
   - Identical entities

3. **No Match**
   - Tests clear non-matches
   - Completely different entities

4. **Partial Match - Missing Fields**
   - Tests impact of missing data
   - Same person with incomplete information

### 🚀 Getting Started

```bash
# Quick start
git clone <repository-url>
cd mdm-match-explorer
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
streamlit run src/app.py
```

### 📝 Notes

- Requires Python 3.11 or higher
- Tested on Windows 11, macOS, and Linux
- Compatible with IBM MDM (Match 360) v2.0+
- Token auto-refresh requires IBM Cloud API key

---

## [Unreleased]

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
- [ ] REST API endpoint for programmatic access

### Under Consideration

- [ ] Real-time collaboration features
- [ ] Comparison result analytics dashboard
- [ ] Machine learning insights
- [ ] Integration with other IBM products
- [ ] Mobile-responsive improvements
- [ ] Accessibility enhancements (WCAG 2.1)
- [ ] Performance optimizations
- [ ] Advanced filtering and search
- [ ] Custom field mapping
- [ ] Webhook notifications

---

## Version History

### Version Numbering

We use [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality (backwards compatible)
- **PATCH** version for backwards compatible bug fixes

### Release Schedule

- **Major releases**: Quarterly
- **Minor releases**: Monthly
- **Patch releases**: As needed

### Support Policy

- **Current version**: Full support
- **Previous minor**: Security fixes only
- **Older versions**: No support

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Reporting bugs
- Suggesting features
- Submitting pull requests
- Development workflow
- Code standards

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by IBM MDM (Match 360)
- Visualizations by [Plotly](https://plotly.com/)
- Data validation by [Pydantic](https://pydantic.dev/)

---

**Questions?** Open an issue or discussion in the repository.

**Found a bug?** Please report it with details in the issue tracker.

**Want to contribute?** We welcome contributions! See CONTRIBUTING.md.