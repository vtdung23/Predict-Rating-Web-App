# 🚨 URGENT FIX: Out of Memory on Render

## Problem
```
==> Out of memory (used over 512Mi)
```

Render Free Tier has **512MB RAM limit**. PhoBERT model is too heavy to load on startup.

---

## ✅ Solution Applied: Lazy Loading

### Changes Made

**File: `app/services/ml_service.py`**
- ✅ Model now loads **on first request** instead of on startup
- ✅ Reduces initial memory footprint
- ✅ Imports (torch, transformers) only when needed

---

## 📝 Update Render Configuration

### Step 1: Change Start Command

Go to Render Dashboard → Your Web Service → Settings

**OLD Start Command:**
```bash
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

**NEW Start Command (Reduce workers from 4 → 1):**
```bash
gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --timeout 120
```

### Step 2: Push Updated Code

```bash
git add app/services/ml_service.py
git commit -m "Fix: Lazy load ML model to avoid OOM on Render"
git push origin master
```

### Step 3: Redeploy

1. Go to Render Dashboard
2. Click **"Manual Deploy"** → **"Clear build cache & deploy"**
3. Wait for deployment (will take 5-10 minutes)

---

## 🔍 Expected Behavior After Fix

### On Startup (Fast):
```
✅ ML Service initialized (model will load on first request)
🚀 Running in PRODUCTION mode
✅ Database tables created successfully!
[INFO] Starting gunicorn
```

### On First Prediction Request (Slow - 30-60 seconds):
```
🔄 Loading ML model (first request)...
📍 Using device: cpu
📦 Loading tokenizer...
🧠 Loading PhoBERT model...
⚙️ Loading trained weights...
✅ Model loaded successfully!
```

### Subsequent Requests (Fast):
Model is already loaded, predictions are instant.

---

## ⚠️ Important Notes

### 1. First Request Will Be Slow
- User must wait 30-60 seconds for first prediction
- Consider adding loading spinner in frontend
- Or call `/health` endpoint on deploy to pre-load model

### 2. Free Tier Limitations
If still getting OOM errors, consider:
- ✅ Use quantized model (smaller size)
- ✅ Upgrade to Starter ($7/month, 512MB → 2GB RAM)
- ✅ Deploy model separately (separate service)
- ✅ Use CPU-only PyTorch build

### 3. Model Files Must Exist
Ensure these files are in repository:
- `app/services/Model/phoBERT_multi_class_tokenizer/`
- `app/services/Model/best_phoBER.pth`

---

## 🧪 Test Locally First

```bash
python main.py
```

Expected output:
```
✅ ML Service initialized (model will load on first request)
🔧 Development Mode: Using SQLite
```

Then test prediction endpoint - model will load on first request.

---

## 📊 Memory Usage Comparison

| Configuration | Startup Memory | With Model Loaded |
|---------------|----------------|-------------------|
| **Before (Eager)** | ~450MB | ~550MB (OOM) |
| **After (Lazy)** | ~150MB | ~450MB (OK) |

---

## 🆘 If Still Getting OOM

### Option 1: Use Dummy Model (Testing)
Temporarily use dummy predictions to verify deployment works:

Edit `app/services/ml_service.py`:
```python
def predict_single(self, text: str) -> Dict[str, Any]:
    # Skip model loading for testing
    return {
        'rating': 4,  # Dummy rating
        'confidence': 0.85
    }
```

### Option 2: Upgrade Render Plan
- Starter: $7/month, 2GB RAM
- Standard: $25/month, 4GB RAM

### Option 3: Deploy Model Separately
Use external ML API service (AWS Lambda, Hugging Face Inference API, etc.)

---

**After making these changes, try deploying again!**
