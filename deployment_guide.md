# Deployment Guide for Stock Price Predictor

This guide covers deployment to **Render** (Recommended) and **Streamlit Cloud**.

## 🚀 Quick Start: Deploy to Render

We have added a `render.yaml` file to automate the deployment.

### Option A: Use the "Blueprint" (Easiest)
1.  **Push to GitHub**:
    - If you haven't already, push this project to a GitHub repository (see [GitHub Guide](#github-guide) below).
2.  **Create Service on Render**:
    - Go to [dashboard.render.com](https://dashboard.render.com/).
    - Click **New +** -> **Blueprint**.
    - Connect your GitHub repository.
    - Click **Apply**.
    - Render will automatically read `render.yaml` and deploy your app.

### Option B: Manual Setup (If Option A fails)
1.  **Create Web Service**:
    - Go to [dashboard.render.com](https://dashboard.render.com/).
    - Click **New +** -> **Web Service**.
    - Connect your GitHub repository.
2.  **Configure**:
    - **Name**: `stock-predictor`
    - **Runtime**: `Python 3`
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
3.  **Deploy**: Click **Create Web Service**.

---

## <a id="github-guide"></a>🐙 GitHub Guide: How to Push Your Code

If you don't have a repository yet, follow these steps or use the provided `push_to_github.bat` script.

### 1. Create a Repository
- Go to [github.com/new](https://github.com/new).
- Name it (e.g., `stock-price-predictor`).
- **Do NOT** check "Initialize with README" or .gitignore (you already have them).
- Be sure to select **Public** (unless you have a paid Render account).

### 2. Push Code (Using Terminal)
Open your terminal in this directory (`d:\personal\project\pro1\stock_price_prediction`) and run:

```bash
# Initialize Git (if not done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit"

# Link to GitHub (Replace URL with YOUR repo URL from Step 1)
git remote add origin https://github.com/YOUR_USERNAME/stock-price-predictor.git

# Push
git push -u origin main
```

### 3. Automatic Script
We created a script `push_to_github.bat` in this folder.
1. Create the repo on GitHub first.
2. Run `push_to_github.bat`.
3. Paste your repository URL when asked.

---

## ⚠️ Troubleshooting
- **Memory Limits**: The free tier on Render has 512MB RAM. Since this app uses `tensorflow`, it might be heavy. If deployment fails (OOM error), you may need to:
    - Upgrade to a paid Render plan.
    - Or switching to a lighter model (e.g., TFLite or Scikit-learn).
- **Build Times**: First build can take 5-10 minutes.
