# Deploying to Render.com

This guide will help you deploy your **Resume Builder** on Render.com.

Since you have a monorepo (Frontend + Backend in one repo), we will deploy them as two separate services:
1.  **Backend (Web Service)**: Python/Django
2.  **Frontend (Static Site)**: React

---

## Prerequisite: Push to GitHub/GitLab
Make sure your code is pushed to a remote repository (GitHub or GitLab). Render needs this to pull your code.

---

## Part 1: Deploy Backend (Django)

1.  Log in to [Render Dashboard](https://dashboard.render.com/).
2.  Click **New +** -> **Web Service**.
3.  Connect your GitHub repository.
4.  Configure the service:
    *   **Name**: `resume-backend` (or any name)
    *   **Root Directory**: `backend/core` (Important!)
    *   **Runtime**: `Python 3`
    *   **Build Command**: `./render-build.sh`
    *   **Start Command**: `gunicorn core.wsgi:application`
5.  **Environment Variables** (Scroll down to "Advanced"):
    Add the following keys:
    *   `PYTHON_VERSION`: `3.9.0` (or your local version)
    *   `SECRET_KEY`: (Generate a random string)
    *   `DEBUG`: `False`
    *   `ALLOWED_HOSTS`: `*` (or your render URL like `resume-backend.onrender.com`)
    *   `Database`: Render will ask if you want to add a Postgres DB. **Yes, create one.**
        *   Or manually create a **New + -> PostgreSQL** instance on Render.
        *   Copy the `Internal Database URL`.
        *   Add env var `DATABASE_URL` with that value in your Web Service.
6.  Click **Create Web Service**.
7.  Wait for the build to finish. Once live, copy your backend URL (e.g., `https://resume-backend.onrender.com`).

---

## Part 2: Deploy Frontend (React)

1.  On Render Dashboard, click **New +** -> **Static Site**.
2.  Connect the **SAME** GitHub repository.
3.  Configure the service:
    *   **Name**: `resume-frontend`
    *   **Root Directory**: `frontend` (Important!)
    *   **Build Command**: `npm install; npm run build`
    *   **Publish Directory**: `build`
4.  **Environment Variables**:
    *   `REACT_APP_API_URL`: Paste your **Backend URL** from Part 1 (e.g., `https://resume-backend.onrender.com`).
        *   *Note: Do NOT add a trailing slash `/`.*
5.  Click **Create Static Site**.
6.  Wait for the build to finish.

---

## Part 3: Final Configuration

1.  Go back to your **Backend Service** on Render settings.
2.  Update the **Environment Variables**:
    *   `CORS_ALLOWED_ORIGINS`: Add your **Frontend URL** (e.g., `https://resume-frontend.onrender.com`).
    *   `ALLOWED_HOSTS`: Ensure your backend URL is here (usually `*` is easiest for start, or comma-separated domains).
3.  **Redeploy** the Backend (Manual Deploy -> Clear Cache & Deploy) if needed to apply changes.

---

## 🎉 Done!
Visit your **Frontend URL**. You should see the Resume Builder. It will talk to your separate Backend service to generate PDFs.
