"""
Alert Generation Service
Monitors data for anomalies and generates alerts
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
from services.analytics_engine import AnalyticsEngine

logger = logging.getLogger(__name__)


class AlertService:
    """
    Generate and manage alerts based on data anomalies
    """
    
    @staticmethod
    def generate_anomaly_alerts(
        data: List[Dict[str, Any]],
        metric_column: str,
        threshold: float = 2.0,
        domain: str = "general"
    ) -> List[Dict[str, Any]]:
        """
        Generate alerts from anomaly detection
        """
        
        # Run anomaly detection
        anomaly_result = AnalyticsEngine.detect_anomalies(data, metric_column, threshold)
        
        if "error" in anomaly_result:
            return []
        
        anomalies = anomaly_result.get("anomalies", [])
        
        if not anomalies:
            return []
        
        alerts = []
        for anomaly in anomalies:
            severity = AlertService._calculate_severity(anomaly["z_score"])
            
            alert = {
                "alert_type": "anomaly",
                "domain": domain,
                "title": f"Anomaly Detected in {metric_column}",
                "description": f"Value {anomaly['value']} deviates by {anomaly['deviation']} from expected range",
                "severity": severity,
                "metric_name": metric_column,
                "metric_value": anomaly["value"],
                "threshold_value": threshold,
                "condition": {
                    "type": "z-score",
                    "z_score": anomaly["z_score"],
                    "threshold": threshold
                },
                "is_read": False,
                "is_active": True,
                "created_at": datetime.now()
            }
            alerts.append(alert)
        
        logger.info(f"Generated {len(alerts)} anomaly alerts for {metric_column}")
        return alerts
    
    @staticmethod
    def generate_threshold_alerts(
        data: List[Dict[str, Any]],
        metric_column: str,
        threshold_value: float,
        comparison: str = "greater",  # 'greater', 'less', 'equal'
        domain: str = "general"
    ) -> List[Dict[str, Any]]:
        """
        Generate alerts when metric crosses threshold
        """
        alerts = []
        
        for idx, row in enumerate(data):
            value = row.get(metric_column)
            
            if value is None:
                continue
            
            try:
                value = float(value)
            except (ValueError, TypeError):
                continue
            
            triggered = False
            if comparison == "greater" and value > threshold_value:
                triggered = True
            elif comparison == "less" and value < threshold_value:
                triggered = True
            elif comparison == "equal" and value == threshold_value:
                triggered = True
            
            if triggered:
                severity = "high" if comparison == "greater" and value > threshold_value * 1.5 else "medium"
                
                alert = {
                    "alert_type": "threshold",
                    "domain": domain,
                    "title": f"{metric_column} {comparison} Threshold",
                    "description": f"Value {value} triggered {comparison} threshold of {threshold_value}",
                    "severity": severity,
                    "metric_name": metric_column,
                    "metric_value": value,
                    "threshold_value": threshold_value,
                    "condition": {
                        "type": "threshold",
                        "comparison": comparison,
                        "threshold": threshold_value
                    },
                    "is_read": False,
                    "is_active": True,
                    "created_at": datetime.now()
                }
                alerts.append(alert)
        
        logger.info(f"Generated {len(alerts)} threshold alerts for {metric_column}")
        return alerts
    
    @staticmethod
    def generate_trend_alerts(
        data: List[Dict[str, Any]],
        metric_column: str,
        domain: str = "general"
    ) -> List[Dict[str, Any]]:
        """
        Generate alerts based on trend analysis
        """
        forecast_result = AnalyticsEngine.forecast_trend(data, metric_column, periods=7)
        
        if "error" in forecast_result:
            return []
        
        alerts = []
        
        trend = forecast_result.get("trend", "stable")
        slope = forecast_result.get("slope", 0)
        
        # Alert on significant trends
        if abs(slope) > 0.1:  # Significant trend
            severity = "high" if abs(slope) > 0.5 else "medium"
            
            alert = {
                "alert_type": "trend",
                "domain": domain,
                "title": f"Significant {trend.capitalize()} Trend in {metric_column}",
                "description": f"Detected {trend} trend with slope {slope:.3f}",
                "severity": severity,
                "metric_name": metric_column,
                "metric_value": slope,
                "threshold_value": 0.1,
                "condition": {
                    "type": "trend",
                    "trend_direction": trend,
                    "slope": slope
                },
                "is_read": False,
                "is_active": True,
                "created_at": datetime.now()
            }
            alerts.append(alert)
        
        logger.info(f"Generated {len(alerts)} trend alerts for {metric_column}")
        return alerts
    
    @staticmethod
    def _calculate_severity(z_score: float) -> str:
        """
        Calculate alert severity based on z-score
        """
        abs_z = abs(z_score)
        
        if abs_z > 4:
            return "critical"
        elif abs_z > 3:
            return "high"
        elif abs_z > 2:
            return "medium"
        else:
            return "low"
    
    @staticmethod
    def generate_comprehensive_alerts(
        data: List[Dict[str, Any]],
        metric_column: str,
        domain: str = "general",
        include_anomaly: bool = True,
        include_trend: bool = True
    ) -> Dict[str, Any]:
        """
        Generate all types of alerts for a metric
        """
        all_alerts = []
        
        if include_anomaly:
            anomaly_alerts = AlertService.generate_anomaly_alerts(data, metric_column, domain=domain)
            all_alerts.extend(anomaly_alerts)
        
        if include_trend:
            trend_alerts = AlertService.generate_trend_alerts(data, metric_column, domain=domain)
            all_alerts.extend(trend_alerts)
        
        # Sort by severity
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        all_alerts.sort(key=lambda x: severity_order.get(x["severity"], 4))
        
        return {
            "total_alerts": len(all_alerts),
            "critical": sum(1 for a in all_alerts if a["severity"] == "critical"),
            "high": sum(1 for a in all_alerts if a["severity"] == "high"),
            "medium": sum(1 for a in all_alerts if a["severity"] == "medium"),
            "low": sum(1 for a in all_alerts if a["severity"] == "low"),
            "alerts": all_alerts
        }
