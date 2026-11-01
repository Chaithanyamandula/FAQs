# College FAQ Classifier - Deployment Guide
## Architecture: Netlify (Frontend) + Render (Backend)

This guide walks you through deploying the project in less than 5 minutes:
- **Backend (Render.com)**: Python Flask API running fine-tuned DistilBERT with CORS enabled.
- **Frontend (Netlify)**: High-speed static hosting with the Render-inspired minimal dark UI.

---

## Part 1: Push Project to GitHub

1. Initialize a git repository in your project folder (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Deploy College FAQ Classifier"
   ```
   *(Note: The included `.gitignore` automatically excludes `venv/` and `model/` so you won't hit GitHub's 100MB file limit. Render will automatically build the model during deployment).*

2. Create a new repository on [GitHub](https://github.com/new) (e.g. `college-faq-classifier`).

3. Link and push your code:
   ```bash
   git remote add origin https://github.com/<your-username>/college-faq-classifier.git
   git branch -M main
   git push -u origin main
   ```

---

## Part 2: Deploy Backend to Render.com

1. Go to [Render Dashboard](https://dashboard.render.com/) and click **New +** -> **Web Service**.
2. Connect your GitHub account and select your `college-faq-classifier` repository.
3. Configure the settings:
   - **Name**: `college-faq-bert-api` (or any name you like)
   - **Language**: `Python 3`
   - **Region**: Choose the closest region (e.g., Singapore, Oregon, Frankfurt)
   - **Branch**: `main`
   - **Build Command**:
     ```bash
     pip install -r requirements.txt && python train.py
     ```
     *(This installs dependencies and trains DistilBERT in ~1.5 minutes, generating the model directly on Render)*
   - **Start Command**:
     ```bash
     gunicorn app:app --timeout 120
     ```
   - **Instance Type**: `Free`
4. Click **Deploy Web Service**.
5. Once deployment completes, copy your live Render URL (e.g. `https://college-faq-bert-api.onrender.com`).
   - You can test it by visiting: `https://your-service.onrender.com/health` -> returns `{"status":"ok"}`.

---

## Part 3: Deploy Frontend to Netlify

You can deploy the frontend in 2 simple ways:

### Option A: Drag and Drop (Fastest, 30 seconds!)
1. Log in to [Netlify](https://app.netlify.com/).
2. Go to **Sites** -> drag and drop the `frontend` folder (`c:\Users\chait\OneDrive\Desktop\FAQs\frontend`) into the Netlify upload box.
3. Your site is live instantly!

### Option B: Deploy from GitHub
1. In Netlify, click **Add new site** -> **Import an existing project**.
2. Select your GitHub repository.
3. In **Build settings**:
   - **Base directory**: `frontend`
   - **Publish directory**: `frontend` (or leave empty)
4. Click **Deploy**.

---

## Part 4: Connect Netlify Frontend to Render Backend

1. Open your live Netlify website in your browser.
2. At the top right of the header, click the button: **`API: Default ⚙`**
3. Paste your live Render backend URL:
   ```
   https://your-service-name.onrender.com
   ```
4. Click **OK**. It is saved in your browser's local storage and immediately points all classification requests to your live Render backend!
