# 🔍 How to Test if Composio is Pulling CSV Data

## 🚀 **Quick Testing Steps**

### **Step 1: Test Composio Connection**
```bash
cd /Users/kunalkamdar/Documents/copilotkit-canva-llamaindex-project/copilotkit-canvas-llamaindex
python3 test_composio.py
```

This will test:
- ✅ Composio API key configuration
- ✅ Composio client initialization
- ✅ Google Sheets connection (if you provide a Sheet ID)

### **Step 2: Check Environment Variables**
Make sure you have these in your `.env` file:
```bash
COMPOSIO_API_KEY=your_api_key_here
COMPOSIO_USER_ID=your_user_id_here
```

### **Step 3: Test in Your Application**

#### **Method 1: Chat with the Agent**
```
User: "Import data from Google Sheet ID: [Your Sheet ID]"
Agent: [Should import and create cards]
```

#### **Method 2: Check Console Logs**
Look for these log messages in your application:
- `"Got sheet info: [Spreadsheet Title]"`
- `"Sheet info keys: [list of available fields]"`
- `"Number of rows retrieved: [number]"`

#### **Method 3: Use the Google Sheets Modal**
1. **Start your app**: `pnpm dev`
2. **Click the Google Sheets button** in the UI
3. **Enter a Sheet ID** and click "Import Sheet"
4. **Check if cards appear** on the canvas

## 🔧 **Troubleshooting Common Issues**

### **Issue 1: Composio Not Connected**
**Symptoms:**
- Error: "Failed to initialize Composio client"
- No response from Google Sheets

**Solutions:**
1. **Check API Key**: Verify `COMPOSIO_API_KEY` in `.env`
2. **Install Composio**: `pip install composio`
3. **Check User ID**: Verify `COMPOSIO_USER_ID` in `.env`

### **Issue 2: Google Sheets Access Denied**
**Symptoms:**
- Error: "Failed to get spreadsheet info"
- 403 Forbidden errors

**Solutions:**
1. **Check Sheet Permissions**: Make sure the sheet is shared with your Google account
2. **Verify Sheet ID**: Ensure the Sheet ID is correct
3. **Check Composio Permissions**: Make sure Composio has access to Google Sheets

### **Issue 3: No Data Retrieved**
**Symptoms:**
- Connection successful but no cards created
- "No data found in sheet" message

**Solutions:**
1. **Check Sheet Format**: Ensure data is in the correct format
2. **Verify Sheet Name**: Make sure you're importing from the right sheet
3. **Check Data Range**: Ensure data starts from row 1, column A

## 📊 **How to Verify Data is Being Pulled**

### **Check 1: Console Output**
Look for these messages in your application logs:
```
✅ Got sheet info: Supply Chain - Suppliers
✅ Sheet info keys: ['properties', 'sheets', 'spreadsheetId']
✅ Number of rows retrieved: 4
✅ Converting 3 items to canvas format
```

### **Check 2: Canvas Cards**
After importing, you should see:
- **Supplier cards** with company info, reliability scores, risk levels
- **Inventory cards** with product names, stock levels, status
- **Order cards** with order numbers, suppliers, amounts
- **Logistics cards** with shipment IDs, carriers, tracking numbers

### **Check 3: Data Accuracy**
Verify that the imported data matches your CSV:
- **Company names** from suppliers.csv
- **Product names** from inventory.csv
- **Order numbers** from orders.csv
- **Shipment IDs** from logistics.csv

## 🎯 **Testing with Your Mock Data**

### **Step 1: Create Google Sheets**
1. **Go to Google Sheets**
2. **Create 4 sheets** with the data from the CSV files
3. **Get the Sheet IDs** from the URLs

### **Step 2: Test Individual Sheets**
```
User: "Import suppliers from Google Sheet ID: [Suppliers Sheet ID]"
Agent: [Should create 3 supplier cards]

User: "Import inventory from Google Sheet ID: [Inventory Sheet ID]"
Agent: [Should create 3 inventory cards]
```

### **Step 3: Test Bulk Import**
```
User: "Import all supply chain data from these sheets:
- Suppliers: [Suppliers Sheet ID]
- Inventory: [Inventory Sheet ID]
- Orders: [Orders Sheet ID]
- Logistics: [Logistics Sheet ID]"
Agent: [Should create all 12 cards]
```

## 🔍 **Debug Information**

### **Check Composio Logs**
Look for these in your application console:
- `"Composio client initialized successfully"`
- `"Successfully connected to Google Sheets!"`
- `"Number of rows retrieved: [number]"`

### **Check Sheet Data Format**
Ensure your Google Sheets have:
- **Header row** with proper column names
- **Data rows** with actual values
- **No empty rows** between header and data
- **Consistent formatting** across all sheets

### **Check Agent Response**
The agent should respond with:
- **Confirmation messages** about importing data
- **Card creation notifications** for each item
- **Summary of imported items** by category

## 🎉 **Success Indicators**

### **✅ Composio is Working When:**
1. **No error messages** in console
2. **Cards appear** on the canvas after import
3. **Data is accurate** and matches your CSV files
4. **Agent responds** with import confirmations

### **❌ Composio is Not Working When:**
1. **Error messages** about Composio connection
2. **No cards created** after import attempt
3. **Empty responses** from the agent
4. **403/404 errors** in console

## 🚀 **Next Steps**

Once you confirm Composio is working:
1. **Test with real data** from your Google Sheets
2. **Verify bidirectional sync** (changes in canvas sync to sheets)
3. **Test AI analysis** with the imported data
4. **Optimize performance** for larger datasets

The key is to check the console logs and verify that cards are actually being created on the canvas after import attempts! 🎯
