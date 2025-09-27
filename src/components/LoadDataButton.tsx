"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

interface LoadDataButtonProps {
  onLoadData: (data: any) => void;
}

export function LoadDataButton({ onLoadData }: LoadDataButtonProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [loadedItems, setLoadedItems] = useState<number>(0);

  const loadMockData = () => {
    setIsLoading(true);
    
    // Direct mock data (same as in the JSON file)
    const mockData = {
      "items": [
        {
          "id": "0001",
          "type": "supplier",
          "name": "TechCorp Solutions",
          "subtitle": "Leading electronics supplier",
          "data": {
            "field1": "TechCorp Solutions",
            "field2": "components",
            "field3": "North America",
            "field4": ["ISO 9001", "FDA Certified"],
            "field5": 95,
            "field6": "contact@techcorp.com",
            "field7": ["Microprocessors", "Memory chips", "Circuit boards"],
            "field8": 7,
            "field9": "Net 30",
            "field10": "low"
          }
        },
        {
          "id": "0002",
          "type": "supplier",
          "name": "Global Parts Inc",
          "subtitle": "International component supplier",
          "data": {
            "field1": "Global Parts Inc",
            "field2": "raw materials",
            "field3": "Asia Pacific",
            "field4": ["ISO 9001", "ISO 14001"],
            "field5": 78,
            "field6": "info@globalparts.com",
            "field7": ["Steel", "Aluminum", "Plastics"],
            "field8": 14,
            "field9": "Net 45",
            "field10": "medium"
          }
        },
        {
          "id": "0003",
          "type": "supplier",
          "name": "Budget Suppliers Ltd",
          "subtitle": "Cost-effective supplier",
          "data": {
            "field1": "Budget Suppliers Ltd",
            "field2": "components",
            "field3": "Europe",
            "field4": ["ISO 9001"],
            "field5": 45,
            "field6": "sales@budgetsuppliers.com",
            "field7": ["Basic components", "Generic parts"],
            "field8": 21,
            "field9": "Net 60",
            "field10": "high"
          }
        },
        {
          "id": "0004",
          "type": "inventory",
          "name": "Product A",
          "subtitle": "High-demand electronics",
          "data": {
            "field1": "Product A",
            "field2": "ELEC-001",
            "field3": 150,
            "field4": 50,
            "field5": 200,
            "field6": 75,
            "field7": "units",
            "field8": 25.99,
            "field9": "TechCorp Solutions",
            "field10": "Warehouse A",
            "field11": 7,
            "field12": "in stock"
          }
        },
        {
          "id": "0005",
          "type": "inventory",
          "name": "Product B",
          "subtitle": "Standard component",
          "data": {
            "field1": "Product B",
            "field2": "COMP-002",
            "field3": 25,
            "field4": 30,
            "field5": 100,
            "field6": 40,
            "field7": "units",
            "field8": 15.50,
            "field9": "Global Parts Inc",
            "field10": "Warehouse B",
            "field11": 14,
            "field12": "low stock"
          }
        },
        {
          "id": "0006",
          "type": "inventory",
          "name": "Product C",
          "subtitle": "Trending product",
          "data": {
            "field1": "Product C",
            "field2": "TREND-003",
            "field3": 0,
            "field4": 20,
            "field5": 80,
            "field6": 25,
            "field7": "units",
            "field8": 45.00,
            "field9": "Budget Suppliers Ltd",
            "field10": "Warehouse A",
            "field11": 21,
            "field12": "out of stock"
          }
        },
        {
          "id": "0007",
          "type": "order",
          "name": "PO-2024-001",
          "subtitle": "Urgent component order",
          "data": {
            "field1": "PO-2024-001",
            "field2": "TechCorp Solutions",
            "field3": "2024-01-15",
            "field4": "2024-01-22",
            "field5": "confirmed",
            "field6": 12500.00,
            "field7": "USD",
            "field8": ["Product A", "Product B"],
            "field9": "urgent",
            "field10": "Express delivery required"
          }
        },
        {
          "id": "0008",
          "type": "order",
          "name": "PO-2024-002",
          "subtitle": "Standard order",
          "data": {
            "field1": "PO-2024-002",
            "field2": "Global Parts Inc",
            "field3": "2024-01-10",
            "field4": "2024-01-24",
            "field5": "shipped",
            "field6": 8500.00,
            "field7": "USD",
            "field8": ["Product B"],
            "field9": "medium",
            "field10": "Standard delivery"
          }
        },
        {
          "id": "0009",
          "type": "order",
          "name": "PO-2024-003",
          "subtitle": "Budget order",
          "data": {
            "field1": "PO-2024-003",
            "field2": "Budget Suppliers Ltd",
            "field3": "2024-01-05",
            "field4": "2024-01-26",
            "field5": "delivered",
            "field6": 3200.00,
            "field7": "USD",
            "field8": ["Product C"],
            "field9": "low",
            "field10": "No special requirements"
          }
        },
        {
          "id": "0010",
          "type": "logistics",
          "name": "SHIP-001",
          "subtitle": "Express delivery",
          "data": {
            "field1": "SHIP-001",
            "field2": "FedEx",
            "field3": "New York NY",
            "field4": "Los Angeles CA",
            "field5": "2024-01-20",
            "field6": "2024-01-22",
            "field7": "in transit",
            "field8": "1Z999AA1234567890",
            "field9": 125.50,
            "field10": "air",
            "field11": "Handle with care - electronics",
            "field12": 50
          }
        },
        {
          "id": "0011",
          "type": "logistics",
          "name": "SHIP-002",
          "subtitle": "Standard delivery",
          "data": {
            "field1": "SHIP-002",
            "field2": "UPS",
            "field3": "Chicago IL",
            "field4": "Seattle WA",
            "field5": "2024-01-18",
            "field6": "2024-01-25",
            "field7": "delivered",
            "field8": "1Z888BB9876543210",
            "field9": 89.75,
            "field10": "ground",
            "field11": "Standard handling",
            "field12": 25
          }
        },
        {
          "id": "0012",
          "type": "logistics",
          "name": "SHIP-003",
          "subtitle": "International delivery",
          "data": {
            "field1": "SHIP-003",
            "field2": "DHL",
            "field3": "Shanghai China",
            "field4": "San Francisco CA",
            "field5": "2024-01-12",
            "field6": "2024-01-28",
            "field7": "delayed",
            "field8": "1Z777CC4567890123",
            "field9": 245.00,
            "field10": "sea",
            "field11": "International customs clearance",
            "field12": 100
          }
        }
      ],
      "globalTitle": "Supply Chain Management Dashboard",
      "globalDescription": "Comprehensive supply chain optimization with AI-powered insights and real-time monitoring",
      "lastAction": "loaded_from_mock_data",
      "itemsCreated": 12,
      "syncSheetId": "",
      "syncSheetName": ""
    };
    
    onLoadData(mockData);
    setLoadedItems(mockData.items.length);
    console.log(`✅ Loaded ${mockData.items.length} items from mock data`);
    setIsLoading(false);
  };

  return (
    <Card className="w-full max-w-md mx-auto mb-6">
      <CardHeader>
        <CardTitle className="text-center">📊 Load Supply Chain Data</CardTitle>
        <CardDescription className="text-center">
          Click the button below to load sample supply chain data
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <Button 
          onClick={loadMockData} 
          disabled={isLoading}
          className="w-full"
          size="lg"
        >
          {isLoading ? "Loading..." : "🚀 Load Sample Data (12 items)"}
        </Button>
        
        {loadedItems > 0 && (
          <div className="text-center text-green-600 font-medium">
            ✅ Loaded {loadedItems} items successfully!
          </div>
        )}
        
        <div className="text-xs text-gray-500 text-center">
          <p><strong>What you'll get:</strong></p>
          <p>🏭 3 Suppliers • 📦 3 Inventory • 📋 3 Orders • 🚚 3 Logistics</p>
        </div>
      </CardContent>
    </Card>
  );
}

export default LoadDataButton;
