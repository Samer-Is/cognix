"""
Advanced Analytics Engine
Provides predictive analytics, anomaly detection, and statistical analysis
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class AnalyticsEngine:
    """
    Core analytics engine with ML capabilities
    """
    
    @staticmethod
    def detect_anomalies(data: List[Dict[str, Any]], metric_column: str, threshold: float = 2.0) -> Dict[str, Any]:
        """
        Detect anomalies using Z-score method
        """
        if not data or len(data) < 3:
            return {"anomalies": [], "method": "z-score", "threshold": threshold}
        
        try:
            df = pd.DataFrame(data)
            if metric_column not in df.columns:
                return {"error": f"Column '{metric_column}' not found"}
            
            values = pd.to_numeric(df[metric_column], errors='coerce').dropna()
            
            if len(values) < 3:
                return {"anomalies": []}
            
            mean = values.mean()
            std = values.std()
            
            if std == 0:
                return {"anomalies": [], "reason": "No variance in data"}
            
            z_scores = np.abs((values - mean) / std)
            anomaly_indices = np.where(z_scores > threshold)[0].tolist()
            
            anomalies = []
            for idx in anomaly_indices:
                anomalies.append({
                    "index": int(idx),
                    "value": float(values.iloc[idx]),
                    "z_score": float(z_scores.iloc[idx]),
                    "deviation": f"{((values.iloc[idx] - mean) / mean * 100):.1f}%"
                })
            
            return {
                "anomalies": anomalies,
                "total_points": len(values),
                "anomaly_count": len(anomalies),
                "mean": float(mean),
                "std": float(std),
                "threshold": threshold
            }
            
        except Exception as e:
            logger.error(f"Anomaly detection error: {e}")
            return {"error": str(e)}
    
    @staticmethod
    def forecast_trend(data: List[Dict[str, Any]], metric_column: str, periods: int = 7) -> Dict[str, Any]:
        """
        Simple linear regression forecast
        """
        if not data or len(data) < 2:
            return {"error": "Insufficient data for forecasting"}
        
        try:
            df = pd.DataFrame(data)
            if metric_column not in df.columns:
                return {"error": f"Column '{metric_column}' not found"}
            
            values = pd.to_numeric(df[metric_column], errors='coerce').dropna()
            
            if len(values) < 2:
                return {"error": "Insufficient valid data points"}
            
            # Simple linear regression
            x = np.arange(len(values))
            y = values.values
            
            # Calculate slope and intercept
            x_mean = x.mean()
            y_mean = y.mean()
            
            numerator = np.sum((x - x_mean) * (y - y_mean))
            denominator = np.sum((x - x_mean) ** 2)
            
            if denominator == 0:
                return {"error": "Cannot calculate trend"}
            
            slope = numerator / denominator
            intercept = y_mean - slope * x_mean
            
            # Generate forecasts
            future_x = np.arange(len(values), len(values) + periods)
            forecasts = slope * future_x + intercept
            
            # Calculate confidence
            residuals = y - (slope * x + intercept)
            mse = np.mean(residuals ** 2)
            rmse = np.sqrt(mse)
            
            forecast_points = []
            for i, forecast in enumerate(forecasts):
                forecast_points.append({
                    "period": i + 1,
                    "value": float(forecast),
                    "lower_bound": float(forecast - 1.96 * rmse),
                    "upper_bound": float(forecast + 1.96 * rmse)
                })
            
            trend_direction = "increasing" if slope > 0 else "decreasing" if slope < 0 else "stable"
            
            return {
                "forecasts": forecast_points,
                "trend": trend_direction,
                "slope": float(slope),
                "rmse": float(rmse),
                "historical_mean": float(y_mean)
            }
            
        except Exception as e:
            logger.error(f"Forecast error: {e}")
            return {"error": str(e)}
    
    @staticmethod
    def calculate_correlations(data: List[Dict[str, Any]], columns: List[str]) -> Dict[str, Any]:
        """
        Calculate correlation matrix for numeric columns
        """
        if not data or len(columns) < 2:
            return {"error": "Need at least 2 columns for correlation"}
        
        try:
            df = pd.DataFrame(data)
            
            # Select numeric columns
            numeric_df = df[columns].apply(pd.to_numeric, errors='coerce')
            
            if numeric_df.empty:
                return {"error": "No numeric data found"}
            
            corr_matrix = numeric_df.corr()
            
            # Convert to list of correlations
            correlations = []
            for i, col1 in enumerate(columns):
                for j, col2 in enumerate(columns):
                    if i < j:  # Only upper triangle
                        corr_value = corr_matrix.iloc[i, j]
                        if not np.isnan(corr_value):
                            correlations.append({
                                "var1": col1,
                                "var2": col2,
                                "correlation": float(corr_value),
                                "strength": AnalyticsEngine._interpret_correlation(abs(corr_value))
                            })
            
            # Sort by absolute correlation
            correlations.sort(key=lambda x: abs(x['correlation']), reverse=True)
            
            return {
                "correlations": correlations,
                "matrix": corr_matrix.to_dict()
            }
            
        except Exception as e:
            logger.error(f"Correlation error: {e}")
            return {"error": str(e)}
    
    @staticmethod
    def _interpret_correlation(corr: float) -> str:
        """Interpret correlation strength"""
        if corr >= 0.7:
            return "strong"
        elif corr >= 0.4:
            return "moderate"
        elif corr >= 0.2:
            return "weak"
        else:
            return "very weak"
    
    @staticmethod
    def segment_analysis(data: List[Dict[str, Any]], segment_column: str, metric_column: str) -> Dict[str, Any]:
        """
        Analyze metrics by segments
        """
        if not data:
            return {"error": "No data provided"}
        
        try:
            df = pd.DataFrame(data)
            
            if segment_column not in df.columns or metric_column not in df.columns:
                return {"error": "Required columns not found"}
            
            df[metric_column] = pd.to_numeric(df[metric_column], errors='coerce')
            
            segments = []
            for segment_name, group in df.groupby(segment_column):
                values = group[metric_column].dropna()
                
                if len(values) > 0:
                    segments.append({
                        "segment": str(segment_name),
                        "count": int(len(values)),
                        "mean": float(values.mean()),
                        "median": float(values.median()),
                        "std": float(values.std()) if len(values) > 1 else 0,
                        "min": float(values.min()),
                        "max": float(values.max()),
                        "total": float(values.sum())
                    })
            
            # Sort by mean descending
            segments.sort(key=lambda x: x['mean'], reverse=True)
            
            return {
                "segments": segments,
                "total_segments": len(segments)
            }
            
        except Exception as e:
            logger.error(f"Segment analysis error: {e}")
            return {"error": str(e)}
    
    @staticmethod
    def time_series_decomposition(data: List[Dict[str, Any]], date_column: str, value_column: str) -> Dict[str, Any]:
        """
        Decompose time series into trend, seasonality, and residual
        Simple moving average approach
        """
        if not data or len(data) < 7:
            return {"error": "Need at least 7 data points"}
        
        try:
            df = pd.DataFrame(data)
            df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
            df = df.dropna(subset=[date_column])
            df = df.sort_values(date_column)
            
            df[value_column] = pd.to_numeric(df[value_column], errors='coerce')
            values = df[value_column].dropna()
            
            if len(values) < 7:
                return {"error": "Insufficient valid data points"}
            
            # Calculate moving average (trend)
            window = min(7, len(values) // 3)
            trend = values.rolling(window=window, center=True).mean()
            
            # Detrend
            detrended = values - trend
            
            # Simple seasonality (weekly pattern if enough data)
            seasonality = detrended.rolling(window=window).mean()
            
            # Residual
            residual = values - trend - seasonality
            
            return {
                "trend": trend.dropna().tolist()[-10:],
                "seasonality_pattern": "detected" if seasonality.std() > 0 else "none",
                "volatility": float(residual.std()) if len(residual.dropna()) > 0 else 0,
                "trend_direction": "increasing" if trend.dropna().iloc[-1] > trend.dropna().iloc[0] else "decreasing"
            }
            
        except Exception as e:
            logger.error(f"Time series decomposition error: {e}")
            return {"error": str(e)}
