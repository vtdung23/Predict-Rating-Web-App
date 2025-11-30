"""
Prediction Router
Handles single and batch predictions
"""
import io
import csv
from typing import List, Dict
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, PredictionHistory
from app.schemas import (
    SinglePredictionRequest,
    SinglePredictionResponse,
    BatchPredictionResponse,
    PredictionHistoryResponse,
    PDFReportRequest
)
from app.services.auth_service import get_current_user
from app.services.ml_service import get_ml_service, MLPredictionService
from app.services.visualization_service import get_viz_service, VisualizationService
from app.services.report_service import get_report_service, ReportService

router = APIRouter()


@router.post("/single", response_model=SinglePredictionResponse)
async def predict_single(
    request: SinglePredictionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    ml_service: MLPredictionService = Depends(get_ml_service)
):
    """
    Predict rating for a single comment
    
    - **product_name**: Name of the product
    - **comment**: Vietnamese product review text
    
    Returns predicted rating (1-5 stars) with confidence score
    """
    # Make prediction
    prediction = ml_service.predict_single(request.comment)
    
    # Save to history
    history = PredictionHistory(
        user_id=current_user.id,
        product_name=request.product_name,
        comment=request.comment,
        predicted_rating=prediction['rating'],
        confidence_score=prediction['confidence'],
        prediction_type='single'
    )
    db.add(history)
    db.commit()
    
    return {
        "predicted_rating": prediction['rating'],
        "confidence_score": prediction['confidence'],
        "comment": request.comment
    }


@router.post("/batch", response_model=BatchPredictionResponse)
async def predict_batch(
    product_name: str = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    ml_service: MLPredictionService = Depends(get_ml_service),
    viz_service: VisualizationService = Depends(get_viz_service),
    report_service: ReportService = Depends(get_report_service)
):
    """
    Predict ratings for batch of comments from CSV file
    
    - **product_name**: Name of the product
    - **file**: CSV file with 'Comment' column
    
    Returns predictions with visualization data (wordcloud, distribution chart)
    """
    # Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be a CSV"
        )
    
    try:
        # Read CSV file
        contents = await file.read()
        csv_file = io.StringIO(contents.decode('utf-8'))
        reader = csv.DictReader(csv_file)
        
        # Check for Comment column
        if 'Comment' not in reader.fieldnames:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CSV must contain 'Comment' column"
            )
        
        # Extract comments
        comments = []
        for row in reader:
            if row.get('Comment', '').strip():
                comments.append(row['Comment'].strip())
        
        if not comments:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid comments found in CSV"
            )
        
        # Make batch predictions
        predictions = ml_service.predict_batch(comments)
        
        # Save to history
        for pred in predictions:
            history = PredictionHistory(
                user_id=current_user.id,
                product_name=product_name,
                comment=pred['text'],
                predicted_rating=pred['rating'],
                confidence_score=pred['confidence'],
                prediction_type='batch'
            )
            db.add(history)
        db.commit()
        
        # Calculate rating distribution
        ratings = [p['rating'] for p in predictions]
        distribution = viz_service.calculate_rating_distribution(ratings)
        
        # Generate word cloud
        wordcloud_filename = f"wordcloud_{current_user.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        wordcloud_url = viz_service.generate_wordcloud(comments, wordcloud_filename)
        
        # Prepare results for CSV download
        results = []
        for pred in predictions:
            results.append({
                'Comment': pred['text'],
                'Predicted_Rating': pred['rating'],
                'Confidence': pred['confidence']
            })
        
        # Generate PDF report
        pdf_filename = f"report_{current_user.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf_content = report_service.generate_pdf_report(
            predictions=predictions,
            distribution=distribution,
            wordcloud_path=wordcloud_url,
            username=current_user.username,
            filename=pdf_filename
        )
        
        return {
            "total_predictions": len(predictions),
            "rating_distribution": distribution,
            "wordcloud_url": wordcloud_url,
            "results": results,
            "csv_download_url": f"/api/predict/download/{current_user.id}/{datetime.now().timestamp()}",
            "pdf_download_url": f"/api/predict/download-pdf/{current_user.id}/{datetime.now().timestamp()}"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file: {str(e)}"
        )


@router.get("/history", response_model=List[PredictionHistoryResponse])
async def get_prediction_history(
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get prediction history for current user
    
    - **limit**: Maximum number of records to return (default: 50)
    """
    history = db.query(PredictionHistory).filter(
        PredictionHistory.user_id == current_user.id
    ).order_by(PredictionHistory.created_at.desc()).limit(limit).all()
    
    return history


@router.post("/download-csv")
async def download_predictions_csv(
    results: List[dict],
    current_user: User = Depends(get_current_user)
):
    """
    Download prediction results as CSV
    """
    # Create CSV in memory
    output = io.StringIO()
    
    if results:
        fieldnames = results[0].keys()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    # Reset position
    output.seek(0)
    
    # Return as streaming response
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        }
    )


@router.post("/download-pdf")
async def download_predictions_pdf(
    request: PDFReportRequest,
    current_user: User = Depends(get_current_user),
    report_service: ReportService = Depends(get_report_service)
):
    """
    Download prediction results as PDF report
    """
    try:
        pdf_content = report_service.generate_pdf_report(
            predictions=request.predictions,
            distribution=request.distribution,
            wordcloud_path=request.wordcloud_path,
            username=current_user.username
        )
        
        return StreamingResponse(
            io.BytesIO(pdf_content),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=predictions_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating PDF: {str(e)}"
        )
