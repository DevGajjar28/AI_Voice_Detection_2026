# Deployment Guide

This guide helps you deploy the Voice Detection API to a cloud provider so judges can access it 24/7.

## Option 1: Render (Recommended - Free & Easy)

1.  **Push your code to GitHub**
    *   Create a new repository on GitHub.
    *   Push all files in this folder to that repository.

2.  **Create a Web Service on Render**
    *   Go to [dashboard.render.com](https://dashboard.render.com/).
    *   Click **New +** -> **Web Service**.
    *   Connect your GitHub account and select your repository.

3.  **Configure the Service**
    *   **Name**: `hcl-voice-detector` (or any name)
    *   **Region**: Any (e.g., Singapore or Frankfurt)
    *   **Branch**: `main`
    *   **Runtime**: `Docker` (Render will automatically detect the `Dockerfile`)
    *   **Instance Type**: `Free`

4.  **Deploy**
    *   Click **Create Web Service**.
    *   Wait for the build to finish (it might take 5-10 minutes to install TensorFlow).
    *   Once live, you will get a URL like `https://hcl-voice-detector.onrender.com`.

5.  **Test the Live API**
    *   Replace `http://localhost:8000` with your new URL in your tests.
    *   Example: `https://hcl-voice-detector.onrender.com/api/voice-detection`

---

## Option 2: Railway (Alternative)

1.  Go to [railway.app](https://railway.app/).
2.  Click **New Project** -> **Deploy from GitHub repo**.
3.  Select your repository.
4.  Railway will detect the `Dockerfile` and build it automatically.
5.  Once deployed, go to **Settings** -> **Networking** to generate a public domain.

## Important Notes

*   **Model Size**: The model file is ~71MB, which is safe for GitHub (limit is 100MB). You do NOT need Git LFS.
*   **Performance**: The first request might be slow on free tiers because the server "sleeps" when inactive. This is normal for free plans.
*   **API Key**: The API key is currently hardcoded as `sk_test_123456789`.
