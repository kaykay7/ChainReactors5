"""
📈 DEMAND FORECASTING AGENT
Specialized agent for demand prediction, trend analysis, and forecasting models.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
import statistics
from .csv_data_source import CSVDataSource

class ForecastingAgent:
    """Specialized agent for demand forecasting and trend analysis."""
    
    def __init__(self, agent_id: str = "forecasting_agent", memory_manager=None, csv_data_source=None):
        self.agent_id = agent_id
        self.memory_manager = memory_manager
        self.csv_data_source = csv_data_source or CSVDataSource()
        self.capabilities = [
            "demand_forecasting",
            "trend_analysis",
            "seasonal_pattern_detection",
            "anomaly_detection",
            "forecast_accuracy_measurement",
            "scenario_planning"
        ]
    
    def forecast_demand(self, historical_data: List[Dict], forecast_periods: int = 30) -> Dict[str, Any]:
        """Generate demand forecasts using multiple methods."""
        forecasts = {}
        
        for item in historical_data:
            item_id = item.get('id')
            demand_history = item.get('historical_demand', [])
            
            if len(demand_history) < 3:
                continue
            
            # Simple Moving Average
            sma_forecast = self._simple_moving_average(demand_history, forecast_periods)
            
            # Exponential Smoothing
            es_forecast = self._exponential_smoothing(demand_history, forecast_periods)
            
            # Trend Analysis
            trend_forecast = self._trend_analysis(demand_history, forecast_periods)
            
            # Seasonal Adjustment (if enough data)
            seasonal_forecast = self._seasonal_adjustment(demand_history, forecast_periods)
            
            # Ensemble forecast (weighted average)
            ensemble_forecast = self._ensemble_forecast([
                sma_forecast, es_forecast, trend_forecast, seasonal_forecast
            ])
            
            forecasts[item_id] = {
                "item_name": item.get('name'),
                "forecast_periods": forecast_periods,
                "methods": {
                    "simple_moving_average": sma_forecast,
                    "exponential_smoothing": es_forecast,
                    "trend_analysis": trend_forecast,
                    "seasonal_adjustment": seasonal_forecast,
                    "ensemble": ensemble_forecast
                },
                "confidence": self._calculate_confidence(demand_history),
                "trend": self._detect_trend(demand_history),
                "seasonality": self._detect_seasonality(demand_history)
            }
        
        return {"demand_forecasts": forecasts}
    
    def detect_anomalies(self, demand_data: List[Dict]) -> Dict[str, Any]:
        """Detect anomalous demand patterns."""
        anomalies = []
        
        for item in demand_data:
            demand_history = item.get('historical_demand', [])
            if len(demand_history) < 5:
                continue
            
            # Statistical anomaly detection
            mean_demand = statistics.mean(demand_history)
            std_demand = statistics.stdev(demand_history) if len(demand_history) > 1 else 0
            
            for i, demand in enumerate(demand_history):
                z_score = abs((demand - mean_demand) / std_demand) if std_demand > 0 else 0
                
                if z_score > 2:  # 2 standard deviations
                    anomalies.append({
                        "item_id": item.get('id'),
                        "item_name": item.get('name'),
                        "period": i,
                        "actual_demand": demand,
                        "expected_demand": mean_demand,
                        "z_score": z_score,
                        "severity": "high" if z_score > 3 else "medium"
                    })
        
        return {"anomalies": anomalies}
    
    def analyze_seasonal_patterns(self, demand_data: List[Dict]) -> Dict[str, Any]:
        """Analyze seasonal patterns in demand."""
        seasonal_analysis = {}
        
        for item in demand_data:
            demand_history = item.get('historical_demand', [])
            if len(demand_history) < 12:  # Need at least a year of monthly data
                continue
            
            # Calculate seasonal indices
            seasonal_indices = self._calculate_seasonal_indices(demand_history)
            
            seasonal_analysis[item.get('id')] = {
                "item_name": item.get('name'),
                "seasonal_indices": seasonal_indices,
                "peak_season": max(seasonal_indices, key=seasonal_indices.get),
                "low_season": min(seasonal_indices, key=seasonal_indices.get),
                "seasonality_strength": self._calculate_seasonality_strength(seasonal_indices)
            }
        
        return {"seasonal_patterns": seasonal_analysis}
    
    def scenario_planning(self, base_forecast: Dict, scenarios: List[str]) -> Dict[str, Any]:
        """Generate scenario-based forecasts."""
        scenario_forecasts = {}
        
        for scenario in scenarios:
            if scenario == "optimistic":
                multiplier = 1.2
            elif scenario == "pessimistic":
                multiplier = 0.8
            elif scenario == "worst_case":
                multiplier = 0.6
            else:
                multiplier = 1.0
            
            scenario_forecasts[scenario] = {
                "multiplier": multiplier,
                "forecast": {k: v * multiplier for k, v in base_forecast.items()},
                "description": f"{scenario.title()} scenario with {multiplier}x demand"
            }
        
        return {"scenario_forecasts": scenario_forecasts}
    
    def _simple_moving_average(self, data: List[float], periods: int) -> List[float]:
        """Calculate simple moving average forecast."""
        if len(data) < 3:
            return [data[-1]] * periods if data else [0] * periods
        
        window_size = min(3, len(data))
        recent_avg = sum(data[-window_size:]) / window_size
        return [recent_avg] * periods
    
    def _exponential_smoothing(self, data: List[float], periods: int, alpha: float = 0.3) -> List[float]:
        """Calculate exponential smoothing forecast."""
        if not data:
            return [0] * periods
        
        forecast = [data[0]]
        for i in range(1, len(data)):
            forecast.append(alpha * data[i] + (1 - alpha) * forecast[i-1])
        
        # Extend forecast
        last_forecast = forecast[-1]
        return [last_forecast] * periods
    
    def _trend_analysis(self, data: List[float], periods: int) -> List[float]:
        """Calculate trend-based forecast."""
        if len(data) < 2:
            return [data[-1]] * periods if data else [0] * periods
        
        # Simple linear trend
        n = len(data)
        x = list(range(n))
        y = data
        
        # Calculate slope
        slope = self._calculate_slope(x, y)
        
        # Forecast future values
        forecast = []
        for i in range(periods):
            future_x = n + i
            future_y = data[-1] + slope * (i + 1)
            forecast.append(max(0, future_y))  # Demand can't be negative
        
        return forecast
    
    def _seasonal_adjustment(self, data: List[float], periods: int) -> List[float]:
        """Calculate seasonally adjusted forecast."""
        if len(data) < 12:  # Need at least a year of data
            return self._simple_moving_average(data, periods)
        
        # Simple seasonal adjustment
        seasonal_indices = self._calculate_seasonal_indices(data)
        base_forecast = self._simple_moving_average(data, periods)
        
        # Apply seasonal adjustment
        adjusted_forecast = []
        for i, base_value in enumerate(base_forecast):
            seasonal_index = seasonal_indices.get(i % 12, 1.0)
            adjusted_forecast.append(base_value * seasonal_index)
        
        return adjusted_forecast
    
    def _ensemble_forecast(self, forecasts: List[List[float]]) -> List[float]:
        """Combine multiple forecasts using weighted average."""
        if not forecasts:
            return [0] * 30
        
        # Simple equal weighting
        weights = [0.3, 0.3, 0.2, 0.2]  # Adjust based on method performance
        ensemble = []
        
        for i in range(len(forecasts[0])):
            weighted_sum = sum(forecast[i] * weight for forecast, weight in zip(forecasts, weights))
            ensemble.append(weighted_sum)
        
        return ensemble
    
    def _calculate_confidence(self, data: List[float]) -> str:
        """Calculate forecast confidence based on data quality."""
        if len(data) < 10:
            return "low"
        elif len(data) < 30:
            return "medium"
        else:
            return "high"
    
    def _detect_trend(self, data: List[float]) -> str:
        """Detect trend direction."""
        if len(data) < 3:
            return "insufficient_data"
        
        recent_avg = sum(data[-3:]) / 3
        earlier_avg = sum(data[:3]) / 3
        
        if recent_avg > earlier_avg * 1.1:
            return "increasing"
        elif recent_avg < earlier_avg * 0.9:
            return "decreasing"
        else:
            return "stable"
    
    def _detect_seasonality(self, data: List[float]) -> bool:
        """Detect if data has seasonal patterns."""
        if len(data) < 12:
            return False
        
        # Simple seasonality test
        seasonal_indices = self._calculate_seasonal_indices(data)
        max_index = max(seasonal_indices.values())
        min_index = min(seasonal_indices.values())
        
        return (max_index - min_index) > 0.3  # 30% variation indicates seasonality
    
    def _calculate_seasonal_indices(self, data: List[float]) -> Dict[int, float]:
        """Calculate seasonal indices for monthly data."""
        if len(data) < 12:
            return {i: 1.0 for i in range(12)}
        
        # Group by month
        monthly_data = {i: [] for i in range(12)}
        for i, value in enumerate(data):
            month = i % 12
            monthly_data[month].append(value)
        
        # Calculate average for each month
        monthly_avg = {}
        overall_avg = sum(data) / len(data)
        
        for month, values in monthly_data.items():
            if values:
                monthly_avg[month] = sum(values) / len(values)
            else:
                monthly_avg[month] = overall_avg
        
        # Calculate seasonal indices
        seasonal_indices = {}
        for month, avg in monthly_avg.items():
            seasonal_indices[month] = avg / overall_avg if overall_avg > 0 else 1.0
        
        return seasonal_indices
    
    def _calculate_seasonality_strength(self, seasonal_indices: Dict[int, float]) -> str:
        """Calculate strength of seasonality."""
        max_index = max(seasonal_indices.values())
        min_index = min(seasonal_indices.values())
        variation = max_index - min_index
        
        if variation > 0.5:
            return "strong"
        elif variation > 0.2:
            return "moderate"
        else:
            return "weak"
    
    def _calculate_slope(self, x: List[int], y: List[float]) -> float:
        """Calculate slope of linear regression."""
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_x2 = sum(xi * xi for xi in x)
        
        return (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
    
    def collaborate_with_inventory_agent(self, forecast_data: Dict) -> Dict[str, Any]:
        """Send forecast data to inventory agent for reorder point calculations."""
        return {
            "request_type": "update_forecast_data",
            "target_agent": "inventory_agent",
            "data": forecast_data,
            "request_id": f"forecasting_{datetime.now().isoformat()}"
        }
