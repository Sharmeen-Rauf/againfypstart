# Vercel Environment Variables Setup

## Frontend Environment Variables

For the Botboss frontend deployed on Vercel, you need to add the following environment variable:

### Required Variable

**Key:** `VITE_API_URL`

**Value:** Your backend API URL

**Examples:**
- If backend is on Railway: `https://your-app.railway.app`
- If backend is on Render: `https://your-app.onrender.com`
- If testing locally: `http://localhost:8000`

### Step-by-Step Instructions

1. **Go to Vercel Dashboard**
   - Navigate to your project: `againfypstart`
   - Go to **Settings** → **Environment Variables**

2. **Add the Variable**
   - **Key field:** Enter `VITE_API_URL`
   - **Value field:** Enter your backend URL
   - **Environment:** Select where to apply (Production, Preview, Development)
     - Recommended: Select all three (Production, Preview, Development)

3. **Save**
   - Click the **"Save"** button at the bottom right

4. **Redeploy (if needed)**
   - After adding environment variables, you may need to trigger a new deployment
   - Go to **Deployments** tab
   - Click the three dots (⋯) on the latest deployment
   - Select **"Redeploy"**

### Environment Selection

- **Production:** Used for production deployments (main branch)
- **Preview:** Used for preview deployments (pull requests, branches)
- **Development:** Used for development deployments

**Recommendation:** Add the variable to all three environments for consistency.

### Verification

After deployment, check:
1. Open your deployed frontend URL
2. Check browser console (F12) for any API connection errors
3. Try logging in - if it works, the environment variable is configured correctly

### Notes

- Environment variables prefixed with `VITE_` are exposed to the frontend
- Changes to environment variables require a new deployment to take effect
- Never commit environment variables to Git (use Vercel's interface instead)

