# 📊 CSV Data Source Rule for All Agents

## 🎯 **Rule: All Agents Must Use CSV Files Only**

**CRITICAL RULE**: All specialized agents in the system are **mandated** to use only CSV files as their data source. No external APIs, databases, or other data sources are permitted.

## 📋 **Rule Implementation**

### **✅ What Agents MUST Do**
1. **Use CSVDataSource class** for all data access
2. **Load data from CSV files** in the `./mock_data/` directory
3. **Map CSV columns** to expected field names
4. **Include data_source: "CSV"** in all responses
5. **Validate CSV data integrity** before processing

### **❌ What Agents MUST NOT Do**
1. **Access external APIs** (Google Sheets, databases, etc.)
2. **Use hardcoded data** or mock objects
3. **Connect to external services** for data
4. **Use any data source other than CSV files**

## 🏗️ **Implementation Details**

### **1. CSV Data Source Class**
```python
from agent.agent.csv_data_source import CSVDataSource

# All agents must use this class
csv_data_source = CSVDataSource(csv_dir="./mock_data")
```

### **2. Required CSV Files**
All agents must work with these CSV files:
- **`suppliers.csv`** - Supplier information
- **`inventory.csv`** - Inventory data
- **`orders.csv`** - Order information
- **`logistics.csv`** - Logistics data

### **3. Agent Initialization**
```python
# All agents must be initialized with CSV data source
agent = InventoryAgent(
    memory_manager=memory_manager,
    csv_data_source=csv_data_source
)
```

### **4. Data Access Pattern**
```python
def analyze_data(self, data: List[Dict] = None) -> Dict[str, Any]:
    """All agent methods must follow this pattern."""
    # Use CSV data if no data provided
    if data is None:
        data = self.csv_data_source.get_supplier_data()  # or appropriate method
    
    # Process data
    result = {
        "data_source": "CSV",
        # ... analysis results
    }
    
    return result
```

## 📊 **CSV File Structure Requirements**

### **suppliers.csv**
```csv
ID,Name,Subtitle,Company Name,Category,Location,Certifications,Reliability Score,Contact Info,Products,Delivery Time,Payment Terms,Risk Level
0001,TechCorp Solutions,Leading electronics supplier,TechCorp Solutions,components,North America,"ISO 9001; FDA Certified",95,contact@techcorp.com,"Microprocessors; Memory chips; Circuit boards",7,Net 30,low
```

### **inventory.csv**
```csv
ID,Name,Subtitle,Product Name,SKU,Current Stock,Min Stock,Max Stock,Reorder Point,Unit of Measure,Unit Cost,Supplier,Location,Lead Time,Status
0001,Product A,High-demand electronics,Product A,ELEC-001,150,50,200,75,units,25.99,TechCorp Solutions,Warehouse A,7,in stock
```

### **orders.csv**
```csv
ID,Name,Subtitle,Order Number,Supplier,Order Date,Expected Delivery,Status,Total Amount,Currency,Items Ordered,Priority,Notes
0001,PO-2024-001,Urgent component order,PO-2024-001,TechCorp Solutions,2024-01-15,2024-01-22,confirmed,12500.00,USD,"Product A; Product B",urgent,Express delivery required
```

### **logistics.csv**
```csv
ID,Name,Subtitle,Shipment ID,Carrier,Origin Location,Destination Location,Shipping Date,Expected Arrival,Status,Tracking Number,Shipping Cost,Shipping Method,Special Requirements,Weight/Volume
0001,SHIP-001,Express delivery,SHIP-001,FedEx,New York NY,Los Angeles CA,2024-01-20,2024-01-22,in transit,1Z999AA1234567890,125.50,air,Handle with care - electronics,50
```

## 🎯 **Agent-Specific Rules**

### **🧮 Inventory Agent Rules**
```python
# MUST use CSV data source
def analyze_stock_levels(self, inventory_data: List[Dict] = None) -> Dict[str, Any]:
    if inventory_data is None:
        inventory_data = self.csv_data_source.get_inventory_data()
    
    # Map CSV columns to expected fields
    current_stock = item.get('Current Stock', 0)
    min_stock = item.get('Min Stock', 0)
    max_stock = item.get('Max Stock', 0)
    reorder_point = item.get('Reorder Point', 0)
    
    return {
        "data_source": "CSV",
        # ... analysis results
    }
```

### **🏭 Supplier Agent Rules**
```python
# MUST use CSV data source
def analyze_supplier_performance(self, supplier_data: List[Dict] = None) -> Dict[str, Any]:
    if supplier_data is None:
        supplier_data = self.csv_data_source.get_supplier_data()
    
    # Map CSV columns to expected fields
    reliability_score = supplier.get('Reliability Score', 0)
    delivery_time = supplier.get('Delivery Time', 0)
    company_name = supplier.get('Company Name', '')
    
    return {
        "data_source": "CSV",
        # ... analysis results
    }
```

