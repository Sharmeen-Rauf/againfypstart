# Deploying Backend on Vercel

## Prerequisites

1. Your backend code is in the `backend` directory
2. You have a Vercel account
3. Your MongoDB connection string is ready

## Step-by-Step Deployment

### 1. Prepare Your Backend

The backend is already configured with:
- ✅ `vercel.json` configuration file
- ✅ `api/index.py` serverless entry point
- ✅ FastAPI app setup for serverless

### 2. Deploy to Vercel

#### Option A: Using Vercel CLI (Recommended)

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm i -g vercel
   ```

2. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

3. **Login to Vercel**:
   ```bash
   vercel login
   ```

4. **Deploy**:
   ```bash
   vercel
   ```
   
   - Follow the prompts
   - Select your project or create a new one
   - **Important**: Set root directory as `backend` (or just deploy from backend folder)

5. **Deploy to Production**:
   ```bash
   vercel --prod
   ```

#### Option B: Using Vercel Dashboard

1. **Go to Vercel Dashboard**: https://vercel.com/dashboard
2. **Click "Add New" → "Project"**
3. **Import your Git Repository**
4. **Configure Project**:
   - **Root Directory**: Set to `backend`
   - **Framework Preset**: Other (or leave blank)
   - **Build Command**: Leave empty (Vercel auto-detects Python)
   - **Output Directory**: Leave empty
   - **Install Command**: `pip install -r requirements.txt`

5. **Add Environment Variables** (see step 3 below)

6. **Deploy**

### 3. Add Environment Variables in Vercel

In your Vercel project settings, go to **Environment Variables** and add:

| Key | Value | Environment |
|-----|-------|-------------|
| `MONGODB_URL` | `mongodb+srv://f90396245_db_user:resturentwebsitenew@cluster0.94frwr3.mongodb.net/?appName=Cluster0` | Production, Preview, Development |
| `DATABASE_NAME` | `botboss` | Production, Preview, Development |
| `SECRET_KEY` | Your JWT secret key | Production, Preview, Development |
| `OPENAI_API_KEY` | Your OpenAI API key | Production, Preview, Development |

**Important Notes:**
- ⚠️ Never commit these values to Git
- ✅ Add them via Vercel dashboard
- ✅ Use different values for production vs development if needed

### 4. Update Frontend Environment Variable

After backend is deployed, get your backend URL (e.g., `https://your-project.vercel.app`) and add it to your frontend's Vercel project:

**Frontend Environment Variable:**
- Key: `VITE_API_URL`
- Value: `https://your-backend-project.vercel.app`

### 5. Test Your Deployment

1. Visit your backend URL: `https://your-project.vercel.app`
2. Check API docs: `https://your-project.vercel.app/docs`
3. Test health endpoint: `https://your-project.vercel.app/api/health`

## Project Structure for Vercel

```
backend/
├── api/
│   └── index.py          # Vercel serverless entry point
├── app/
│   ├── main.py           # FastAPI app
│   ├── database.py
│   ├── models.py
│   └── routers/
├── requirements.txt
└── vercel.json           # Vercel configuration
```

## Important Notes

### Serverless Considerations

1. **Cold Starts**: First request after inactivity may be slower
2. **Connection Pooling**: MongoDB connections are managed per request
3. **Function Timeout**: Default is 10 seconds (can be increased in Vercel Pro)
4. **Database Initialization**: Runs on each cold start (optimized in code)

### Limitations

- Free tier has function execution limits
- Maximum execution time: 10 seconds (free) / 60 seconds (Pro)
- Consider upgrading to Pro for production use

### Troubleshooting

1. **Import Errors**: Check that `api/index.py` has correct path setup
2. **Environment Variables**: Verify all are set correctly
3. **Build Errors**: Check `requirements.txt` is complete
4. **Database Connection**: Verify MongoDB URL and network access

## Alternative: Using Railway/Render

If you encounter limitations with Vercel's serverless functions, consider:
- **Railway**: Better for long-running connections
- **Render**: Good free tier for web services

But Vercel works well for most FastAPI applications! 🚀

