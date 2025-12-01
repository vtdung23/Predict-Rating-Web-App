# ✅ Hugging Face Spaces Deployment Checklist

## Pre-Deployment (Local Setup)

### 1. Database Preparation
- [ ] Create external PostgreSQL database (Render/Neon)
- [ ] Test database connection locally
- [ ] Run database migrations (if any)
- [ ] Create initial admin user (optional)

### 2. Code Preparation
- [ ] Review `Dockerfile` (port 7860, user permissions)
- [ ] Verify `requirements.txt` has all dependencies
- [ ] Check `database.py` hybrid connection logic
- [ ] Test application locally with Docker
- [ ] Generate strong `SECRET_KEY`

### 3. Files to Push
- [ ] `Dockerfile` (CRITICAL)
- [ ] `requirements.txt`
- [ ] `main.py`
- [ ] `app/` directory (all modules)
- [ ] `README_HF_SPACE.md` (rename to README.md)
- [ ] `.dockerignore`

### 4. Files to EXCLUDE
- [ ] `.env` files (secrets)
- [ ] `env/` or `venv/` directories
- [ ] `__pycache__/` directories
- [ ] Local `.db` files
- [ ] `app/static/uploads/` temporary files

---

## Hugging Face Spaces Setup

### 1. Create New Space
- [ ] Go to https://huggingface.co/new-space
- [ ] Choose a memorable Space name
- [ ] Select **Docker** SDK
- [ ] Choose **CPU Basic** (16GB RAM - Free Tier)
- [ ] Set visibility (Public/Private)
- [ ] Click **Create Space**

### 2. Configure Environment Variables
Navigate to **Settings** → **Repository Secrets**

**Required Secrets:**
- [ ] Add `DATABASE_URL`
  ```
  postgresql://user:pass@host:port/database
  ```
- [ ] Add `SECRET_KEY`
  ```
  (generated random string, 32+ chars)
  ```

**Verify:**
- [ ] Secrets show as `***` (hidden)
- [ ] No typos in variable names
- [ ] DATABASE_URL starts with `postgresql://`

---

## Deployment

### 1. Push Code to HF Space
```bash
# Clone your Space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE
cd YOUR_SPACE

# Copy project files
# (Exclude env/, __pycache__, .db files)

# IMPORTANT: Rename README
cp README_HF_SPACE.md README.md

# Initialize git (if needed)
git init
git remote add origin https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE

# Commit and push
git add .
git commit -m "Initial deployment to Hugging Face Spaces"
git push -u origin main
```

### 2. Monitor Build
- [ ] Go to your Space URL
- [ ] Click **Logs** tab
- [ ] Watch Docker build process
- [ ] Wait for "Running on http://0.0.0.0:7860" message
- [ ] Build time: ~5-10 minutes

### 3. Expected Build Stages
```
✅ Building Docker image...
✅ Installing dependencies from requirements.txt...
✅ Downloading PyTorch & Transformers (~2GB)...
✅ Creating user 'user' (UID 1000)...
✅ Setting permissions...
✅ Starting uvicorn server...
✅ Application running on port 7860
```

---

## Post-Deployment Verification

### 1. Check Application Status
- [ ] Space shows "Running" status (green)
- [ ] No errors in Logs tab
- [ ] Access Space URL (opens app)

### 2. Test Database Connection
Expected log message:
```
🚀 Production Mode: Using PostgreSQL
```

If you see this instead:
```
🔧 Development Mode: Using SQLite
```
→ DATABASE_URL is missing or incorrect

### 3. Test Core Functionality
- [ ] Access `/docs` (Swagger UI loads)
- [ ] Register a new user
- [ ] Login successfully
- [ ] Access dashboard
- [ ] Make a single prediction
- [ ] Upload CSV for batch prediction
- [ ] View prediction history
- [ ] Word cloud generates
- [ ] Charts display correctly

