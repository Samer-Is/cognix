"""
Sentiment Analysis Service
Analyzes text sentiment using simple lexicon-based approach
"""

from typing import Dict, List, Any
import re
from collections import Counter


class SentimentAnalyzer:
    """
    Lightweight sentiment analyzer for customer feedback, reviews, etc.
    """
    
    # Simple sentiment lexicons
    POSITIVE_WORDS = {
        'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love',
        'best', 'perfect', 'awesome', 'outstanding', 'superb', 'happy', 'satisfied',
        'pleased', 'delighted', 'impressed', 'recommend', 'thank', 'thanks'
    }
    
    NEGATIVE_WORDS = {
        'bad', 'terrible', 'awful', 'horrible', 'poor', 'worst', 'hate', 'disappointing',
        'disappointed', 'unhappy', 'unsatisfied', 'frustrated', 'angry', 'annoyed',
        'problem', 'issue', 'broken', 'failed', 'waste', 'never', 'refund'
    }
    
    @staticmethod
    def analyze_text(text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of a single text
        
        Returns:
            dict with sentiment score, label, and details
        """
        if not text:
            return {
                "score": 0.0,
                "label": "neutral",
                "confidence": 0.0
            }
        
        # Normalize text
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        # Count sentiment words
        positive_count = sum(1 for word in words if word in SentimentAnalyzer.POSITIVE_WORDS)
        negative_count = sum(1 for word in words if word in SentimentAnalyzer.NEGATIVE_WORDS)
        
        # Calculate score (-1 to 1)
        total_sentiment_words = positive_count + negative_count
        if total_sentiment_words == 0:
            score = 0.0
            confidence = 0.0
        else:
            score = (positive_count - negative_count) / len(words) if len(words) > 0 else 0.0
            confidence = min(total_sentiment_words / len(words) * 2, 1.0) if len(words) > 0 else 0.0
        
        # Determine label
        if score > 0.05:
            label = "positive"
        elif score < -0.05:
            label = "negative"
        else:
            label = "neutral"
        
        return {
            "score": round(score, 3),
            "label": label,
            "confidence": round(confidence, 3),
            "positive_words": positive_count,
            "negative_words": negative_count,
            "total_words": len(words)
        }
    
    @staticmethod
    def analyze_bulk(texts: List[str]) -> Dict[str, Any]:
        """
        Analyze sentiment for multiple texts
        
        Returns:
            Aggregated sentiment statistics
        """
        if not texts:
            return {
                "error": "No texts provided",
                "count": 0
            }
        
        results = [SentimentAnalyzer.analyze_text(text) for text in texts]
        
        # Aggregate statistics
        positive = sum(1 for r in results if r['label'] == 'positive')
        negative = sum(1 for r in results if r['label'] == 'negative')
        neutral = sum(1 for r in results if r['label'] == 'neutral')
        
        avg_score = sum(r['score'] for r in results) / len(results)
        avg_confidence = sum(r['confidence'] for r in results) / len(results)
        
        return {
            "total_texts": len(texts),
            "positive": positive,
            "negative": negative,
            "neutral": neutral,
            "positive_percentage": round(positive / len(texts) * 100, 1),
            "negative_percentage": round(negative / len(texts) * 100, 1),
            "neutral_percentage": round(neutral / len(texts) * 100, 1),
            "average_score": round(avg_score, 3),
            "average_confidence": round(avg_confidence, 3),
            "sentiment_distribution": {
                "positive": positive,
                "negative": negative,
                "neutral": neutral
            }
        }
    
    @staticmethod
    def analyze_dataframe_column(data: List[Dict[str, Any]], text_column: str) -> Dict[str, Any]:
        """
        Analyze sentiment for a specific column in dataset
        """
        if not data or text_column not in data[0]:
            return {"error": f"Column '{text_column}' not found"}
        
        texts = [str(row.get(text_column, "")) for row in data if row.get(text_column)]
        
        if not texts:
            return {"error": "No text data found"}
        
        bulk_analysis = SentimentAnalyzer.analyze_bulk(texts)
        
        # Add column-specific info
        bulk_analysis["analyzed_column"] = text_column
        bulk_analysis["rows_analyzed"] = len(texts)
        
        return bulk_analysis
