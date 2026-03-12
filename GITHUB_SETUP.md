# GitHub Repository Setup Guide

Follow these steps to create and push your project to GitHub.

## Step 1: Create Repository on GitHub

1. **Go to GitHub**
   - Open your browser and go to: https://github.com/rkende
   - Click the **"+"** icon in the top right corner
   - Select **"New repository"**

2. **Configure Repository**
   - **Repository name**: `mdm-match-explorer`
   - **Description**: `Interactive Streamlit app for exploring IBM MDM (Match 360) matching algorithms`
   - **Visibility**: Choose **Public** (recommended for community sharing) or **Private**
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
   - Click **"Create repository"**

## Step 2: Push Your Code

After creating the repository, GitHub will show you commands. Use these:

### Option A: Using HTTPS (Recommended for Windows)

```powershell
# Navigate to your project
cd C:\Users\ROBERTKENDE\OneDrive - IBM\DOCS\WORKSPACES\bob\mdm-match-explorer

# Add the remote repository
git remote add origin https://github.com/rkende/mdm-match-explorer.git

# Rename branch to main (if needed)
git branch -M main

# Push your code
git push -u origin main
```

### Option B: Using SSH (If you have SSH keys configured)

```powershell
# Navigate to your project
cd C:\Users\ROBERTKENDE\OneDrive - IBM\DOCS\WORKSPACES\bob\mdm-match-explorer

# Add the remote repository
git remote add origin git@github.com:rkende/mdm-match-explorer.git

# Rename branch to main (if needed)
git branch -M main

# Push your code
git push -u origin main
```

## Step 3: Verify Upload

1. Go to: https://github.com/rkende/mdm-match-explorer
2. You should see all your files
3. The README.md will be displayed automatically

## Step 4: Configure Repository Settings (Optional but Recommended)

### Add Topics

1. Go to your repository
2. Click the gear icon next to "About"
3. Add topics:
   - `ibm-mdm`
   - `match360`
   - `streamlit`
   - `data-quality`
   - `entity-matching`
   - `python`
   - `data-governance`

### Enable Features

1. Go to **Settings** tab
2. Under **Features**, enable:
   - ✅ Issues
   - ✅ Discussions (great for Q&A)
   - ✅ Projects (optional)
   - ✅ Wiki (optional)

### Add Repository Description

1. Click the gear icon next to "About"
2. Add description: `Interactive Streamlit app for exploring IBM MDM (Match 360) matching algorithms`
3. Add website (if you deploy it): `https://your-deployment-url.com`
4. Click "Save changes"

## Step 5: Create a Release (Optional)

1. Go to **Releases** (right sidebar)
2. Click **"Create a new release"**
3. **Tag version**: `v1.0.0`
4. **Release title**: `v1.0.0 - Initial Release`
5. **Description**: Copy from CHANGELOG.md
6. Click **"Publish release"**

## Troubleshooting

### Authentication Issues

If you get authentication errors when pushing:

**For HTTPS:**
1. GitHub may prompt for credentials
2. Use your GitHub username
3. For password, use a **Personal Access Token** (not your GitHub password)
4. Create token at: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select scopes: `repo` (full control)
   - Copy the token and use it as password

**For SSH:**
1. You need to set up SSH keys
2. Follow: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

### Branch Name Issues

If your default branch is `master` instead of `main`:

```powershell
git branch -M main
```

### Remote Already Exists

If you get "remote origin already exists":

```powershell
git remote remove origin
git remote add origin https://github.com/rkende/mdm-match-explorer.git
```

## Next Steps After Upload

1. **Update README badges** (optional)
   - Update repository URL in badges
   - Add build status badges if you set up CI/CD

2. **Share your project**
   - LinkedIn post
   - Twitter/X
   - IBM internal channels
   - Streamlit community forum

3. **Enable GitHub Pages** (optional)
   - Host documentation
   - Create project website

## Quick Commands Reference

```powershell
# Check git status
git status

# View remote URL
git remote -v

# View commit history
git log --oneline

# Create a new branch
git checkout -b feature/new-feature

# Push changes
git add .
git commit -m "Your commit message"
git push
```

## Need Help?

- **Git Documentation**: https://git-scm.com/doc
- **GitHub Docs**: https://docs.github.com
- **GitHub Support**: https://support.github.com

---

**Ready to push?** Run the commands from Step 2 above!