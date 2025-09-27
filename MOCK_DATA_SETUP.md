# Mock Google Spreadsheet Setup Guide

This guide will help you create a mock Google Spreadsheet with supply chain data that you can use with your Supply Chain Optimization Agent.

## 📁 **Files Created**

### **Data Files**
- `mock_data/supply_chain_data.csv` - Basic CSV format
- `mock_data/google_sheets_format.csv` - Google Sheets compatible format
- `mock_data/supply_chain_canvas_data.json` - Direct canvas import format

### **Scripts**
- `mock_data/convert_csv_to_canvas.py` - Convert CSV to canvas format
- `mock_data/create_google_sheet.py` - Create real Google Sheet
- `mock_data/generate_canvas_data.py` - Generate canvas data directly

## 🚀 **Quick Start (Recommended)**

### **Option 1: Direct Canvas Import**
```bash
cd mock_data
python generate_canvas_data.py
```

This creates `supply_chain_canvas_data.json` that you can directly import into your application.

### **Option 2: Google Sheets Integration**
1. **Create a Google Sheet manually**:
   - Go to [Google Sheets](https://sheets.google.com)
   - Create a new spreadsheet
   - Copy the data from `mock_data/google_sheets_format.csv`
   - Paste it into the sheet

2. **Use the Sheet ID**:
   - Copy the Sheet ID from the URL
   - Use it in your Supply Chain Optimization Agent

## 📊 **Mock Data Overview**

### **🏭 Suppliers (3 items)**
- **TechCorp Solutions**: High-performance electronics supplier (95% reliability)
- **Global Parts Inc**: International raw materials supplier (78% reliability)
- **Budget Suppliers Ltd**: Cost-effective supplier (45% reliability)

### **📦 Inventory (3 items)**
- **Product A**: High-demand electronics (150 units in stock)
- **Product B**: Standard component (25 units - low stock)
- **Product C**: Trending product (0 units - out of stock)

### **📋 Orders (3 items)**
- **PO-2024-001**: Urgent order from TechCorp (confirmed)
- **PO-2024-002**: Standard order from Global Parts (shipped)
- **PO-2024-003**: Budget order from Budget Suppliers (delivered)

### **🚚 Logistics (3 items)**
- **SHIP-001**: Express delivery via FedEx (in transit)
- **SHIP-002**: Standard delivery via UPS (delivered)
- **SHIP-003**: International delivery via DHL (delayed)

## 🔧 **Detailed Setup Options**

### **Option A: Direct JSON Import**

1. **Generate the data**:
```bash
cd mock_data
python generate_canvas_data.py
```

2. **Import into your app**:
   - Copy the contents of `supply_chain_canvas_data.json`
   - Use it to populate your canvas state
   - Or modify your application to load this JSON file

### **Option B: Google Sheets Integration**

1. **Create Google Sheet**:
   - Go to [Google Sheets](https://sheets.google.com)
   - Create new spreadsheet
   - Name it "Supply Chain Management Dashboard"

2. **Add the data**:
   - Open `mock_data/google_sheets_format.csv`
   - Copy all the data
   - Paste it into your Google Sheet

3. **Get the Sheet ID**:
   - Copy the Sheet ID from the URL (the long string between `/d/` and `/edit`)
   - Example: `1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms`

4. **Use in your app**:
   - Use the Sheet ID in your Supply Chain Optimization Agent
   - The agent will automatically import and sync the data

### **Option C: Automated Google Sheet Creation**

1. **Set up Google API credentials**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable Google Sheets API
   - Create credentials (OAuth 2.0 Client ID)
   - Download the JSON file and rename it to `credentials.json`
   - Place it in the `mock_data` directory

2. **Run the script**:
```bash
cd mock_data
python create_google_sheet.py
```

3. **Use the generated Sheet ID**:
   - The script will output a Sheet ID
   - Use this ID in your Supply Chain Optimization Agent

## 🎯 **Using the Data in Your App**

### **Method 1: Direct State Import**
```javascript
// In your React component
import supplyChainData from './mock_data/supply_chain_canvas_data.json';

// Set the initial state
const [state, setState] = useState(supplyChainData);
```

### **Method 2: Google Sheets Integration**
1. **Start your app**: `pnpm dev`
2. **Open the Google Sheets modal**
3. **Enter the Sheet ID** from your Google Sheet
4. **Click "Import Sheet"**
5. **The agent will automatically populate the canvas**

### **Method 3: Chat with the Agent**
```
User: "Import data from Google Sheet ID: 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
Agent: [Imports and creates all the cards automatically]
```

## 📈 **Data Structure**

### **Supplier Data**
- Company name, category, location
- Reliability score (0-100)
- Contact information, products offered
- Delivery time, payment terms, risk level

### **Inventory Data**
- Product name, SKU, stock levels
- Min/max stock, reorder points
- Unit cost, supplier, lead time
- Current status (in stock, low stock, out of stock)

### **Order Data**
- Order number, supplier, dates
- Status (pending, confirmed, shipped, delivered)
- Amount, currency, priority
- Items ordered, special instructions

### **Logistics Data**
- Shipment ID, carrier, locations
- Shipping and arrival dates
- Status (picked up, in transit, delivered, delayed)
- Tracking number, cost, method
- Special handling requirements

## 🔄 **Real-time Sync**

Once you have the data imported:

1. **Automatic Sync**: Changes in the canvas automatically sync to Google Sheets
2. **Bidirectional**: Changes in Google Sheets sync back to the canvas
3. **AI Optimization**: The agent can analyze and optimize based on the data
4. **Real-time Updates**: All changes are reflected immediately

## 🎯 **Next Steps**

1. **Import the data** using one of the methods above
2. **Explore the cards** - click on different fields to see the data
3. **Chat with the agent** - ask it to analyze the data
4. **Try optimization** - ask the agent to optimize your supply chain
5. **Monitor performance** - use the agent's analysis tools

## 🚀 **Example Queries**

Once you have the data loaded, try these queries with the agent:

```
"Analyze our current inventory levels and identify any issues"
"Assess our supplier performance and provide recommendations"
"Identify potential risks in our supply chain"
"Optimize our procurement costs"
"Create a demand forecast for the next quarter"
"Set up monitoring for low stock items"
```

The mock data provides a realistic supply chain scenario with various challenges that the AI agent can help you optimize! 🎉
