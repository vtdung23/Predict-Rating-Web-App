"""
ML Prediction Service with LAZY LOADING
Model loads on first request to reduce memory usage on startup
"""
import os
from typing import List, Dict, Any, Optional

# Only set HF cache for local development
if not os.getenv("RENDER"):
    os.environ['HF_HOME'] = 'G:/huggingface_cache'

class MLPredictionService:
    """
    ML Service with lazy loading to avoid Out of Memory errors on Render Free Tier
    Model loads on first prediction request instead of on startup
    """

    def __init__(self):
        """Initialize service without loading model (lazy loading)"""
        # Model components (loaded on first request)
        self.model: Optional[Any] = None
        self.tokenizer: Optional[Any] = None
        self.device: Optional[str] = None
        self.model_loaded = False
        
        # Paths to model files
        CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.TOKENIZER_DIR = os.path.join(CURRENT_DIR, "Model", "phoBERT_multi_class_tokenizer")
        self.WEIGHT_PATH = os.path.join(CURRENT_DIR, "Model", "best_phoBER.pth")
        
        print("✅ ML Service initialized (model will load on first request)")
    
    def _load_model(self):
        """Load model and tokenizer (called on first request)"""
        if self.model_loaded:
            return
        
        print("🔄 Loading ML model (first request)...")
        
        # Import heavy dependencies only when needed
        import torch
        from transformers import AutoTokenizer, RobertaForSequenceClassification
        
        # Determine device
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"📍 Using device: {self.device}")
        
        # Load tokenizer
        print("📦 Loading tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.TOKENIZER_DIR, use_fast=False)
        
        # Load model architecture
        print("🧠 Loading PhoBERT model...")
        self.model = RobertaForSequenceClassification.from_pretrained(
            "vinai/phobert-base",
            num_labels=5,
            problem_type="single_label_classification"
        )
        
        # Load fine-tuned weights
        print("⚙️ Loading trained weights...")
        state_dict = torch.load(self.WEIGHT_PATH, map_location=self.device, weights_only=False)
        self.model.load_state_dict(state_dict)
        
        # Set to evaluation mode and move to device
        self.model.eval()
        self.model.to(self.device)
        
        self.model_loaded = True
        print("✅ Model loaded successfully!")
            
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
        # Lazy load model on first request
        self._load_model()
        
        # Import torch here (already loaded in _load_model)
        import torch
        import torch.nn.functional as F

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
        
        # Move tensors to device (CPU or CUDA)
        encoded = {k: v.to(self.device) for k, v in encoded.items()}

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
        # Import underthesea only when needed
        from underthesea import word_tokenize
        
        # Vietnamese word tokenization
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
