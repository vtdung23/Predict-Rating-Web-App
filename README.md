# Vietnamese Product Rating Prediction System

## 🎯 Project Overview
A full-stack web application that predicts sentiment ratings (1-5 stars) for Vietnamese product reviews using Machine Learning.

**Built for:** Introduction to Machine Learning - University Project  
**Tech Stack:** FastAPI + Jinja2 + TailwindCSS + SQLite + Chart.js

---

## 📁 Project Structure

```
PredictRating/
├── app/
│   ├── database/              # SQLite database storage
│   ├── routers/              # API route handlers
│   │   ├── auth.py           # Authentication endpoints
│   │   ├── prediction.py     # Prediction endpoints
│   │   └── dashboard.py      # Frontend routes
│   ├── services/             # Business logic
│   │   ├── auth_service.py   # JWT & password handling
│   │   ├── ml_service.py     # ML prediction (DUMMY - replace with your model)
│   │   └── visualization_service.py  # WordCloud & charts
│   ├── static/               # Static files (CSS, JS, uploads)
│   │   └── uploads/
│   │       └── wordclouds/   # Generated word cloud images
│   ├── templates/            # Jinja2 HTML templates
│   │   ├── base.html         # Base layout
│   │   ├── login.html        # Login page
│   │   ├── register.html     # Registration page
│   │   └── dashboard.html    # Main prediction interface
│   ├── config.py             # Configuration settings
│   ├── database.py           # Database connection
│   ├── models.py             # SQLAlchemy models (User, PredictionHistory)
│   └── schemas.py            # Pydantic validation schemas
├── main.py                   # FastAPI application entry point
└── requirements.txt          # Python dependencies
```

---

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python main.py
```

The server will start at: **http://localhost:8000**

### 3. Access the Application

- **Frontend Dashboard:** http://localhost:8000/dashboard
- **API Documentation (Swagger UI):** http://localhost:8000/docs  ⭐ **SHOW THIS TO YOUR TEACHER**
- **Alternative API Docs (ReDoc):** http://localhost:8000/redoc

---

## 📚 API Documentation (Swagger UI)

FastAPI automatically generates **interactive API documentation** at `/docs`.

### How to Access:
1. Run the application
2. Open browser: **http://localhost:8000/docs**
3. You'll see all API endpoints with:
   - Request/response schemas
   - Try it out functionality
   - Authentication support

### Key API Endpoints:

#### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login (get JWT token)
- `GET /api/auth/me` - Get current user info

#### Predictions
- `POST /api/predict/single` - Predict single comment
- `POST /api/predict/batch` - Predict batch from CSV
- `GET /api/predict/history` - Get prediction history

---

## 🎓 How to Use (User Journey)

### Step 1: Register/Login
1. Go to http://localhost:8000/login
2. Register a new account or login
3. You'll be redirected to the dashboard

### Step 2: Select Product
- Choose a target product from the dropdown list

### Step 3A: Single Comment Prediction
1. Click "Single Comment" tab
2. Enter a Vietnamese product review
3. Click "Predict Rating"
4. See the predicted rating (1-5 stars) with confidence score

### Step 3B: Batch CSV Prediction
1. Click "Upload CSV" tab
2. Upload a CSV file with a `Comment` column
3. Click "Predict Batch"
4. View results:
   - **Bar Chart:** Rating distribution (how many 1⭐, 2⭐, etc.)
   - **Word Cloud:** Most frequent words in comments
   - **Table:** All predictions with confidence scores
   - **Download:** Export results as CSV with `Predicted_Rating` column

---

## 🔧 Replace Dummy ML Model

The current `ml_service.py` uses a **DUMMY** prediction function. Replace it with your real model:

### File: `app/services/ml_service.py`

```python
class MLPredictionService:
    def __init__(self):
        # TODO: Load your trained model
        self.model = load_model('path/to/your/model.h5')  # Example
        self.tokenizer = load_tokenizer('path/to/tokenizer.pkl')
    
    def predict_single(self, text: str) -> Dict[str, any]:
        # TODO: Implement your preprocessing
        preprocessed = self.preprocess(text)
        
        # TODO: Make prediction with your model
        prediction = self.model.predict(preprocessed)
        rating = self.postprocess(prediction)  # Convert to 1-5
        
        return {
            'rating': rating,
            'confidence': prediction.max()
        }
```

---

## 📊 Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email
- `hashed_password`: Bcrypt hashed password
- `created_at`: Registration timestamp

### Prediction History Table
- `id`: Primary key
- `user_id`: Foreign key to Users
- `product_name`: Product name
- `comment`: Original comment
- `predicted_rating`: Predicted rating (1-5)
- `confidence_score`: Confidence (0-1)
- `prediction_type`: 'single' or 'batch'
- `created_at`: Prediction timestamp

---

## 🎨 Features

✅ **Authentication:** JWT-based secure login/registration  
✅ **Single Prediction:** Predict one comment at a time  
✅ **Batch Prediction:** Upload CSV and predict multiple comments  
✅ **Visualization:**
  - Bar chart for rating distribution  
  - Word cloud for frequent words  
✅ **History Tracking:** All predictions saved to database  
✅ **CSV Export:** Download results with predicted ratings  
✅ **Responsive UI:** TailwindCSS mobile-friendly design  
✅ **API Documentation:** Auto-generated Swagger UI  

---

## 🏆 Bonus Points for Teacher Demo

1. **Show Swagger UI** at `/docs` - Automatic API documentation ⭐
2. **Demonstrate:**
   - User registration/login flow
   - Single comment prediction
   - CSV batch upload with visualizations
   - Download CSV results
3. **Explain:**
   - Clean separation of concerns (routers, services, models)
   - RESTful API design
   - JWT authentication
   - Database relationships

---

## 📝 CSV File Format

Your CSV file should have at least a `Comment` column:

```csv
Comment
"Sản phẩm rất tốt, đóng gói cẩn thận"
"Chất lượng kém, không như mô tả"
"Giao hàng nhanh, sản phẩm ổn"
```

After prediction, you'll get:

```csv
Comment,Predicted_Rating,Confidence
"Sản phẩm rất tốt, đóng gói cẩn thận",5,0.95
"Chất lượng kém, không như mô tả",1,0.88
"Giao hàng nhanh, sản phẩm ổn",4,0.92
```

---

## 🔐 Security Notes

- Change `SECRET_KEY` in `app/config.py` before deployment
- Passwords are hashed using bcrypt
- JWT tokens expire after 24 hours
- CORS is enabled for development (configure for production)

---

## 🐛 Troubleshooting

### Issue: "Import errors" when running
**Solution:** Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: "Database errors"
**Solution:** Delete `app/database/rating_prediction.db` and restart the app to recreate tables

### Issue: "Word cloud doesn't display"
**Solution:** Check that `app/static/uploads/wordclouds/` directory exists

---

## 📧 Support

For questions about the project structure or implementation, refer to the code comments or consult your instructor.

**Good luck with your project presentation! 🎓**
