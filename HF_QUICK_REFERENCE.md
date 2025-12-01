# 🚀 Hugging Face Spaces - Quick Reference Card

## ⚡ Quick Deploy (5 Steps)

```bash
# 1. Create Space on HF
https://huggingface.co/new-space → Docker SDK → CPU Basic

# 2. Add Secrets (Settings → Repository Secrets)
DATABASE_URL = postgresql://user:pass@host:port/db
SECRET_KEY = <generate with: python -c "import secrets; print(secrets.token_urlsafe(32))">

# 3. Clone Space repo
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE
cd YOUR_SPACE

# 4. Copy project files
# Copy all except: env/, __pycache__/, *.db, .env

# 5. Push
git add .
git commit -m "Initial deployment"
git push origin main
```

---

## 🔐 Environment Variables

| Variable | Required | Example |
|----------|----------|---------|
| `DATABASE_URL` | ✅ Yes | `postgresql://user:pass@host:5432/db` |
| `SECRET_KEY` | ✅ Yes | `xK7mP9vR2nQ5wT8yU4eL6hG3jN0bM...` |

---

## 📋 Critical Files Checklist

```
✅ Dockerfile (port 7860, user 1000)
✅ requirements.txt (no gunicorn)
✅ main.py
✅ app/ directory
✅ .dockerignore
✅ README.md (from README_HF_SPACE.md)
```

---

## 🐳 Dockerfile Must-Haves

```dockerfile
# ✅ Port 7860 (HF requirement)
EXPOSE 7860
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]

# ✅ User ID 1000 (HF requirement)
RUN useradd -m -u 1000 user
USER user

# ✅ Write permissions
RUN chmod -R 777 /app/app/static/uploads
```

---

## 🧪 Test Locally

```bash
# Build
docker build -t test .

# Run
docker run -p 7860:7860 \
  -e DATABASE_URL="postgresql://..." \
  -e SECRET_KEY="..." \
  test

# Access
http://localhost:7860
```

---

## 🔍 Verify Deployment

```
✅ Space shows "Running" status
✅ Logs show: "🚀 Production Mode: Using PostgreSQL"
✅ Access /docs (Swagger UI)
✅ Can register and login
✅ Predictions work
```

---

## 🐛 Common Errors

| Error | Fix |
|-------|-----|
| App startup failed | Check DATABASE_URL in Secrets |
| 502 Bad Gateway | Wait 2-3 min for model loading |
| Permission denied | Check Dockerfile user permissions |
| Database refused | Allow external connections in DB |

---

## 📊 Key Differences: Render vs HF

| | Render | Hugging Face |
|-|--------|--------------|
| RAM | 512MB | 16GB |
| Port | Auto | 7860 (fixed) |
| Deploy | Procfile | Dockerfile |
| User | root | user (1000) |

---

## 📚 Documentation Files

- `HUGGING_FACE_DEPLOYMENT.md` - Full guide
- `HF_ENV_VARIABLES.md` - Secrets setup
- `HF_DEPLOYMENT_CHECKLIST.md` - Step-by-step
- `HF_MIGRATION_SUMMARY.md` - Overview

---

## 🆘 Emergency Commands

```bash
# View logs
# Go to Space → Logs tab

# Rebuild
git commit --allow-empty -m "Rebuild"
git push

# Rollback
git revert HEAD
git push
```

---

## ✅ Success Indicators

```
INFO:     Started server process [1]
INFO:     Uvicorn running on http://0.0.0.0:7860
🚀 Production Mode: Using PostgreSQL
```

---

## 🔗 Important Links

- Create Space: https://huggingface.co/new-space
- HF Docs: https://huggingface.co/docs/hub/spaces-sdks-docker
- FastAPI Docs: https://fastapi.tiangolo.com

---

**Print this for quick reference during deployment! 📄**
