# Release Notes - Version 1.1.0

**Release Date:** March 12, 2026

## 🎉 What's New

Version 1.1.0 introduces two major features that significantly enhance the usability and flexibility of the IBM MDM Match Decision Explorer:

### 1. 🔍 Load Records from Database

You can now load entity records directly from your MDM database using Record IDs, eliminating the need to manually enter data for existing records.

**Key Features:**
- ✅ Load entity data with a single click
- ✅ Automatic field population from database
- ✅ Read-only mode for loaded fields (prevents accidental edits)
- ✅ Smart caching to avoid redundant API calls
- ✅ Support for mixed comparisons (DB record vs manual entry)

**How to Use:**
1. Enter a Record ID in the sidebar (e.g., "12345")
2. Check "🔍 Load data from Record Number"
3. Fields automatically populate and become read-only
4. Uncheck to edit the loaded data if needed

**Comparison Modes:**
- **Both Manual**: Enter data in both forms
- **Both from DB**: Load both entities using Record IDs
- **Mixed**: Load one from DB, enter the other manually

### 2. 📊 Configurable Detail Levels

Choose how much information you want to see with three detail levels:

**Low (Default)** - Clean, minimal UI
- Perfect for demos and production use
- Shows only essential match results
- No debug clutter

**High** - More context
- Additional match metadata
- Better for understanding match logic
- Still clean and professional

**Debug** - Full transparency
- Complete API request/response details
- Internal state information
- Ideal for development and troubleshooting

## 🔧 Improvements

### API Integration
- **Smart Parameter Handling**: Automatically determines when to use `record_number` parameters vs request body
- **Mixed Mode Support**: Properly handles comparisons between database records and manual entries
- **API Workaround**: Implements solution for MDM API's behavior of ignoring request body when record_numbers are present

### User Experience
- **Cleaner Default UI**: App starts in "low" detail mode for better first impression
- **Better Visual Feedback**: Clear indication of loaded vs manual data
- **Persistent State**: Checkbox states persist across UI interactions
- **Improved Error Messages**: More helpful error messages for common issues

### Code Quality
- **Enhanced Validation**: Better error handling for record loading failures
- **Gender Mapping**: Bidirectional mapping between API codes (M/F) and display values (Male/Female)
- **Date Handling**: Proper birth date format without unnecessary timestamps
- **Session State**: Improved Streamlit state management to prevent conflicts

## 🐛 Bug Fixes

- Fixed invalid "standard" detail level causing 400 API errors
- Fixed record data not appearing in UI after loading
- Fixed checkbox state not persisting after data load
- Fixed compare button not working after record load
- Fixed gender value mismatch between UI and API
- Fixed birth date format including unnecessary timestamp
- Fixed API ignoring request body in mixed comparison scenarios
- Fixed missing `record_last_updated` field causing validation errors

## 📚 Documentation Updates

- Updated README with new features and usage examples
- Added comprehensive CHANGELOG entry for v1.1.0
- Enhanced code comments explaining complex logic
- Added technical notes about API behavior and workarounds

## 🔄 Migration Guide

**Good News:** This release is fully backwards compatible with v1.0.0!

No changes are required to your existing configuration or workflows. All new features are opt-in:
- Record loading is disabled by default (checkbox unchecked)
- Detail level defaults to "low" for clean UI
- Manual entry mode works exactly as before

## 📊 Performance

- Record loading: <1 second (with caching)
- No performance impact on manual entry mode
- Reduced API calls through smart caching
- Same fast comparison times as v1.0.0

## 🔒 Security

No security changes in this release. The application maintains the same security posture as v1.0.0:
- Credentials stored only in `.env` file
- Token cache with restricted permissions
- No credential logging
- HTTPS-only API communication

## 🎯 Use Cases

### Use Case 1: Quick Database Record Comparison
**Scenario:** Compare two existing customer records
1. Enter Record ID 1: "12345"
2. Enter Record ID 2: "67890"
3. Check both "Load data" checkboxes
4. Click Compare
5. View results in clean "low" detail mode

### Use Case 2: Test "What-If" Scenarios
**Scenario:** See how a record would match if data was different
1. Load a record from database (Record ID: "12345")
2. Uncheck "Load data" to enable editing
3. Modify specific fields (e.g., change address)
4. Compare against another record
5. Analyze impact of changes

### Use Case 3: Validate Manual Entry
**Scenario:** Check if manually entered data matches existing record
1. Load existing record in Entity 1 (Record ID: "12345")
2. Manually enter data in Entity 2
3. Compare to see if they match
4. Use "high" detail level for more context

### Use Case 4: Deep Troubleshooting
**Scenario:** Investigate why two records aren't matching
1. Load both records from database
2. Switch to "debug" detail level
3. Compare entities
4. Review full API request/response
5. Analyze field-by-field contributions

## 🚀 Upgrade Instructions

### From v1.0.0 to v1.1.0

```bash
# Pull latest changes
git pull origin main

# No dependency changes, but you can update to be safe
pip install -r requirements.txt --upgrade

# Restart the application
streamlit run src/app.py
```

That's it! No configuration changes needed.

## 🙏 Acknowledgments

Special thanks to all users who provided feedback and feature requests that made this release possible.

## 📞 Support

- **Issues**: Report bugs via GitHub Issues
- **Questions**: Open a GitHub Discussion
- **Documentation**: See README.md and other docs in the repository

## 🔮 What's Next

Looking ahead to v1.2.0:
- Support for organization entities
- Batch comparison mode
- Export results to CSV/JSON
- Custom algorithm configuration UI

Stay tuned!

---

**Full Changelog**: [CHANGELOG.md](CHANGELOG.md)

**Download**: [GitHub Releases](https://github.com/your-repo/mdm-match-explorer/releases/tag/v1.1.0)