# 🎉 Version 1.1.0 - Record Loading & Detail Levels

## What's New

### 🔍 Load Records from Database
Load entity records directly from your MDM database using Record IDs - no more manual data entry for existing records!

**Features:**
- ✅ One-click data loading from database
- ✅ Automatic field population
- ✅ Read-only mode for loaded fields
- ✅ Smart caching for performance
- ✅ Support for mixed comparisons (DB + manual)

### 📊 Configurable Detail Levels
Choose your preferred level of information:
- **Low** (default) - Clean UI, just the essentials
- **High** - More context and metadata
- **Debug** - Full API details for troubleshooting

## Key Improvements

- 🔄 Smart API parameter handling for mixed comparison modes
- 🎨 Cleaner default UI experience
- 💡 Better visual feedback for loaded vs manual data
- 🔍 Enhanced validation and error handling
- 📝 Improved documentation with usage examples

## Bug Fixes

- Fixed invalid detail level causing API errors
- Fixed checkbox state persistence issues
- Fixed gender value mapping between UI and API
- Fixed date format handling
- Fixed API request body handling in mixed scenarios

## Upgrade Instructions

```bash
git pull origin main
pip install -r requirements.txt --upgrade
streamlit run src/app.py
```

**Fully backwards compatible** - no configuration changes needed!

## Documentation

- 📚 [Full Release Notes](RELEASE_NOTES_v1.1.0.md)
- 📝 [Changelog](CHANGELOG.md)
- 📖 [README](README.md)

## What's Next

Looking ahead to v1.2.0:
- Support for organization entities
- Batch comparison mode
- Export results to CSV/JSON
- Custom algorithm configuration UI

---

**Full Changelog**: v1.0.0...v1.1.0