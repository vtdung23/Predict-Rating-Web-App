"""
ML Prediction Service
This is a DUMMY service - replace with your real model
"""
import random
from typing import List, Dict, Any
import torch
from transformers import AutoTokenizer, RobertaForSequenceClassification
from underthesea import word_tokenize
import torch.nn.functional as F

class MLPredictionService:

    def __init__(self):
        import os
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_loaded = True

        # Resolve absolute base path of this file (ml_service.py)
        CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

        # Paths to tokenizer directory and model weights
        TOKENIZER_DIR = os.path.join(CURRENT_DIR, "Model", "phoBERT_multi_class_tokenizer")
        WEIGHT_PATH = os.path.join(CURRENT_DIR, "Model", "best_phoBER.pth")

        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_DIR, use_fast=False)

        # Load base PhoBERT architecture with 5 classes
        self.model = RobertaForSequenceClassification.from_pretrained(
            "vinai/phobert-base",
            num_labels=5,
            problem_type="single_label_classification"
        )

        # Load your fine-tuned weights
        state_dict = torch.load(WEIGHT_PATH, map_location=device)
        self.model.load_state_dict(state_dict)

        self.model.eval()
            
    def predict_single(self, text: str) -> Dict[str, Any]:
        """
        Predict rating for a single comment
        
        Args:
            text: Vietnamese product comment
            
        Returns:
            dict: {
                'rating': int (1-5),
                'confidence': float (0-1)
            }
        """

        # 1. Vietnamese preprocessing
        processed_text = self.preprocess(text)

        # 2. Tokenize
        encoded = self.tokenizer(
            processed_text,
            padding=True,
            truncation=True,
            max_length=256,
            return_tensors="pt"
        )

        # 3. Inference
        with torch.no_grad():
            outputs = self.model(**encoded)
            logits = outputs.logits
            probs = F.softmax(logits, dim=1)

        # 4. Get prediction + confidence
        predicted_class = torch.argmax(probs, dim=1).item()
        confidence = probs[0][predicted_class].item()

        # 5. Convert 0-based label → rating 1-5
        rating = predicted_class + 1

        return {
            'rating': rating,
            'confidence': confidence
        }
    
    def predict_batch(self, texts: List[str]) -> List[Dict[str, any]]:
        """
        Predict ratings for multiple comments
        
        Args:
            texts: List of Vietnamese product comments
            
        Returns:
            list: List of prediction dictionaries
        """
        # DUMMY BATCH PREDICTION
        results = []
        for text in texts:
            prediction = self.predict_single(text)
            results.append({
                'text': text,
                'rating': prediction['rating'],
                'confidence': prediction['confidence']
            })
        
        return results
    
    def preprocess(self, text: str) -> str:
        """
        Preprocess Vietnamese text
        TODO: Implement your preprocessing pipeline
        """
        # Example preprocessing:
        # - Remove special characters
        # - Normalize Vietnamese characters
        # - Tokenization
        text = word_tokenize(text, format="text")

        return text
    
    def postprocess(self, prediction: any) -> int:
        """
        Convert model output to rating (1-5)
        TODO: Implement your postprocessing logic
        """
        # Example: Convert probability distribution to class
        return int(prediction)


# Singleton instance
ml_service = MLPredictionService()


def get_ml_service() -> MLPredictionService:
    """Dependency to get ML service"""
    return ml_service
