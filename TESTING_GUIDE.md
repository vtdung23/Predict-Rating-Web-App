# 🧪 Testing Guide - Step by Step

## Pre-requisites
```bash
# Make sure dependencies are installed
pip install -r requirements.txt

# Start the server
python main.py
```

Server should start at: **http://localhost:8000**

---

## ✅ Test 1: Access Swagger UI (API Documentation)

### Steps:
1. Open browser: **http://localhost:8000/docs**
2. You should see:
   - "Vietnamese Product Rating Prediction API" title
   - Three sections: Authentication, Prediction, Dashboard
   - All endpoints listed with descriptions

### What to show teacher:
- This is **automatic API documentation** (bonus points!)
- Click any endpoint to see request/response schemas
- Click "Try it out" to test endpoints interactively

**Status:** ✅ PASS / ❌ FAIL

---

## ✅ Test 2: User Registration

### Steps:
1. Go to: **http://localhost:8000/register**
2. Fill in:
   - Username: `testuser1`
   - Email: `test@example.com`
   - Password: `password123`
3. Click "Register"
4. Should redirect to login page

### Expected Result:
- Green success message appears
- Redirects to `/login` after 1.5 seconds

**Status:** ✅ PASS / ❌ FAIL

---

## ✅ Test 3: User Login

### Steps:
1. Go to: **http://localhost:8000/login**
2. Enter:
   - Username: `testuser1`
   - Password: `password123`
3. Click "Login"

### Expected Result:
- Green "Login successful!" message
- Redirects to `/dashboard`
- You see username in top-right corner

**Status:** ✅ PASS / ❌ FAIL

---

## ✅ Test 4: Single Comment Prediction

### Steps:
1. On dashboard, select a product from dropdown (e.g., "Điện thoại iPhone 15 Pro Max")
2. Make sure "Single Comment" tab is active
3. Enter Vietnamese comment:
   ```
   Sản phẩm rất tốt, chất lượng cao, đóng gói cẩn thận. Rất hài lòng!
   ```
4. Click "Predict Rating"

### Expected Result:
- Green result box appears below
- Shows predicted rating (1-5)
- Shows confidence percentage
- Shows star rating (⭐⭐⭐⭐⭐)

**Status:** ✅ PASS / ❌ FAIL

---

## ✅ Test 5: Batch CSV Prediction

### Steps:
1. Select a product from dropdown
2. Click "Upload CSV" tab
3. Click "Choose File" and select `sample_comments.csv`
4. File name should display: "Selected: sample_comments.csv"
5. Click "Predict Batch"

### Expected Result:
- Results section appears with 3 components:

**A) Bar Chart:**
- Shows distribution of ratings (1⭐ to 5⭐)
- Colored bars (red for 1-star, green for 5-star)

**B) Word Cloud:**
- Image showing frequent Vietnamese words
- Larger words appear more frequently in comments

**C) Results Table:**
- Shows all comments with predicted ratings
- Each row has: Comment | Rating | Confidence

**Status:** ✅ PASS / ❌ FAIL

---

## ✅ Test 6: Download CSV Results

### Steps:
1. After batch prediction (Test 5), scroll to results table
2. Click "Download CSV" button (green button, top-right of table)

### Expected Result:
- CSV file downloads automatically
- Filename format: `predictions_[timestamp].csv`
- File contains columns: `Comment`, `Predicted_Rating`, `Confidence`

### Verify downloaded file:
- Open in Excel/Notepad
- Should have all 20 comments from `sample_comments.csv`
- Each has a predicted rating and confidence score

**Status:** ✅ PASS / ❌ FAIL

---

## ✅ Test 7: Test Swagger UI Endpoints

### Steps:
1. Go to: **http://localhost:8000/docs**
2. Find "POST /api/auth/login" endpoint
3. Click "Try it out"
4. Enter:
   ```json
   username: testuser1
   password: password123
   ```
5. Click "Execute"

### Expected Result:
- Response Code: 200
- Response body contains:
  ```json
  {
    "access_token": "eyJ0eXAiOiJKV1Q...",
    "token_type": "bearer"
  }
  ```

### Test authenticated endpoint:
1. Copy the `access_token` value
2. Click "Authorize" button (top-right, with lock icon)
3. Paste token in "Value" field: `Bearer YOUR_TOKEN_HERE`
4. Click "Authorize" then "Close"
5. Try "GET /api/auth/me" endpoint
6. Click "Try it out" → "Execute"

### Expected Result:
- Response Code: 200
- Shows your user info (username, email, etc.)

**Status:** ✅ PASS / ❌ FAIL

---

## ✅ Test 8: Logout

### Steps:
1. On dashboard, click "Logout" button (top-right, red button)

### Expected Result:
- Redirects to `/login` page
- Token is cleared from browser storage

**Status:** ✅ PASS / ❌ FAIL

---

## ✅ Test 9: Protected Route (Authentication Check)

### Steps:
1. After logout, try to access: **http://localhost:8000/dashboard**
2. Open browser console (F12)

### Expected Result:
- JavaScript checks for token
- Redirects back to `/login` because no token exists

**Status:** ✅ PASS / ❌ FAIL

---

## ✅ Test 10: Database Persistence

### Steps:
1. Stop the server (Ctrl+C)
2. Start it again: `python main.py`
3. Go to login page
4. Login with previous credentials (`testuser1` / `password123`)

### Expected Result:
- Login works (user data persisted in database)
- Dashboard loads successfully

**Status:** ✅ PASS / ❌ FAIL

---

## 🐛 Troubleshooting

### Error: "Module not found"
```bash
pip install -r requirements.txt
```

### Error: "Port 8000 already in use"
- Kill other process using port 8000
- Or change port in `main.py`: `uvicorn.run(..., port=8001)`

### Error: "Database is locked"
- Close all instances of the application
- Delete `app/database/rating_prediction.db`
- Restart application (will create new database)

### Word cloud doesn't show
- Check folder exists: `app/static/uploads/wordclouds/`
- Check server console for errors

### CSV upload fails
- Ensure CSV has "Comment" column (case-sensitive)
- Check CSV is UTF-8 encoded
- Make sure comments are not empty

---

## 📊 Test Results Summary

| Test | Description | Status |
|------|-------------|--------|
| 1 | Swagger UI Access | ⬜ |
| 2 | User Registration | ⬜ |
| 3 | User Login | ⬜ |
| 4 | Single Prediction | ⬜ |
| 5 | Batch CSV Prediction | ⬜ |
| 6 | CSV Download | ⬜ |
| 7 | Swagger API Testing | ⬜ |
| 8 | Logout | ⬜ |
| 9 | Auth Protection | ⬜ |
| 10 | Database Persistence | ⬜ |

Fill in: ✅ PASS / ❌ FAIL / ⚠️ PARTIAL

---

## 🎯 Demo Checklist for Teacher

Before presenting, make sure:

- [ ] Server is running (`python main.py`)
- [ ] You can access Swagger UI (http://localhost:8000/docs)
- [ ] You have a test account ready
- [ ] `sample_comments.csv` is available
- [ ] You understand the architecture (routers, services, models)
- [ ] You can explain how to replace dummy ML model

### Demo Flow:
1. **Show Swagger UI** - explain automatic generation (bonus!)
2. **Register → Login** - show JWT authentication
3. **Single prediction** - demonstrate UI
4. **Batch CSV** - show visualizations (chart + word cloud)
5. **Download CSV** - export results
6. **Explain architecture** - separation of concerns

Good luck! 🎓
