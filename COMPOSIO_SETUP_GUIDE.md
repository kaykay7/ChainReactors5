# 🔧 Composio Setup and Testing Guide

## 🚨 **Current Issue: Composio Not Configured**

The test shows that Composio is not properly configured. Here's how to fix it:

## 🔑 **Step 1: Get Composio Credentials**

### **Option A: Get Free Composio Account**
1. **Go to [Composio](https://composio.dev)**
2. **Sign up for a free account**
3. **Get your API key** from the dashboard
4. **Get your User ID** from the dashboard

### **Option B: Use Existing Account**
If you already have a Composio account:
1. **Log in to your Composio dashboard**
2. **Copy your API key**
3. **Copy your User ID**

## 📝 **Step 2: Configure Environment Variables**

### **Create/Update .env file**
Create a `.env` file in your project root with:
```bash
COMPOSIO_API_KEY=your_actual_api_key_here
COMPOSIO_USER_ID=your_actual_user_id_here
```

### **Example .env file:**
```bash
# Composio Configuration
COMPOSIO_API_KEY=cp_1234567890abcdef
COMPOSIO_USER_ID=user_1234567890

# Other environment variables...
OPENAI_API_KEY=your_openai_key_here
```

## 🧪 **Step 3: Test Composio Connection**

### **Run the test script:**
```bash
python3 simple_composio_test.py
```

### **Expected output:**
```
🔍 Testing Composio Setup...
========================================
COMPOSIO_API_KEY: ✅ Found
COMPOSIO_USER_ID: ✅ Found
✅ Composio package imported successfully
✅ Composio client initialized successfully

🎉 Composio is properly configured!
```

## 🔍 **Step 4: Test Google Sheets Integration**

### **Method 1: Test with a Real Google Sheet**
1. **Create a Google Sheet** with some data
2. **Get the Sheet ID** from the URL
3. **Test the connection:**
```bash
python3 test_composio.py
```

### **Method 2: Test in Your Application**
1. **Start your app**: `pnpm dev`
2. **Open the Google Sheets modal**
3. **Enter a Sheet ID** and click "Import Sheet"
4. **Check if cards appear** on the canvas

## 🎯 **Step 5: Verify Data Import**

### **Check Console Logs**
Look for these messages in your application:
```
✅ Got sheet info: [Spreadsheet Title]
✅ Number of rows retrieved: [number]
✅ Converting [number] items to canvas format
```

### **Check Canvas Cards**
After importing, you should see:
- **Cards created** on the canvas
- **Data populated** in the card fields
- **Correct card types** (supplier, inventory, order, logistics)

## 🚨 **Troubleshooting Common Issues**

### **Issue 1: "COMPOSIO_API_KEY not found"**
**Solution:**
1. **Check .env file** exists in project root
2. **Verify API key** is correct
3. **Restart your application** after adding .env

### **Issue 2: "Failed to initialize Composio client"**
**Solution:**
1. **Check internet connection**
2. **Verify API key** is valid
3. **Check Composio service** status

### **Issue 3: "Failed to get spreadsheet info"**
**Solution:**
1. **Check Sheet ID** is correct
2. **Verify sheet permissions** (make it public or share with your account)
3. **Check Google Sheets API** is enabled in Composio

### **Issue 4: "No data found in sheet"**
**Solution:**
1. **Check sheet has data** in rows 1+
2. **Verify data format** matches expected structure
3. **Check sheet name** is correct

## 📊 **How to Know if Composio is Working**

### **✅ Success Indicators:**
1. **No error messages** in console
2. **Cards appear** on canvas after import
3. **Data is accurate** and matches your sheets
4. **Agent responds** with import confirmations

### **❌ Failure Indicators:**
1. **Error messages** about Composio connection
2. **No cards created** after import attempt
3. **Empty responses** from the agent
4. **403/404 errors** in console

## 🎯 **Testing with Your Mock Data**

### **Step 1: Create Google Sheets**
1. **Go to Google Sheets**
2. **Create 4 sheets** with the CSV data I provided
3. **Get the Sheet IDs**

### **Step 2: Test Import**
```
User: "Import suppliers from Google Sheet ID: [Your Sheet ID]"
Agent: [Should create supplier cards]
```

### **Step 3: Verify Data**
- **Check cards** have correct data
- **Verify relationships** between cards
- **Test AI analysis** with the imported data

## 🚀 **Next Steps**

Once Composio is working:
1. **Test with real data** from your Google Sheets
2. **Verify bidirectional sync** (canvas ↔ sheets)
3. **Test AI analysis** with imported data
4. **Optimize performance** for larger datasets

## 💡 **Pro Tips**

### **For Development:**
- **Use test sheets** with small datasets first
- **Check console logs** for debugging
- **Test individual sheets** before bulk import

### **For Production:**
- **Set up proper error handling**
- **Monitor API usage** and limits
- **Implement data validation**

The key is to get Composio properly configured first, then test with your Google Sheets data! 🎯
