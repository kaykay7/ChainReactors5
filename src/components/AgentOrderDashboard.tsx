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
  Zap,
  Plus,
  RefreshCw
} from "lucide-react";

interface AgentOrder {
  id: string;
  supplier: string;
  products: string[];
  quantity: number;
  total_amount: number;
  currency: string;
  status: string;
  priority: string;
  region: string;
  order_date: string;
  expected_delivery: string;
  tracking_number: string;
  notes: string;
  created_at: string;
  pattern_type: string;
}

interface DashboardMetrics {
  total_orders: number;
  urgent_orders: number;
  critical_orders: number;
  total_value: number;
  products_count: number;
  recent_orders: AgentOrder[];
}

export default function AgentOrderDashboard() {
  const { state, setState } = useCoAgent<AgentState>({
    name: "sample_agent",
    initialState,
  });
  
  // Dashboard state
  const [orders, setOrders] = useState<AgentOrder[]>([]);
  const [metrics, setMetrics] = useState<DashboardMetrics>({
    total_orders: 0,
    urgent_orders: 0,
    critical_orders: 0,
    total_value: 0,
    products_count: 0,
    recent_orders: []
  });
  
  const [alerts, setAlerts] = useState<any[]>([]);
  const [selectedAlert, setSelectedAlert] = useState<any | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  
  const isDesktop = useMediaQuery("(min-width: 768px)");

  // Fetch orders from agent
  const fetchOrdersFromAgent = useCallback(async () => {
    setIsLoading(true);
    try {
      // This will trigger the agent to get orders
      // The agent will respond with order data
      console.log("Fetching orders from agent...");
      
      // Simulate fetching orders (in real implementation, this would come from the agent)
      // For now, we'll generate some sample orders to show the functionality
      const sampleOrders: AgentOrder[] = [
        {
          id: `ORD-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
          supplier: "TechCorp Solutions",
          products: ["High-Speed Microprocessor", "Memory Module 16GB"],
          quantity: 25,
          total_amount: 8250.00,
          currency: "USD",
          status: "processing",
          priority: "urgent",
          region: "North America",
          order_date: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
          expected_delivery: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
          tracking_number: `TRK${Math.floor(Math.random() * 1000000)}`,
          notes: "Urgent order for production line",
          created_at: new Date().toISOString(),
          pattern_type: "urgent_orders"
        }
      ];
      
      setOrders(prev => [...prev, ...sampleOrders]);
      
      // Update metrics
      setMetrics(prev => ({
        ...prev,
        total_orders: prev.total_orders + sampleOrders.length,
        urgent_orders: prev.urgent_orders + sampleOrders.filter(o => o.priority === 'urgent').length,
        total_value: prev.total_value + sampleOrders.reduce((sum, o) => sum + o.total_amount, 0)
      }));
      
    } catch (error) {
      console.error("Failed to fetch orders:", error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Fetch dashboard data from agent
  const fetchDashboardData = useCallback(async () => {
    setIsLoading(true);
    try {
      console.log("Fetching dashboard data from agent...");
    } catch (error) {
      console.error("Failed to fetch dashboard data:", error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // CopilotKit actions for order management
  useCopilotAction({
    name: "generateOrders",
    description: "Generate multiple orders for testing.",
    parameters: [
      { name: "count", type: "number", required: false, description: "Number of orders to generate (default: 5)." },
      { name: "orderType", type: "string", required: false, description: "Type of orders (mixed, urgent, bulk, premium)." }
    ],
    handler: ({ count = 5, orderType = "mixed" }: { count?: number, orderType?: string }) => {
      console.log(`🚀 FRONTEND: Generating ${count} ${orderType} orders...`);
      console.log(`🚀 FRONTEND: Current orders count: ${orders.length}`);
      
      // Generate orders based on the request
      const newOrders: AgentOrder[] = [];
      const suppliers = ["TechCorp Solutions", "Global Parts Inc", "Budget Suppliers Ltd", "Premium Components", "FastTrack Logistics"];
      const products = ["High-Speed Microprocessor", "Memory Module 16GB", "Steel Bracket", "Aluminum Frame", "Power Supply Unit", "Data Cable", "Sensor Module"];
      const priorities = orderType === "urgent" ? ["urgent"] : orderType === "bulk" ? ["medium"] : orderType === "premium" ? ["high"] : ["low", "medium", "high", "urgent"];
      const statuses = ["pending", "confirmed", "processing", "shipped", "delivered"];
      
      for (let i = 0; i < count; i++) {
        const priority = priorities[Math.floor(Math.random() * priorities.length)];
        const supplier = suppliers[Math.floor(Math.random() * suppliers.length)];
        const productCount = Math.floor(Math.random() * 3) + 1;
        const selectedProducts = products.sort(() => 0.5 - Math.random()).slice(0, productCount);
        const quantity = Math.floor(Math.random() * 50) + 1;
        const baseAmount = Math.random() * 5000 + 100;
        const totalAmount = Math.round(baseAmount * 100) / 100;
        
        const order: AgentOrder = {
          id: `ORD-${Date.now()}-${Math.floor(Math.random() * 1000)}-${i}`,
          supplier,
          products: selectedProducts,
          quantity,
          total_amount: totalAmount,
          currency: "USD",
          status: statuses[Math.floor(Math.random() * statuses.length)],
          priority,
          region: ["North America", "Europe", "Asia Pacific", "South America", "Africa"][Math.floor(Math.random() * 5)],
          order_date: new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000).toISOString(),
          expected_delivery: new Date(Date.now() + Math.random() * 14 * 24 * 60 * 60 * 1000).toISOString(),
          tracking_number: `TRK${Math.floor(Math.random() * 1000000)}`,
          notes: `${orderType} order for ${selectedProducts.join(', ')}`,
          created_at: new Date().toISOString(),
          pattern_type: `${orderType}_orders`
        };
        
        newOrders.push(order);
      }
      
      // Add orders to state immediately
      setOrders(prev => {
        const updated = [...prev, ...newOrders];
        console.log(`🚀 FRONTEND: Added ${newOrders.length} orders. Total now: ${updated.length}`);
        return updated;
      });
      
      // Update metrics immediately
      setMetrics(prev => {
        const updated = {
          ...prev,
          total_orders: prev.total_orders + newOrders.length,
          urgent_orders: prev.urgent_orders + newOrders.filter(o => o.priority === 'urgent').length,
          critical_orders: prev.critical_orders + newOrders.filter(o => o.priority === 'critical').length,
          total_value: prev.total_value + newOrders.reduce((sum, o) => sum + o.total_amount, 0)
        };
        console.log(`🚀 FRONTEND: Updated metrics:`, updated);
        return updated;
      });
      
      // Force a re-render by updating a dummy state
      setTimeout(() => {
        setOrders(prev => [...prev]);
        console.log(`🚀 FRONTEND: Force re-render triggered`);
      }, 100);
      
      return `✅ Generated ${count} ${orderType} orders (Total value: $${newOrders.reduce((sum, o) => sum + o.total_amount, 0).toFixed(2)})`;
    },
  });

  useCopilotAction({
    name: "createProduct",
    description: "Create a new product.",
    parameters: [
      { name: "name", type: "string", required: true, description: "Product name." },
      { name: "category", type: "string", required: false, description: "Product category." },
      { name: "basePrice", type: "number", required: false, description: "Base price for the product." }
    ],
    handler: ({ name, category, basePrice }: { name: string, category?: string, basePrice?: number }) => {
      console.log(`Creating product: ${name}`);
      
      // Update products count in metrics
      setMetrics(prev => ({
        ...prev,
        products_count: prev.products_count + 1
      }));
      
      return `✅ Created product: ${name} (${category || 'Electronics'}) - $${basePrice || Math.round(Math.random() * 500 + 10)}`;
    },
  });

  useCopilotAction({
    name: "createOrder",
    description: "Create a new order.",
    parameters: [
      { name: "products", type: "array", required: false, description: "List of product names." },
      { name: "quantity", type: "number", required: false, description: "Order quantity." },
      { name: "priority", type: "string", required: false, description: "Order priority." },
      { name: "supplier", type: "string", required: false, description: "Supplier name." }
    ],
    handler: ({ products, quantity, priority, supplier }: { products?: string[], quantity?: number, priority?: string, supplier?: string }) => {
      console.log(`Creating order for products: ${products?.join(', ')}`);
      
      // Generate a single order
      const orderProducts = products || ["High-Speed Microprocessor", "Memory Module 16GB"];
      const orderQuantity = quantity || Math.floor(Math.random() * 50) + 1;
      const orderPriority = priority || ["low", "medium", "high", "urgent"][Math.floor(Math.random() * 4)];
      const orderSupplier = supplier || ["TechCorp Solutions", "Global Parts Inc", "Budget Suppliers Ltd"][Math.floor(Math.random() * 3)];
      const totalAmount = Math.round((Math.random() * 5000 + 100) * 100) / 100;
      
      const newOrder: AgentOrder = {
        id: `ORD-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
        supplier: orderSupplier,
        products: orderProducts,
        quantity: orderQuantity,
        total_amount: totalAmount,
        currency: "USD",
        status: ["pending", "confirmed", "processing"][Math.floor(Math.random() * 3)],
        priority: orderPriority,
        region: ["North America", "Europe", "Asia Pacific"][Math.floor(Math.random() * 3)],
        order_date: new Date(Date.now() - Math.random() * 24 * 60 * 60 * 1000).toISOString(),
        expected_delivery: new Date(Date.now() + Math.random() * 7 * 24 * 60 * 60 * 1000).toISOString(),
        tracking_number: `TRK${Math.floor(Math.random() * 1000000)}`,
        notes: `Order for ${orderProducts.join(', ')}`,
        created_at: new Date().toISOString(),
        pattern_type: `${orderPriority}_orders`
      };
      
      // Add order to state
      setOrders(prev => [...prev, newOrder]);
      
      // Update metrics
      setMetrics(prev => ({
        ...prev,
        total_orders: prev.total_orders + 1,
        urgent_orders: prev.urgent_orders + (orderPriority === 'urgent' ? 1 : 0),
        critical_orders: prev.critical_orders + (orderPriority === 'critical' ? 1 : 0),
        total_value: prev.total_value + totalAmount
      }));
      
      return `✅ Created order: ${newOrder.id} - ${orderSupplier} - $${totalAmount} (${orderPriority})`;
    },
  });

  useCopilotAction({
    name: "getOrders",
    description: "Get all orders from the system.",
    parameters: [],
    handler: () => {
      console.log("Getting all orders...");
      const orderList = orders.slice(-5).map(order => 
        `• ${order.id}: ${order.supplier} - $${order.total_amount} (${order.priority})`
      ).join('\n');
      return `📋 Recent Orders (${orders.length} total):\n${orderList || 'No orders yet'}`;
    },
  });

  useCopilotAction({
    name: "getProducts",
    description: "Get all products from the system.",
    parameters: [],
    handler: () => {
      console.log("Getting all products...");
      return `📦 Products: ${metrics.products_count} available products in the system`;
    },
  });

  useCopilotAction({
    name: "getDashboardData",
    description: "Get dashboard data and metrics.",
    parameters: [],
    handler: () => {
      console.log("Getting dashboard data...");
      return `📊 Dashboard Data:
• Total Orders: ${metrics.total_orders}
• Urgent Orders: ${metrics.urgent_orders}
• Critical Orders: ${metrics.critical_orders}
• Total Value: $${metrics.total_value.toFixed(2)}
• Products: ${metrics.products_count}`;
    },
  });

  // Load initial data
  useEffect(() => {
    fetchDashboardData();
  }, [fetchDashboardData]);

  // Debug log for orders and metrics
  useEffect(() => {
    console.log(`🚀 FRONTEND: Orders updated: ${orders.length} orders`);
    console.log(`🚀 FRONTEND: Metrics:`, metrics);
  }, [orders, metrics]);

  // Listen for agent responses and update dashboard
  useEffect(() => {
    const handleAgentResponse = (event: any) => {
      if (event.detail && event.detail.type === 'agent_response') {
        const response = event.detail.data;
        console.log('Agent response received:', response);
        
        // Check if response contains order data
        if (response.includes('Generated') && response.includes('orders')) {
          // Extract order count from response
          const match = response.match(/Generated (\d+) (\w+) orders/);
          if (match) {
            const count = parseInt(match[1]);
            const orderType = match[2];
            
            // Generate orders based on agent response
            const newOrders: AgentOrder[] = [];
            const suppliers = ["TechCorp Solutions", "Global Parts Inc", "Budget Suppliers Ltd", "Premium Components", "FastTrack Logistics"];
            const products = ["High-Speed Microprocessor", "Memory Module 16GB", "Steel Bracket", "Aluminum Frame", "Power Supply Unit", "Data Cable", "Sensor Module"];
            const priorities = orderType === "urgent" ? ["urgent"] : orderType === "bulk" ? ["medium"] : orderType === "premium" ? ["high"] : ["low", "medium", "high", "urgent"];
            const statuses = ["pending", "confirmed", "processing", "shipped", "delivered"];
            
            for (let i = 0; i < count; i++) {
              const priority = priorities[Math.floor(Math.random() * priorities.length)];
              const supplier = suppliers[Math.floor(Math.random() * suppliers.length)];
              const productCount = Math.floor(Math.random() * 3) + 1;
              const selectedProducts = products.sort(() => 0.5 - Math.random()).slice(0, productCount);
              const quantity = Math.floor(Math.random() * 50) + 1;
              const baseAmount = Math.random() * 5000 + 100;
              const totalAmount = Math.round(baseAmount * 100) / 100;
              
              const order: AgentOrder = {
                id: `ORD-${Date.now()}-${Math.floor(Math.random() * 1000)}-${i}`,
                supplier,
                products: selectedProducts,
                quantity,
                total_amount: totalAmount,
                currency: "USD",
                status: statuses[Math.floor(Math.random() * statuses.length)],
                priority,
                region: ["North America", "Europe", "Asia Pacific", "South America", "Africa"][Math.floor(Math.random() * 5)],
                order_date: new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000).toISOString(),
                expected_delivery: new Date(Date.now() + Math.random() * 14 * 24 * 60 * 60 * 1000).toISOString(),
                tracking_number: `TRK${Math.floor(Math.random() * 1000000)}`,
                notes: `${orderType} order for ${selectedProducts.join(', ')}`,
                created_at: new Date().toISOString(),
                pattern_type: `${orderType}_orders`
              };
              
              newOrders.push(order);
            }
            
            // Add orders to state
            setOrders(prev => [...prev, ...newOrders]);
            
            // Update metrics
            setMetrics(prev => ({
              ...prev,
              total_orders: prev.total_orders + newOrders.length,
              urgent_orders: prev.urgent_orders + newOrders.filter(o => o.priority === 'urgent').length,
              critical_orders: prev.critical_orders + newOrders.filter(o => o.priority === 'critical').length,
              total_value: prev.total_value + newOrders.reduce((sum, o) => sum + o.total_amount, 0)
            }));
          }
        }
      }
    };

    // Listen for custom events from the agent
    window.addEventListener('agent_response', handleAgentResponse);
    
    return () => {
      window.removeEventListener('agent_response', handleAgentResponse);
    };
  }, []);

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'bg-red-500';
      case 'high': return 'bg-orange-500';
      case 'medium': return 'bg-yellow-500';
      case 'low': return 'bg-green-500';
      default: return 'bg-gray-500';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical': return 'bg-red-500';
      case 'urgent': return 'bg-orange-500';
      case 'high': return 'bg-yellow-500';
      case 'medium': return 'bg-blue-500';
      case 'low': return 'bg-green-500';
      default: return 'bg-gray-500';
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
              <h1 className="text-xl font-semibold">Agent Order Dashboard</h1>
              <p className="text-sm text-gray-600">AI-generated orders and products</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <Button 
              onClick={fetchOrdersFromAgent}
              disabled={isLoading}
              variant="outline" 
              size="sm"
              className="flex items-center gap-2"
            >
              <RefreshCw className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
              Refresh Orders
            </Button>
            <Badge variant="outline" className="flex items-center gap-1">
              <Bell className="h-3 w-3" />
              {alerts.length} Alerts
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
                AI Agent Assistant
              </h3>
              <p className="text-sm text-gray-600">Generate orders and products</p>
            </div>
            <CopilotChat
              className="flex-1 overflow-auto"
              labels={{
                title: "Order Generation AI",
                initial: "🤖 I can generate orders and products for you. Try saying 'generate 5 urgent orders' or 'create a new product called Widget'.",
              }}
              suggestions={[
                {
                  title: "Generate Orders",
                  message: "Generate 5 mixed orders",
                },
                {
                  title: "Create Product",
                  message: "Create a new product called Smart Sensor",
                },
                {
                  title: "Create Order",
                  message: "Create an urgent order for microprocessors",
                },
                {
                  title: "Get Dashboard Data",
                  message: "Show me the dashboard data",
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
                  <CardTitle className="text-sm font-medium">Total Orders</CardTitle>
                  <Package className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{metrics.total_orders}</div>
                  <p className="text-xs text-muted-foreground">
                    Generated by AI agent
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Urgent Orders</CardTitle>
                  <AlertTriangle className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-orange-600">{metrics.urgent_orders}</div>
                  <p className="text-xs text-muted-foreground">
                    High priority orders
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Value</CardTitle>
                  <DollarSign className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{formatCurrency(metrics.total_value)}</div>
                  <p className="text-xs text-muted-foreground">
                    All orders combined
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Products</CardTitle>
                  <TrendingUp className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{metrics.products_count}</div>
                  <p className="text-xs text-muted-foreground">
                    Available products
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
                  Orders generated by AI agent
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
                        <Badge 
                          variant={order.priority === 'urgent' || order.priority === 'critical' ? 'destructive' : 'secondary'}
                          className={cn("text-white", getPriorityColor(order.priority))}
                        >
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
                      <p className="text-sm">Use the chat to generate orders or products</p>
                      <Button 
                        onClick={fetchOrdersFromAgent}
                        className="mt-4"
                        variant="outline"
                        size="sm"
                      >
                        <Plus className="h-4 w-4 mr-2" />
                        Generate Orders
                      </Button>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Quick Actions */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Zap className="h-5 w-5" />
                  Quick Actions
                </CardTitle>
                <CardDescription>
                  Generate orders and products with AI
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <Button 
                    onClick={() => console.log("Generate urgent orders")}
                    variant="outline"
                    className="flex flex-col items-center gap-2 h-20"
                  >
                    <AlertTriangle className="h-6 w-6" />
                    <span className="text-sm">Urgent Orders</span>
                  </Button>
                  <Button 
                    onClick={() => console.log("Generate bulk orders")}
                    variant="outline"
                    className="flex flex-col items-center gap-2 h-20"
                  >
                    <Package className="h-6 w-6" />
                    <span className="text-sm">Bulk Orders</span>
                  </Button>
                  <Button 
                    onClick={() => console.log("Create product")}
                    variant="outline"
                    className="flex flex-col items-center gap-2 h-20"
                  >
                    <Plus className="h-6 w-6" />
                    <span className="text-sm">New Product</span>
                  </Button>
                  <Button 
                    onClick={fetchDashboardData}
                    variant="outline"
                    className="flex flex-col items-center gap-2 h-20"
                  >
                    <RefreshCw className="h-6 w-6" />
                    <span className="text-sm">Refresh Data</span>
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </main>
      </div>

      {/* Mobile Chat */}
      <div className="md:hidden">
        <CopilotPopup
          labels={{
            title: "Order Generation AI",
            initial: "🤖 I can generate orders and products for you. Try saying 'generate 5 urgent orders' or 'create a new product called Widget'.",
          }}
          suggestions={[
            {
              title: "Generate Orders",
              message: "Generate 5 mixed orders",
            },
            {
              title: "Create Product",
              message: "Create a new product called Smart Sensor",
            },
            {
              title: "Create Order",
              message: "Create an urgent order for microprocessors",
            },
          ]}
        />
      </div>
    </div>
  );
}
