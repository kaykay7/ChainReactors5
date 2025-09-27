# 📊 Separate Google Sheets Setup Guide

You're absolutely right! Having separate Google Sheets for each supply chain category is much more logical and organized. Here's the complete setup for 4 separate Google Sheets.

## 🗂️ **File Structure**

### **📁 Separate CSV Files**
- **`suppliers.csv`** - Supplier management and performance tracking
- **`inventory.csv`** - Inventory levels and stock management  
- **`orders.csv`** - Purchase orders and delivery tracking
- **`logistics.csv`** - Shipping and logistics coordination

### **🔧 Integration Scripts**
- **`generate_from_separate_csvs.py`** - Convert separate CSV files to canvas format
- **`create_separate_sheets.py`** - Create 4 separate Google Sheets automatically

## 🚀 **Quick Start Options**

### **Option 1: Manual Google Sheets Creation (Easiest)**

#### **Step 1: Create 4 Google Sheets**
1. Go to [Google Sheets](https://sheets.google.com)
2. Create 4 new spreadsheets with these names:
   - **"Supply Chain - Suppliers"**
   - **"Supply Chain - Inventory"**
   - **"Supply Chain - Orders"**
   - **"Supply Chain - Logistics"**

#### **Step 2: Import Data**
For each sheet, copy the corresponding CSV data:

**🏭 Suppliers Sheet:**
```
ID,Name,Subtitle,Company Name,Category,Location,Certifications,Reliability Score,Contact Info,Products,Delivery Time,Payment Terms,Risk Level
0001,TechCorp Solutions,Leading electronics supplier,TechCorp Solutions,components,North America,"ISO 9001; FDA Certified",95,contact@techcorp.com,"Microprocessors; Memory chips; Circuit boards",7,Net 30,low
0002,Global Parts Inc,International component supplier,Global Parts Inc,raw materials,Asia Pacific,"ISO 9001; ISO 14001",78,info@globalparts.com,"Steel; Aluminum; Plastics",14,Net 45,medium
0003,Budget Suppliers Ltd,Cost-effective supplier,Budget Suppliers Ltd,components,Europe,ISO 9001,45,sales@budgetsuppliers.com,"Basic components; Generic parts",21,Net 60,high
```

**📦 Inventory Sheet:**
```
ID,Name,Subtitle,Product Name,SKU,Current Stock,Min Stock,Max Stock,Reorder Point,Unit of Measure,Unit Cost,Supplier,Location,Lead Time,Status
0001,Product A,High-demand electronics,Product A,ELEC-001,150,50,200,75,units,25.99,TechCorp Solutions,Warehouse A,7,in stock
0002,Product B,Standard component,Product B,COMP-002,25,30,100,40,units,15.50,Global Parts Inc,Warehouse B,14,low stock
0003,Product C,Trending product,Product C,TREND-003,0,20,80,25,units,45.00,Budget Suppliers Ltd,Warehouse A,21,out of stock
```

**📋 Orders Sheet:**
```
ID,Name,Subtitle,Order Number,Supplier,Order Date,Expected Delivery,Status,Total Amount,Currency,Items Ordered,Priority,Notes
0001,PO-2024-001,Urgent component order,PO-2024-001,TechCorp Solutions,2024-01-15,2024-01-22,confirmed,12500.00,USD,"Product A; Product B",urgent,Express delivery required
0002,PO-2024-002,Standard order,PO-2024-002,Global Parts Inc,2024-01-10,2024-01-24,shipped,8500.00,USD,Product B,medium,Standard delivery
0003,PO-2024-003,Budget order,PO-2024-003,Budget Suppliers Ltd,2024-01-05,2024-01-26,delivered,3200.00,USD,Product C,low,No special requirements
```

**🚚 Logistics Sheet:**
```
ID,Name,Subtitle,Shipment ID,Carrier,Origin Location,Destination Location,Shipping Date,Expected Arrival,Status,Tracking Number,Shipping Cost,Shipping Method,Special Requirements,Weight/Volume
0001,SHIP-001,Express delivery,SHIP-001,FedEx,New York NY,Los Angeles CA,2024-01-20,2024-01-22,in transit,1Z999AA1234567890,125.50,air,Handle with care - electronics,50
0002,SHIP-002,Standard delivery,SHIP-002,UPS,Chicago IL,Seattle WA,2024-01-18,2024-01-25,delivered,1Z888BB9876543210,89.75,ground,Standard handling,25
0003,SHIP-003,International delivery,SHIP-003,DHL,Shanghai China,San Francisco CA,2024-01-12,2024-01-28,delayed,1Z777CC4567890123,245.00,sea,International customs clearance,100
```

#### **Step 3: Get Sheet IDs**
Copy the Sheet ID from each URL (the long string between `/d/` and `/edit`):
- Example: `1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms`

### **Option 2: Automated Google Sheets Creation**

#### **Step 1: Set up Google API credentials**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Sheets API
4. Create credentials (OAuth 2.0 Client ID)
5. Download the JSON file and rename it to `credentials.json`
6. Place it in the `mock_data` directory

#### **Step 2: Run the automation script**
```bash
cd mock_data
python3 create_separate_sheets.py
```

This will create 4 separate Google Sheets automatically and save the Sheet IDs to `sheet_ids.json`.

## 🎯 **Using the Separate Sheets in Your App**

### **Method 1: Individual Sheet Import**
```
User: "Import suppliers from Google Sheet ID: 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
Agent: [Imports only supplier data and creates supplier cards]
```

### **Method 2: Bulk Import**
```
User: "Import all supply chain data from these sheets:
- Suppliers: 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms
- Inventory: 1CxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms
- Orders: 1DxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms
- Logistics: 1ExiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
Agent: [Imports all data and creates all cards]
```

### **Method 3: Category-specific Operations**
```
User: "Analyze our suppliers and create supplier cards"
Agent: [Analyzes supplier data and creates supplier cards]

User: "Check our inventory levels and create inventory cards"
Agent: [Analyzes inventory data and creates inventory cards]
```

## 📊 **Benefits of Separate Sheets**

### **🎯 Better Organization**
- **Focused Data**: Each sheet contains only relevant data for its category
- **Easier Management**: Update suppliers without affecting inventory data
- **Clear Separation**: Logical boundaries between different business functions

### **🔄 Flexible Integration**
- **Selective Import**: Import only the data you need
- **Category-specific Analysis**: Analyze suppliers, inventory, orders, or logistics separately
- **Modular Updates**: Update one category without affecting others

### **📈 Scalability**
- **Independent Growth**: Each category can grow independently
- **Specialized Views**: Create focused dashboards for each category
- **Team Collaboration**: Different teams can manage different sheets

## 🔧 **Advanced Features**

### **Cross-Sheet Relationships**
The separate sheets maintain relationships through common fields:
- **Suppliers** → **Inventory** (via Supplier field)
- **Suppliers** → **Orders** (via Supplier field)
- **Orders** → **Logistics** (via Order tracking)

### **AI Agent Capabilities**
With separate sheets, the agent can:
- **Analyze supplier performance** across all suppliers
- **Monitor inventory levels** across all products
- **Track order status** across all orders
- **Optimize logistics** across all shipments
- **Identify cross-category issues** (e.g., supplier delays affecting inventory)

### **Real-time Synchronization**
- **Bidirectional Sync**: Changes in the canvas sync back to Google Sheets
- **Category-specific Updates**: Update suppliers without affecting other data
- **Selective Sync**: Choose which categories to sync

## 🎉 **You're All Set!**

The separate Google Sheets approach provides:
- **Better organization** with focused data per category
- **Flexible integration** with selective import capabilities
- **Scalable structure** for growing supply chain operations
- **AI-powered analysis** across all categories

This approach is much more logical and practical for real-world supply chain management! 🚀