### 4. Security Verification
- [ ] Cannot access protected routes without JWT
- [ ] Passwords are hashed (check database)
- [ ] JWT tokens expire after 24 hours
- [ ] HTTPS is enabled (HF provides this)

---

## Troubleshooting

### Issue: Build Failed
**Check:**
- [ ] Dockerfile syntax errors
- [ ] Missing dependencies in requirements.txt
- [ ] Python version compatibility
- [ ] Check Logs for specific error

### Issue: "Application startup failed"
**Check:**
- [ ] DATABASE_URL is set correctly
- [ ] Database is accessible (not firewalled)
- [ ] SECRET_KEY is set
- [ ] Port 7860 is used in CMD

### Issue: "502 Bad Gateway"
**Check:**
- [ ] App is still starting (wait 2-3 min)
- [ ] Heavy model loading in progress
- [ ] Check Logs for crash/errors

### Issue: Database Connection Error
**Check:**
- [ ] DATABASE_URL format is correct
- [ ] Database host is reachable
- [ ] Username/password are correct
- [ ] Database allows external connections

### Issue: JWT Token Invalid
**Check:**
- [ ] SECRET_KEY is set correctly
- [ ] SECRET_KEY hasn't changed
- [ ] Token hasn't expired (24h)
- [ ] Clear browser localStorage

---

## Maintenance

### Regular Tasks
- [ ] Monitor Space usage (CPU/Memory)
- [ ] Check application logs weekly
- [ ] Rotate SECRET_KEY every 90 days
- [ ] Backup PostgreSQL database regularly
- [ ] Update dependencies monthly

### Updating the App
```bash
# Make changes locally
git add .
git commit -m "Update: description"
git push

# HF will automatically rebuild
# Monitor Logs tab for build status
```

### Scaling Considerations
If you exceed Free Tier limits:
- [ ] Upgrade to **Pro** Space (better hardware)
- [ ] Consider upgrading database plan
- [ ] Implement caching (Redis)
- [ ] Optimize model loading

---

## Performance Optimization

### For Heavy Models
- [ ] Use model quantization (reduces size)
- [ ] Cache model in memory (don't reload)
- [ ] Use CPU inference (GPU costs more)
- [ ] Implement request queuing

### For High Traffic
- [ ] Add rate limiting
- [ ] Implement Redis caching
- [ ] Use CDN for static files
- [ ] Optimize database queries
- [ ] Add connection pooling

---

## Security Hardening

### Production Checklist
- [ ] Use strong SECRET_KEY (32+ chars)
- [ ] Enable DATABASE SSL (sslmode=require)
- [ ] Implement rate limiting
- [ ] Add CORS restrictions
- [ ] Log all authentication attempts
- [ ] Implement password strength requirements
- [ ] Add 2FA (future enhancement)
- [ ] Regular security audits

---

## Rollback Plan

If deployment fails:

### Option 1: Revert Git Commit
```bash
git revert HEAD
git push
```

### Option 2: Delete and Recreate Space
1. Delete current Space
2. Create new Space with same name
3. Re-add environment variables
4. Push working version

### Option 3: Use Previous Docker Image
HF keeps previous builds for Pro users

---

## Success Criteria

Deployment is successful when:
- ✅ Space status is "Running"
- ✅ No errors in Logs
- ✅ PostgreSQL connection established
- ✅ All API endpoints respond
- ✅ Frontend loads correctly
- ✅ Users can register and login
- ✅ Predictions work (single + batch)
- ✅ Visualizations generate
- ✅ JWT authentication works

---

## Support Resources

- 📖 [Hugging Face Spaces Docs](https://huggingface.co/docs/hub/spaces-overview)
- 📖 [Docker SDK Guide](https://huggingface.co/docs/hub/spaces-sdks-docker)
- 📖 [FastAPI Documentation](https://fastapi.tiangolo.com)
- 📖 [SQLAlchemy Docs](https://docs.sqlalchemy.org)
- 💬 [HF Community Forum](https://discuss.huggingface.co)

---

**Last Updated:** December 2025
**Version:** 1.0.0
