# Deployment Checklist

Use this checklist to ensure the IBM MDM Match Decision Explorer is properly configured and ready for your demo.

## Pre-Deployment (Day 1 Morning - 2 hours)

### ✅ Environment Setup

- [ ] Python 3.11+ installed and verified (`python --version`)
- [ ] Git repository cloned or project files copied
- [ ] Navigate to `mdm-match-explorer` directory

### ✅ Virtual Environment

- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate virtual environment:
  - Linux/Mac: `source venv/bin/activate`
  - Windows: `venv\Scripts\activate`
- [ ] Verify activation (prompt should show `(venv)`)

### ✅ Dependencies

- [ ] Install requirements: `pip install -r requirements.txt`
- [ ] Verify Streamlit installed: `streamlit --version`
- [ ] Verify all packages installed without errors

### ✅ Configuration

- [ ] Copy `.env.example` to `.env`
- [ ] Obtain Bearer token from IBM Cloud/MDM instance
- [ ] Update `.env` with:
  - [ ] `MDM_API_TOKEN` - Your Bearer token
  - [ ] `MDM_API_BASE_URL` - Your MDM instance URL
  - [ ] `MDM_CRN` - Your Cloud Resource Name
- [ ] Verify CRN format matches your instance
- [ ] Save `.env` file

### ✅ Initial Test

- [ ] Run application: `streamlit run src/app.py`
- [ ] Application opens in browser at `http://localhost:8501`
- [ ] No configuration errors displayed
- [ ] UI loads successfully

## Testing (Day 1 Afternoon - 2 hours)

### ✅ Sample Data Testing

- [ ] Load "Fuzzy Match - Name Typo" scenario
- [ ] Click "Load to Entity 1" - data populates correctly
- [ ] Click "Load to Entity 2" - data populates correctly
- [ ] Verify all fields are filled appropriately

### ✅ API Connectivity

- [ ] Click "🔍 Compare Entities" button
- [ ] No authentication errors
- [ ] API request completes successfully
- [ ] Match result displays
- [ ] Score gauge renders
- [ ] Field comparison table shows

### ✅ All Scenarios

Test each sample scenario:
- [ ] Fuzzy Match - Name Typo
- [ ] Exact Match
- [ ] No Match
- [ ] Partial Match - Missing Fields

For each scenario:
- [ ] Loads correctly
- [ ] Comparison completes
- [ ] Results make sense
- [ ] Debug details available (if enabled)

### ✅ Manual Data Entry

- [ ] Clear all data
- [ ] Manually enter entity 1 data
- [ ] Manually enter entity 2 data
- [ ] Comparison works with manual data
- [ ] Validation catches missing required fields

### ✅ Configuration Options

- [ ] Change record numbers - still works
- [ ] Toggle details level (debug/standard)
- [ ] Verify debug details show when enabled
- [ ] Verify standard mode works

## Polish (Day 2 Morning - 2 hours)

### ✅ UI/UX Review

- [ ] All text is readable
- [ ] Colors and styling look professional
- [ ] No layout issues or overlapping elements
- [ ] Responsive on different screen sizes
- [ ] Icons and emojis display correctly

### ✅ Error Handling

- [ ] Test with invalid token - shows clear error
- [ ] Test with missing CRN - shows clear error
- [ ] Test with empty required fields - validation works
- [ ] Test with network disconnected - graceful error

### ✅ Performance

- [ ] Application loads quickly (< 3 seconds)
- [ ] Comparisons complete in reasonable time (< 5 seconds)
- [ ] No lag when switching between scenarios
- [ ] Memory usage is reasonable

### ✅ Documentation

- [ ] README.md is clear and complete
- [ ] QUICKSTART.md has accurate instructions
- [ ] Sample data descriptions are helpful
- [ ] Error messages are user-friendly

## Demo Preparation (Day 2 Afternoon - 2 hours)

### ✅ Demo Script

- [ ] Review IMPLEMENTATION_PLAN.md demo script
- [ ] Practice the 25-minute demo flow
- [ ] Prepare talking points for each section
- [ ] Have backup scenarios ready

### ✅ Demo Environment

- [ ] Clean browser cache
- [ ] Close unnecessary browser tabs
- [ ] Increase browser zoom if presenting (125-150%)
- [ ] Test screen sharing/projection
- [ ] Have backup internet connection ready

### ✅ Backup Plan

- [ ] Screenshots of successful comparisons
- [ ] Video recording of working demo (optional)
- [ ] Printed handouts with key points
- [ ] Alternative demo data ready

### ✅ Presentation Materials

- [ ] Introduction slides (optional)
- [ ] Architecture diagram ready to show
- [ ] Business value talking points prepared
- [ ] Q&A responses prepared

## Day of Demo

### ✅ Pre-Demo (30 minutes before)

- [ ] Start application: `streamlit run src/app.py`
- [ ] Load and test one scenario end-to-end
- [ ] Verify API connectivity
- [ ] Check all UI elements render correctly
- [ ] Close unnecessary applications
- [ ] Silence notifications

### ✅ During Demo

- [ ] Start with introduction (2 min)
- [ ] Show basic match (5 min)
- [ ] Demonstrate field analysis (5 min)
- [ ] Live data modification (5 min)
- [ ] Debug mode exploration (3 min)
- [ ] Audience participation (3 min)
- [ ] Q&A (2 min)

### ✅ Post-Demo

- [ ] Share repository/code access
- [ ] Provide setup instructions
- [ ] Share contact information
- [ ] Collect feedback
- [ ] Note improvement ideas

## Troubleshooting Quick Reference

### Issue: Authentication Error
**Solution:** Verify Bearer token is valid, check CRN format

### Issue: Connection Timeout
**Solution:** Check network, verify MDM API URL, test with curl

### Issue: Module Not Found
**Solution:** Activate venv, reinstall requirements

### Issue: Port Already in Use
**Solution:** Stop other Streamlit apps, use different port

### Issue: Slow Performance
**Solution:** Check network speed, reduce debug output, restart app

## Success Criteria

- ✅ Application runs without errors
- ✅ All sample scenarios work correctly
- ✅ API integration functions properly
- ✅ UI is professional and responsive
- ✅ Demo flows smoothly
- ✅ Audience is engaged and impressed

## Notes

Use this space for environment-specific notes:

```
MDM Instance: _______________________
Token Expiry: _______________________
Demo Date: __________________________
Audience: ___________________________
Special Requirements: _______________
```

---

**Ready for an impressive demo!** 🚀