### **📈 Forecasting Agent Rules**
```python
# MUST use CSV data source
def forecast_demand(self, historical_data: List[Dict] = None) -> Dict[str, Any]:
    if historical_data is None:
        # Get historical data from CSV
        historical_data = self.csv_data_source.get_inventory_data()
    
    return {
        "data_source": "CSV",
        # ... forecast results
    }
```

## 🔍 **Data Validation Rules**

### **1. CSV File Existence Check**
```python
def _validate_csv_files(self) -> bool:
    """Validate that all required CSV files exist."""
    required_files = ["suppliers.csv", "inventory.csv", "orders.csv", "logistics.csv"]
    
    for file in required_files:
        if not (self.csv_dir / file).exists():
            raise FileNotFoundError(f"Required CSV file not found: {file}")
    
    return True
```

### **2. Data Integrity Check**
```python
def _validate_data_integrity(self) -> Dict[str, Any]:
    """Validate CSV data integrity."""
    validation_results = {
        "supplier_data": {"valid": True, "issues": []},
        "inventory_data": {"valid": True, "issues": []},
        "order_data": {"valid": True, "issues": []},
        "logistics_data": {"valid": True, "issues": []}
    }
    
    # Check required columns
    required_supplier_columns = ["ID", "Name", "Company Name", "Category", "Location", "Reliability Score"]
    # ... validation logic
    
    return validation_results
```

## 🚨 **Enforcement Mechanisms**

### **1. Runtime Validation**
```python
def _enforce_csv_only_rule(self):
    """Enforce that only CSV data is used."""
    if hasattr(self, 'csv_data_source') and self.csv_data_source is None:
        raise ValueError("CSV data source is required for all agents")
    
    # Check that no external data sources are used
    if hasattr(self, 'external_api_client'):
        raise ValueError("External API clients are not allowed - use CSV data only")
```

### **2. Response Validation**
```python
def _validate_response(self, response: Dict[str, Any]) -> bool:
    """Validate that response includes CSV data source."""
    if "data_source" not in response:
        raise ValueError("All agent responses must include 'data_source' field")
    
    if response["data_source"] != "CSV":
        raise ValueError("All agent responses must use 'data_source': 'CSV'")
    
    return True
```

## 📋 **Compliance Checklist**

### **✅ Agent Implementation Checklist**
- [ ] Agent uses `CSVDataSource` class
- [ ] Agent initialized with `csv_data_source` parameter
- [ ] All data access methods use CSV data source
- [ ] CSV column names mapped to expected fields
- [ ] All responses include `"data_source": "CSV"`
- [ ] No external API calls or database connections
- [ ] Data validation implemented
- [ ] Error handling for missing CSV files

### **✅ CSV File Checklist**
- [ ] `suppliers.csv` exists with required columns
- [ ] `inventory.csv` exists with required columns
- [ ] `orders.csv` exists with required columns
- [ ] `logistics.csv` exists with required columns
- [ ] All CSV files have proper headers
- [ ] Data types are consistent
- [ ] No missing required fields

## 🎯 **Benefits of CSV-Only Rule**

### **✅ Consistency**
- **Uniform data access** across all agents
- **Predictable data structure** and format
- **Easier testing** and debugging

### **✅ Reliability**
- **No external dependencies** on APIs or databases
- **Offline operation** possible
- **Data integrity** guaranteed

### **✅ Simplicity**
- **Easy to understand** and maintain
- **Simple data model** for all agents
- **Clear data flow** and processing

### **✅ Performance**
- **Fast data access** from local files
- **No network latency** or API rate limits
- **Efficient processing** of structured data

## 🚨 **Violation Consequences**

### **❌ Code Rejection**
- Any agent that doesn't use CSV data source will be **rejected**
- External API calls will cause **runtime errors**
- Missing CSV data source will **fail initialization**

### **❌ Runtime Errors**
- `ValueError: CSV data source is required for all agents`
- `FileNotFoundError: Required CSV file not found`
- `ValueError: All agent responses must use 'data_source': 'CSV'`

## 🎉 **Summary**

**ALL AGENTS MUST:**
1. ✅ Use `CSVDataSource` class exclusively
2. ✅ Load data from CSV files in `./mock_data/` directory
3. ✅ Map CSV columns to expected field names
4. ✅ Include `"data_source": "CSV"` in all responses
5. ✅ Validate CSV data integrity
6. ✅ Handle missing CSV files gracefully

**NO EXCEPTIONS** - This rule applies to all specialized agents in the system! 🚀
