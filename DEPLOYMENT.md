# Deployment Guide - Fixing 404 Error on Vercel

## Issues Fixed

1. ✅ Added missing `HRDashboard` component
2. ✅ Added missing `Interview.css` stylesheet
3. ✅ Created `vercel.json` for proper routing
4. ✅ Updated all components to use environment variables for API URLs
5. ✅ Added `.gitignore` file

## Steps to Deploy Successfully

### 1. Frontend Deployment (Vercel)

1. **Push your code to GitHub** (if not already done)

2. **Connect to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Set the root directory to `frontend`

3. **Configure Environment Variables**:
   - In Vercel project settings, add:
     ```
     VITE_API_URL=https://your-backend-url.com
     ```
   - Replace with your actual backend URL

4. **Build Settings**:
   - Framework Preset: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

5. **Deploy**

### 2. Backend Deployment (Railway/Render)

#### Option A: Railway

1. Go to [railway.app](https://railway.app)
2. Create new project from GitHub
3. Select your repository
4. Set root directory to `backend`
5. Add environment variables:
   ```
   OPENAI_API_KEY=your-openai-api-key
   SECRET_KEY=your-secret-key
   ```
6. Railway will auto-detect Python and install dependencies
7. Add a start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

#### Option B: Render

1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect GitHub repository
4. Settings:
   - Root Directory: `backend`
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables:
   ```
   OPENAI_API_KEY=your-openai-api-key
   SECRET_KEY=your-secret-key
   ```

### 3. Update Frontend Environment Variable

After backend is deployed, update `VITE_API_URL` in Vercel to point to your backend URL.

### 4. CORS Configuration

Make sure your backend allows requests from your Vercel domain. The backend already has CORS configured, but you may need to add your Vercel domain:

In `backend/app/main.py`, update:
```python
allow_origins=["http://localhost:3000", "http://localhost:5173", "https://your-vercel-app.vercel.app"]
```

## Testing Locally Before Deployment

1. **Start Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   python seed_data.py
   uvicorn app.main:app --reload --port 8000
   ```

2. **Start Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Test the application**:
   - Login with test credentials
   - Start an interview
   - Check HR dashboard

## Common Issues

### 404 Error on Vercel
- ✅ Fixed: Added `vercel.json` with proper rewrites
- Make sure `vercel.json` is in the `frontend` directory

### API Connection Errors
- Check `VITE_API_URL` environment variable in Vercel
- Ensure backend CORS allows your Vercel domain
- Check backend is running and accessible

### Build Failures
- Ensure all dependencies are in `package.json`
- Check Node.js version (Vercel uses Node 18+ by default)
- Review build logs in Vercel dashboard

## File Structure for Deployment

```
againfypstart/
├── frontend/          # Deploy this to Vercel
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
│   └── vercel.json    # ✅ Added for routing
├── backend/           # Deploy this to Railway/Render
│   ├── app/
│   ├── requirements.txt
│   └── seed_data.py
└── README.md
```

## Next Steps After Deployment

1. Test the deployed application
2. Update any hardcoded URLs
3. Set up proper database (consider PostgreSQL for production)
4. Add error monitoring (Sentry, etc.)
5. Set up CI/CD pipelines

