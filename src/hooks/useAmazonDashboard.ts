import { useEffect, useRef, useState } from 'react';

interface SupplyChainAlert {
  alert_id: string;
  alert_type: string;
  severity: string;
  title: string;
  description: string;
  affected_items: string[];
  affected_suppliers: string[];
  timestamp: string;
  estimated_impact: string;
  recommended_actions: string[];
  status: string;
  priority_score: number;
}

interface DashboardMetrics {
  total_items: number;
  low_stock_items: number;
  out_of_stock_items: number;
  active_alerts: number;
  critical_alerts: number;
  on_time_deliveries: number;
  supplier_performance: number;
  inventory_value: number;
  cost_savings: number;
}

interface DashboardData {
  metrics: DashboardMetrics;
  active_alerts: SupplyChainAlert[];
  alert_history: SupplyChainAlert[];
}

export const useAmazonDashboard = (url: string = 'ws://localhost:8765') => {
  const [isConnected, setIsConnected] = useState(false);
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [alerts, setAlerts] = useState<SupplyChainAlert[]>([]);
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const connect = () => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return;

    try {
      wsRef.current = new WebSocket(url);
      
      wsRef.current.onopen = () => {
        console.log('🏪 Connected to Amazon-style dashboard');
        setIsConnected(true);
        if (reconnectTimeoutRef.current) {
          clearTimeout(reconnectTimeoutRef.current);
          reconnectTimeoutRef.current = null;
        }
        
        // Request initial dashboard data
        sendMessage({ type: 'get_dashboard_data' });
      };

      wsRef.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          
          if (data.type === 'dashboard_data') {
            setDashboardData(data.data);
            setAlerts(data.data.active_alerts || []);
            setMetrics(data.data.metrics);
          } else if (data.type === 'supply_chain_alert') {
            const alert = data.alert;
            setAlerts(prev => [alert, ...prev]);
          } else if (data.type === 'dashboard_metrics') {
            setMetrics(data.metrics);
          } else if (data.type === 'alert_acknowledged') {
            console.log(`Alert ${data.alert_id} acknowledged: ${data.success}`);
          } else if (data.type === 'alert_resolved') {
            console.log(`Alert ${data.alert_id} resolved: ${data.success}`);
            // Remove resolved alert from active alerts
            setAlerts(prev => prev.filter(alert => alert.alert_id !== data.alert_id));
          }
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      wsRef.current.onclose = () => {
        console.log('🏪 Disconnected from dashboard');
        setIsConnected(false);
        
        // Auto-reconnect after 3 seconds
        reconnectTimeoutRef.current = setTimeout(() => {
          console.log('🏪 Attempting to reconnect...');
          connect();
        }, 3000);
      };

      wsRef.current.onerror = (error) => {
        console.error('WebSocket error:', error);
        setIsConnected(false);
      };

    } catch (error) {
      console.error('Failed to connect to WebSocket:', error);
      setIsConnected(false);
    }
  };

  const disconnect = () => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }
    
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
    setIsConnected(false);
  };

  const sendMessage = (message: any) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message));
    } else {
      console.warn('WebSocket not connected');
    }
  };

  const acknowledgeAlert = (alertId: string) => {
    sendMessage({
      type: 'acknowledge_alert',
      alert_id: alertId
    });
  };

  const resolveAlert = (alertId: string) => {
    sendMessage({
      type: 'resolve_alert',
      alert_id: alertId
    });
  };

  const getDashboardData = () => {
    sendMessage({ type: 'get_dashboard_data' });
  };

  useEffect(() => {
    connect();
    
    return () => {
      disconnect();
    };
  }, [url]);

  return {
    isConnected,
    dashboardData,
    alerts,
    metrics,
    connect,
    disconnect,
    sendMessage,
    acknowledgeAlert,
    resolveAlert,
    getDashboardData
  };
};
