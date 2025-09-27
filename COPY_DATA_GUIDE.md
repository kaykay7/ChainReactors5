# 📋 How to Copy CSV Data to Google Sheets

## 🚀 **Step-by-Step Instructions**

### **Step 1: Create Google Sheets**

1. Go to [Google Sheets](https://sheets.google.com)
2. Click **"+ Blank"** to create a new spreadsheet
3. Create **4 separate spreadsheets** with these names:
   - **"Supply Chain - Suppliers"**
   - **"Supply Chain - Inventory"**
   - **"Supply Chain - Orders"**
   - **"Supply Chain - Logistics"**

### **Step 2: Copy Data for Each Sheet**

#### **🏭 Suppliers Sheet**

1. **Open the "Supply Chain - Suppliers" spreadsheet**
2. **Copy this header row** (Row 1):
```
ID,Name,Subtitle,Company Name,Category,Location,Certifications,Reliability Score,Contact Info,Products,Delivery Time,Payment Terms,Risk Level
```

3. **Copy these data rows** (Rows 2-4):
```
0001,TechCorp Solutions,Leading electronics supplier,TechCorp Solutions,components,North America,"ISO 9001; FDA Certified",95,contact@techcorp.com,"Microprocessors; Memory chips; Circuit boards",7,Net 30,low
0002,Global Parts Inc,International component supplier,Global Parts Inc,raw materials,Asia Pacific,"ISO 9001; ISO 14001",78,info@globalparts.com,"Steel; Aluminum; Plastics",14,Net 45,medium
0003,Budget Suppliers Ltd,Cost-effective supplier,Budget Suppliers Ltd,components,Europe,ISO 9001,45,sales@budgetsuppliers.com,"Basic components; Generic parts",21,Net 60,high
```

4. **Paste into Google Sheets** (starting from cell A1)

#### **📦 Inventory Sheet**

1. **Open the "Supply Chain - Inventory" spreadsheet**
2. **Copy this header row**:
```
ID,Name,Subtitle,Product Name,SKU,Current Stock,Min Stock,Max Stock,Reorder Point,Unit of Measure,Unit Cost,Supplier,Location,Lead Time,Status
```

3. **Copy these data rows**:
```
0001,Product A,High-demand electronics,Product A,ELEC-001,150,50,200,75,units,25.99,TechCorp Solutions,Warehouse A,7,in stock
0002,Product B,Standard component,Product B,COMP-002,25,30,100,40,units,15.50,Global Parts Inc,Warehouse B,14,low stock
0003,Product C,Trending product,Product C,TREND-003,0,20,80,25,units,45.00,Budget Suppliers Ltd,Warehouse A,21,out of stock
```

#### **📋 Orders Sheet**

1. **Open the "Supply Chain - Orders" spreadsheet**
2. **Copy this header row**:
```
ID,Name,Subtitle,Order Number,Supplier,Order Date,Expected Delivery,Status,Total Amount,Currency,Items Ordered,Priority,Notes
```

3. **Copy these data rows**:
```
0001,PO-2024-001,Urgent component order,PO-2024-001,TechCorp Solutions,2024-01-15,2024-01-22,confirmed,12500.00,USD,"Product A; Product B",urgent,Express delivery required
0002,PO-2024-002,Standard order,PO-2024-002,Global Parts Inc,2024-01-10,2024-01-24,shipped,8500.00,USD,Product B,medium,Standard delivery
0003,PO-2024-003,Budget order,PO-2024-003,Budget Suppliers Ltd,2024-01-05,2024-01-26,delivered,3200.00,USD,Product C,low,No special requirements
```

#### **🚚 Logistics Sheet**

1. **Open the "Supply Chain - Logistics" spreadsheet**
2. **Copy this header row**:
```
ID,Name,Subtitle,Shipment ID,Carrier,Origin Location,Destination Location,Shipping Date,Expected Arrival,Status,Tracking Number,Shipping Cost,Shipping Method,Special Requirements,Weight/Volume
```

3. **Copy these data rows**:
```
0001,SHIP-001,Express delivery,SHIP-001,FedEx,New York NY,Los Angeles CA,2024-01-20,2024-01-22,in transit,1Z999AA1234567890,125.50,air,Handle with care - electronics,50
0002,SHIP-002,Standard delivery,SHIP-002,UPS,Chicago IL,Seattle WA,2024-01-18,2024-01-25,delivered,1Z888BB9876543210,89.75,ground,Standard handling,25
0003,SHIP-003,International delivery,SHIP-003,DHL,Shanghai China,San Francisco CA,2024-01-12,2024-01-28,delayed,1Z777CC4567890123,245.00,sea,International customs clearance,100
```

### **Step 3: Format the Sheets (Optional)**

1. **Select the header row** (Row 1)
2. **Make it bold** and **change background color** to blue
3. **Freeze the header row** (View → Freeze → 1 row)

### **Step 4: Get Sheet IDs**

1. **Copy the Sheet ID** from each URL:
   - URL format: `https://docs.google.com/spreadsheets/d/SHEET_ID/edit`
   - Copy the `SHEET_ID` part (the long string between `/d/` and `/edit`)

2. **Save the Sheet IDs** for use in your app:
   - Suppliers Sheet ID: `[Your Sheet ID]`
   - Inventory Sheet ID: `[Your Sheet ID]`
   - Orders Sheet ID: `[Your Sheet ID]`
   - Logistics Sheet ID: `[Your Sheet ID]`

## 🎯 **Alternative: Direct CSV Import**

### **Method 1: Upload CSV Files**
1. **Go to Google Sheets**
2. **Click "File" → "Import"**
3. **Upload the CSV files** from the `mock_data` folder:
   - `suppliers.csv`
   - `inventory.csv`
   - `orders.csv`
   - `logistics.csv`

### **Method 2: Copy from CSV Files**
1. **Open each CSV file** in a text editor
2. **Select all content** (Ctrl+A / Cmd+A)
3. **Copy** (Ctrl+C / Cmd+C)
4. **Paste into Google Sheets** (Ctrl+V / Cmd+V)

## 🔧 **Using the Sheet IDs in Your App**

### **Individual Import**
```
User: "Import suppliers from Google Sheet ID: [Your Suppliers Sheet ID]"
Agent: [Imports supplier data and creates supplier cards]
```

### **Bulk Import**
```
User: "Import all supply chain data from these sheets:
- Suppliers: [Suppliers Sheet ID]
- Inventory: [Inventory Sheet ID]
- Orders: [Orders Sheet ID]
- Logistics: [Logistics Sheet ID]"
Agent: [Imports all data and creates all cards]
```

## 🎉 **You're Done!**

Once you have the 4 Google Sheets set up with the data, you can:
1. **Use the Sheet IDs** in your Supply Chain Optimization Agent
2. **Import the data** to populate the canvas
3. **Start analyzing** with the AI agent

The separate sheets approach gives you much better organization and flexibility! 🚀
