"use client";

import { useCoAgent, useCopilotAction } from "@copilotkit/react-core";
import { CopilotKitCSSProperties, CopilotChat, CopilotPopup } from "@copilotkit/react-ui";
import { useCallback, useEffect, useRef, useState } from "react";
import type React from "react";
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Progress } from "@/components/ui/progress"
import { useStreaming } from "@/hooks/useStreaming";
import { useMediaQuery } from "@/hooks/use-media-query";
import { cn } from "@/lib/utils";
import type { AgentState } from "@/lib/canvas/types";
import { initialState, isNonEmptyAgentState } from "@/lib/canvas/state";
import { 
  AlertTriangle, 
  Package, 
  Truck, 
  TrendingUp, 
  DollarSign, 
  Clock, 
  CheckCircle, 
  XCircle,
  Bell,
  Activity,
  BarChart3,
  ShoppingCart,
  Users,
  Zap
} from "lucide-react";

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

export default function AmazonDashboard() {
  const { state, setState } = useCoAgent<AgentState>({
    name: "sample_agent",
    initialState,
  });
  
  // Mock order server integration
  const [isConnected, setIsConnected] = useState(false);
  const [orders, setOrders] = useState<any[]>([]);
  
  // Dashboard state
  const [metrics, setMetrics] = useState<DashboardMetrics>({
    total_items: 0,
    low_stock_items: 0,
    out_of_stock_items: 0,
    active_alerts: 0,
    critical_alerts: 0,
    on_time_deliveries: 0,
    supplier_performance: 0,
    inventory_value: 0,
    cost_savings: 0
  });
  
  const [alerts, setAlerts] = useState<SupplyChainAlert[]>([]);
  const [alertHistory, setAlertHistory] = useState<SupplyChainAlert[]>([]);
  const [selectedAlert, setSelectedAlert] = useState<SupplyChainAlert | null>(null);
  
  const isDesktop = useMediaQuery("(min-width: 768px)");

  // Fetch mock orders from the server
  const fetchMockOrders = async () => {
    try {
      const response = await fetch('http://localhost:8765/api/orders/batch');
      const data = await response.json();
      
      if (data.success) {
        console.log('📦 Fetched orders from mock server:', data.data.orders);
        setOrders(prev => [...prev, ...data.data.orders]);
        setIsConnected(true);
        
        // Generate alerts based on orders
        data.data.orders.forEach((order: any) => {
          if (order.priority === 'urgent' || order.priority === 'critical') {
            const alert: SupplyChainAlert = {
              alert_id: `alert_${order.id}`,
              alert_type: order.priority === 'urgent' ? 'rush_order' : 'critical_order',
              severity: order.priority === 'urgent' ? 'high' : 'critical',
              title: `${order.priority.toUpperCase()} Order: ${order.id}`,
              description: `${order.supplier} - ${order.products.join(', ')} - ${order.notes}`,
              affected_items: order.products,
              affected_suppliers: [order.supplier],
              timestamp: order.created_at,
              estimated_impact: `$${order.total_amount} order value`,
              recommended_actions: [
                'Expedite processing',
                'Notify stakeholders',
                'Monitor delivery status'
              ],
              status: 'active',
              priority_score: order.priority === 'urgent' ? 85 : 95
            };
            
            setAlerts(prev => [alert, ...prev]);
            setAlertHistory(prev => [alert, ...prev]);
          }
        });
        
        // Update metrics based on orders
        setMetrics(prev => ({
          ...prev,
          total_items: prev.total_items + data.data.orders.length,
          low_stock_items: prev.low_stock_items + (data.data.orders.filter((o: any) => o.status === 'delayed').length),
          active_alerts: alerts.length + data.data.orders.filter((o: any) => o.priority === 'urgent' || o.priority === 'critical').length,
          critical_alerts: prev.critical_alerts + data.data.orders.filter((o: any) => o.priority === 'critical').length,
          inventory_value: prev.inventory_value + data.data.orders.reduce((sum: number, o: any) => sum + o.total_amount, 0)
        }));
      }
    } catch (error) {
      console.error('Failed to fetch mock orders:', error);
      setIsConnected(false);
    }
  };

  // Poll for new orders every 5 seconds
  useEffect(() => {
    const interval = setInterval(fetchMockOrders, 5000);
    
    // Fetch initial orders
    fetchMockOrders();
    
    return () => clearInterval(interval);
  }, []);

  // CopilotKit actions for dashboard management
  useCopilotAction({
    name: "acknowledgeAlert",
    description: "Acknowledge a supply chain alert.",
    parameters: [
      { name: "alertId", type: "string", required: true, description: "Alert ID to acknowledge." },
    ],
    handler: ({ alertId }: { alertId: string }) => {
      setAlerts(prev => prev.filter(alert => alert.alert_id !== alertId));
      return `Acknowledged alert ${alertId}`;
    },
  });

  useCopilotAction({
    name: "resolveAlert",
    description: "Resolve a supply chain alert.",
    parameters: [
      { name: "alertId", type: "string", required: true, description: "Alert ID to resolve." },
    ],
    handler: ({ alertId }: { alertId: string }) => {
      setAlerts(prev => prev.filter(alert => alert.alert_id !== alertId));
      return `Resolved alert ${alertId}`;
    },
  });

  useCopilotAction({
    name: "getDashboardData",
    description: "Get current dashboard data and metrics.",
    parameters: [],
    handler: () => {
      fetchMockOrders();
      return "Fetching dashboard data...";
    },
  });

  useCopilotAction({
    name: "fetchNewOrders",
    description: "Fetch new mock orders from the server.",
    parameters: [],
    handler: () => {
      fetchMockOrders();
      return "Fetching new orders...";
    },
  });

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'bg-red-500';
      case 'high': return 'bg-orange-500';
      case 'medium': return 'bg-yellow-500';
      case 'low': return 'bg-green-500';
      default: return 'bg-gray-500';
    }
  };

  const getAlertTypeIcon = (alertType: string) => {
    switch (alertType) {
      case 'low_stock': return <Package className="h-4 w-4" />;
      case 'shipping_delay': return <Truck className="h-4 w-4" />;
      case 'supplier_issue': return <Users className="h-4 w-4" />;
      case 'demand_surge': return <TrendingUp className="h-4 w-4" />;
      case 'price_change': return <DollarSign className="h-4 w-4" />;
      default: return <AlertTriangle className="h-4 w-4" />;
    }
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  return (
    <div
      style={{ "--copilot-kit-primary-color": "#2563eb" } as CopilotKitCSSProperties}
      className="h-screen flex flex-col bg-gray-50"
    >
      {/* Header */}
      <div className="bg-white border-b px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <ShoppingCart className="h-5 w-5 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-semibold">Supply Chain Dashboard</h1>
              <p className="text-sm text-gray-600">Real-time monitoring and alerts</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
              <span className="text-sm text-gray-600">
                {isConnected ? 'Live Updates' : 'Disconnected'}
              </span>
            </div>
            <Badge variant="outline" className="flex items-center gap-1">
              <Bell className="h-3 w-3" />
              {metrics.active_alerts} Alerts
            </Badge>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Chat Sidebar */}
        <aside className="max-md:hidden flex flex-col w-80 p-4">
          <div className="h-full flex flex-col bg-white rounded-lg shadow-sm border overflow-hidden">
            <div className="p-4 border-b">
              <h3 className="font-semibold flex items-center gap-2">
                <Activity className="h-4 w-4" />
                AI Assistant
              </h3>
              <p className="text-sm text-gray-600">Real-time supply chain insights</p>
            </div>
            <CopilotChat
              className="flex-1 overflow-auto"
              labels={{
                title: "Supply Chain AI",
                initial: "🏪 I monitor your supply chain in real-time. Ask me about alerts, inventory levels, or supplier performance.",
              }}
              suggestions={[
                {
                  title: "Check Alerts",
                  message: "Show me all active alerts",
                },
                {
                  title: "Inventory Status",
                  message: "What's our current inventory status?",
                },
                {
                  title: "Supplier Performance",
                  message: "How are our suppliers performing?",
                },
                {
                  title: "Cost Analysis",
                  message: "Show me cost savings and value metrics",
                },
              ]}
            />
          </div>
        </aside>

        {/* Dashboard Content */}
        <main className="flex-1 overflow-auto p-6">
          <div className="max-w-7xl mx-auto space-y-6">
            
            {/* Key Metrics Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Items</CardTitle>
                  <Package className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{metrics.total_items}</div>
                  <p className="text-xs text-muted-foreground">
                    +12% from last month
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Low Stock</CardTitle>
                  <AlertTriangle className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-orange-600">{metrics.low_stock_items}</div>
                  <p className="text-xs text-muted-foreground">
                    Items need reordering
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">On-Time Delivery</CardTitle>
                  <Truck className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{metrics.on_time_deliveries.toFixed(1)}%</div>
                  <Progress value={metrics.on_time_deliveries} className="mt-2" />
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Inventory Value</CardTitle>
                  <DollarSign className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{formatCurrency(metrics.inventory_value)}</div>
                  <p className="text-xs text-muted-foreground">
                    Total inventory value
                  </p>
                </CardContent>
              </Card>
            </div>

            {/* Recent Orders Section */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Package className="h-5 w-5" />
                  Recent Orders ({orders.length})
                </CardTitle>
                <CardDescription>
                  Latest orders from mock order server
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3 max-h-64 overflow-y-auto">
                  {orders.slice(0, 10).map((order) => (
                    <div key={order.id} className="flex items-center justify-between p-3 border rounded-lg">
                      <div className="flex-1">
                        <div className="font-medium">{order.id}</div>
                        <div className="text-sm text-gray-600">{order.supplier}</div>
                        <div className="text-xs text-gray-500">{order.products.join(', ')}</div>
                      </div>
                      <div className="text-right">
                        <Badge variant={order.priority === 'urgent' ? 'destructive' : 'secondary'}>
                          {order.priority}
                        </Badge>
                        <div className="text-sm font-medium">${order.total_amount}</div>
                        <div className="text-xs text-gray-500">{order.status}</div>
                      </div>
                    </div>
                  ))}
                  {orders.length === 0 && (
                    <div className="text-center py-8 text-gray-500">
                      <Package className="h-8 w-8 mx-auto mb-2" />
                      <p>No orders yet</p>
                      <p className="text-sm">Orders will appear here as they are generated</p>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Alerts Section */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Active Alerts */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Bell className="h-5 w-5" />
                    Active Alerts ({alerts.length})
                  </CardTitle>
                  <CardDescription>
                    Real-time supply chain notifications
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  {alerts.slice(0, 5).map((alert) => (
                    <Alert key={alert.alert_id} className="cursor-pointer" onClick={() => setSelectedAlert(alert)}>
                      <div className="flex items-start gap-3">
                        <div className={`w-2 h-2 rounded-full mt-2 ${getSeverityColor(alert.severity)}`}></div>
                        <div className="flex-1">
                          <AlertTitle className="flex items-center gap-2">
                            {getAlertTypeIcon(alert.alert_type)}
                            {alert.title}
                          </AlertTitle>
                          <AlertDescription className="mt-1">
                            {alert.description}
                          </AlertDescription>
                          <div className="flex items-center gap-2 mt-2">
                            <Badge variant="outline" className="text-xs">
                              {alert.severity}
                            </Badge>
                            <span className="text-xs text-gray-500">
                              {new Date(alert.timestamp).toLocaleTimeString()}
                            </span>
                          </div>
                        </div>
                      </div>
                    </Alert>
                  ))}
                  {alerts.length === 0 && (
                    <div className="text-center py-8 text-gray-500">
                      <CheckCircle className="h-8 w-8 mx-auto mb-2 text-green-500" />
                      <p>No active alerts</p>
                    </div>
                  )}
                </CardContent>
              </Card>

              {/* Performance Metrics */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <BarChart3 className="h-5 w-5" />
                    Performance Metrics
                  </CardTitle>
                  <CardDescription>
                    Key performance indicators
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>Supplier Performance</span>
                      <span>{metrics.supplier_performance.toFixed(1)}%</span>
                    </div>
                    <Progress value={metrics.supplier_performance} />
                  </div>
                  
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>On-Time Deliveries</span>
                      <span>{metrics.on_time_deliveries.toFixed(1)}%</span>
                    </div>
                    <Progress value={metrics.on_time_deliveries} />
                  </div>

                  <div className="grid grid-cols-2 gap-4 pt-4 border-t">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-green-600">
                        {formatCurrency(metrics.cost_savings)}
                      </div>
                      <p className="text-xs text-gray-600">Cost Savings</p>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-red-600">
                        {metrics.critical_alerts}
                      </div>
                      <p className="text-xs text-gray-600">Critical Alerts</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Alert Details Modal */}
            {selectedAlert && (
              <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
                <Card className="max-w-2xl w-full mx-4">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      {getAlertTypeIcon(selectedAlert.alert_type)}
                      {selectedAlert.title}
                    </CardTitle>
                    <CardDescription>
                      {selectedAlert.description}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="text-sm font-medium">Severity</label>
                        <Badge className={`${getSeverityColor(selectedAlert.severity)} text-white`}>
                          {selectedAlert.severity}
                        </Badge>
                      </div>
                      <div>
                        <label className="text-sm font-medium">Priority Score</label>
                        <div className="text-lg font-semibold">{selectedAlert.priority_score}/100</div>
                      </div>
                    </div>

                    <div>
                      <label className="text-sm font-medium">Estimated Impact</label>
                      <p className="text-sm text-gray-600">{selectedAlert.estimated_impact}</p>
                    </div>

                    <div>
                      <label className="text-sm font-medium">Recommended Actions</label>
                      <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
                        {selectedAlert.recommended_actions.map((action, index) => (
                          <li key={index}>{action}</li>
                        ))}
                      </ul>
                    </div>

                    <div className="flex gap-2 pt-4">
                      <Button 
                        onClick={() => {
                          setAlerts(prev => prev.filter(alert => alert.alert_id !== selectedAlert.alert_id));
                          setSelectedAlert(null);
                        }}
                        variant="outline"
                      >
                        Acknowledge
                      </Button>
                      <Button 
                        onClick={() => {
                          setAlerts(prev => prev.filter(alert => alert.alert_id !== selectedAlert.alert_id));
                          setSelectedAlert(null);
                        }}
                      >
                        Resolve
                      </Button>
                      <Button 
                        variant="outline" 
                        onClick={() => setSelectedAlert(null)}
                      >
                        Close
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </div>
            )}
          </div>
        </main>
      </div>

      {/* Mobile Chat */}
      <div className="md:hidden">
        <CopilotPopup
          labels={{
            title: "Supply Chain AI",
            initial: "🏪 I monitor your supply chain in real-time. Ask me about alerts, inventory levels, or supplier performance.",
          }}
          suggestions={[
            {
              title: "Check Alerts",
              message: "Show me all active alerts",
            },
            {
              title: "Inventory Status",
              message: "What's our current inventory status?",
            },
            {
              title: "Supplier Performance",
              message: "How are our suppliers performing?",
            },
          ]}
        />
      </div>
    </div>
  );
}
