
# 🚀 Quick Start Guide - IBM MDM Match Decision Explorer

Get up and running in **5 minutes**! This guide walks you through the fastest path to exploring IBM MDM matching algorithms.

## ⚡ Prerequisites Checklist

Before you begin, ensure you have:

- [ ] Python 3.11 or higher installed
- [ ] Access to an IBM MDM (Match 360) instance
- [ ] IBM Cloud API key OR Bearer token
- [ ] Your MDM instance CRN (Cloud Resource Name)

## 📋 Step-by-Step Setup

### Step 1: Get Your Credentials (5 minutes)

#### Option A: IBM Cloud API Key (Recommended ⭐)

1. **Login to IBM Cloud**
   - Go to https://cloud.ibm.com
   - Sign in with your IBM ID

2. **Create API Key**
   - Click your profile icon (top right)
   - Select **"Manage → Access (IAM)"**
   - Click **"API keys"** in the left menu
   - Click **"Create an IBM Cloud API key"**
   - Name it: `MDM Match Explorer`
   - Click **"Create"**
   - **IMPORTANT**: Copy the key immediately (you can't see it again!)

3. **Save Your API Key**
   - Store it securely (password manager recommended)
   - You'll paste it into `.env` in Step 3

#### Option B: Bearer Token (Alternative)

```bash
# Generate token using IBM Cloud CLI
ibmcloud iam oauth-tokens

# Or use curl
curl -X POST "https://iam.cloud.ibm.com/identity/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=YOUR_API_KEY"
```

**Note**: Bearer tokens expire after 1 hour. Use API key for automatic renewal!

#### Get Your MDM CRN

1. Go to your MDM instance in IBM Cloud
2. Click on the instance name
3. Find **"CRN"** in the instance details
4. Copy the entire CRN (starts with `crn:v1:bluemix:public:mdm-oc:`)

Example CRN format:
```
crn:v1:bluemix:public:mdm-oc:us-south:a/1234567890abcdef:instance-id-here::
```

### Step 2: Install the Application (2 minutes)

#### Windows

```cmd
# Open Command Prompt or PowerShell

# Clone or download the project
cd path\to\mdm-match-explorer

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Linux/Mac

```bash
# Open Terminal

# Clone or download the project
cd path/to/mdm-match-explorer

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure Environment (1 minute)

1. **Copy the template**
   ```bash
   # Windows
   copy .env.example .env
   
   # Linux/Mac
   cp .env.example .env
   ```

2. **Edit `.env` file**
   
   Open `.env` in your favorite text editor and fill in:

   ```bash
   # Your MDM API endpoint
   MDM_API_BASE_URL=https://your-mdm-instance.appdomain.cloud
   
   # OPTION 1: Use API Key (Recommended - auto-renews!)
   MDM_API_KEY=paste_your_api_key_here
   
   # OPTION 2: Use Bearer Token (expires hourly)
   # MDM_API_TOKEN=paste_your_bearer_token_here
   
   # Your MDM instance CRN
   MDM_CRN=crn:v1:bluemix:public:mdm-oc:region:a/account:instance::
   
   # Entity configuration (usually don't need to change)
   MDM_ENTITY_TYPE=person_entity
   MDM_RECORD_TYPE=person
   ```

3. **Save the file**

### Step 4: Launch the Application (30 seconds)

#### Quick Launch

**Windows:**
```cmd
run.bat
```

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

#### Manual Launch

```bash
# Make sure virtual environment is activated
streamlit run src/app.py
```

The application will automatically open in your browser at `http://localhost:8501`

### Step 5: Try Your First Comparison (1 minute)

1. **Load Sample Data**
   - In the sidebar, find **"Sample Data"**
   - Select **"Fuzzy Match - Name Typo"** from dropdown
   - Click **"Load to Entity 1"**
   - Click **"Load to Entity 2"**

2. **Compare**
   - Scroll down to the **"🔍 Compare Entities"** button
   - Click it!

3. **View Results**
   - See the match decision and confidence score
   - Explore field-by-field comparison
   - Check the debug details (if enabled)

🎉 **Congratulations!** You've successfully run your first MDM match comparison!

## 🎯 What's Next?

### Try Different Scenarios

The app includes 4 pre-configured scenarios:

1. **Fuzzy Match** - Similar entities with typos
2. **Exact Match** - Identical entities
3. **No Match** - Completely different entities
4. **Partial Match** - Same person with missing data

### Create Your Own Comparisons

1. Clear the forms (refresh page)
2. Manually enter entity data in both forms
3. Click **"Compare Entities"**
4. Analyze the results

### Explore Advanced Features

- **Debug Mode**: Enable in sidebar for detailed API responses
- **Token Status**: Monitor token validity in sidebar
- **Field Analysis**: See which fields contributed to match score
- **Score Breakdown**: Understand confidence levels

## 🔧 Troubleshooting

### "Authentication failed" Error

**Problem**: 401 Unauthorized error

**Solutions**:
1. Verify you're using the correct variable name:
   - `MDM_API_KEY` for API keys (not `MDM_API_TOKEN`)
   - `MDM_API_TOKEN` for bearer tokens
2. Check your API key is valid and not expired
3. Ensure CRN matches your MDM instance
4. Restart the application after changing `.env`

### "Connection refused" Error

**Problem**: Can't connect to MDM API

**Solutions**:
1. Verify `MDM_API_BASE_URL` is correct
2. Check your network connection
3. Ensure you're not behind a firewall blocking HTTPS
4. Try accessing the URL in a browser

### "Invalid request" Error (400)

**Problem**: API rejects the comparison request

**Solutions**:
1. Leave **Record Number** fields empty for new entities
2. Ensure all required fields are filled
3. Check date formats are correct
4. Verify entity data structure matches API expectations

### Token Not Showing in Sidebar

**Problem**: No token status displayed

**Solutions**:
1. Make sure you're using `MDM_API_KEY` (not `MDM_API_TOKEN`)
2. Check API key is valid
3. Restart the application
4. Look for error messages in the terminal

### Application Won't Start

**Problem**: Errors when running `streamlit run src/app.py`

**Solutions**:
1. Verify Python version: `python --version` (need 3.11+)
2. Check virtual environment is activated
3. Reinstall dependencies: `pip install -r requirements.txt`
4. Check for syntax errors in `.env` file

## 💡 Pro Tips

### Faster Development

