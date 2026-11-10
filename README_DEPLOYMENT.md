# College FAQ Classifier - Deployment Guide
## Architecture: Render (Backend) + Netlify (Frontend)

This guide walks you through deploying the project with the backend hosted on **Render** (`https://faq-2e3h.onrender.com`) and the frontend hosted on **Netlify**.

---

## 1. Push Latest Code to GitHub

Your repository is already linked to GitHub (`https://github.com/Chaithanyamandula/FAQs.git`).
Commit and push the latest deployment configuration:

```bash
git add .
git commit -m "Configure Render and Netlify deployment with faq.onrender.com backend"
git push origin main
```

*(Note: `.gitignore` automatically excludes `venv/` and `model/`. Render will automatically install dependencies and train the model during build).*

---

## 2. Deploy Backend to Render

1. Log in to your [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** > **Web Service**.
3. Connect your GitHub account and choose repository: **`Chaithanyamandula/FAQs`**.
4. Configure the Web Service settings:
   - **Name**: `faq` *(This gives you `https://faq-2e3h.onrender.com`)*
     > *Note: If `faq` is already claimed by someone else on Render, Render will append random characters (e.g. `faq-xyz1.onrender.com`). You can customize the name or use the gear icon `⚙` on the frontend UI to paste the final URL if it differs.*
   - **Runtime**: `Python 3`
   - **Branch**: `main`
   - **Build Command**:
     ```bash
     pip install -r requirements.txt && python train.py
     ```
   - **Start Command**:
     ```bash
     gunicorn app:app --workers 1 --threads 4 --timeout 120
     ```
   - **Instance Type**: `Free`
5. Click **Deploy Web Service**.
6. When deployment finishes (approx 2 minutes), test your backend health in your browser:
   ```
   https://faq-2e3h.onrender.com/health
   ```
   It should return: `{"service": "college-faq-bert-api", "status": "ok"}`.

---

## 3. Deploy Frontend to Netlify

Choose either **Option A** or **Option B**:

### Option A: Drag and Drop (Instant - 30 seconds)
1. Go to your [Netlify Dashboard](https://app.netlify.com/).
2. Click on **Sites**.
3. Drag and drop the **`frontend`** folder (`c:\Users\chait\OneDrive\Desktop\FAQs\frontend`) directly into the Netlify drop zone.
4. Your frontend is instantly published with a live `.netlify.app` URL!

### Option B: Connect via GitHub (Automatic CI/CD)
1. In Netlify, click **Add new site** > **Import an existing project**.
2. Connect your GitHub account and select **`Chaithanyamandula/FAQs`**.
3. Netlify will auto-detect the root `netlify.toml` which automatically points to the `frontend` directory.
   - **Base directory**: (leave blank or `frontend`)
   - **Publish directory**: `frontend`
4. Click **Deploy FAQs**.

---

## 4. Frontend & Backend Connection

- The frontend is pre-configured with `DEFAULT_BACKEND_URL = "https://faq-2e3h.onrender.com"`.
- Netlify redirect rules (`_redirects` and `netlify.toml`) proxy `/api/*` directly to `https://faq-2e3h.onrender.com/api/:splat`.
- CORS is enabled on the Flask backend so direct cross-origin API calls are fully supported.
- **Render Cold Starts**: On the Free tier, Render puts web services to sleep after 15 minutes of inactivity. When you send the first request after it sleeps, please allow ~40–50 seconds for the container to wake up.
- **Custom URL Switcher**: If your Render service URL differs (e.g. `https://faq-xxxx.onrender.com`), you can click the **`API: faq.onrender.com ⚙`** button in the header of the frontend to update the URL in 1 click without redeploying!
