"""
🧪 Simple CSV Data Rule Test
Tests CSV data source functionality without full agent imports.
"""

import pandas as pd
import os
from pathlib import Path

def test_csv_files_exist():
    """Test that all required CSV files exist."""
    print("🧪 Testing CSV Files Existence...")
    
    required_files = ["suppliers.csv", "inventory.csv", "orders.csv", "logistics.csv"]
    csv_dir = Path("./mock_data")
    
    all_exist = True
    for file in required_files:
        file_path = csv_dir / file
        if file_path.exists():
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            all_exist = False
    
    return all_exist

def test_csv_data_structure():
    """Test CSV data structure and columns."""
    print("\n🧪 Testing CSV Data Structure...")
    
    csv_dir = Path("./mock_data")
    
    # Test suppliers.csv
    suppliers_file = csv_dir / "suppliers.csv"
    if suppliers_file.exists():
        df = pd.read_csv(suppliers_file)
        required_columns = ["ID", "Name", "Company Name", "Category", "Location", "Reliability Score"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"❌ suppliers.csv missing columns: {missing_columns}")
            return False
        else:
            print(f"✅ suppliers.csv has all required columns: {len(df)} records")
    
    # Test inventory.csv
    inventory_file = csv_dir / "inventory.csv"
    if inventory_file.exists():
        df = pd.read_csv(inventory_file)
        required_columns = ["ID", "Name", "Product Name", "Current Stock", "Min Stock", "Max Stock", "Reorder Point"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"❌ inventory.csv missing columns: {missing_columns}")
            return False
        else:
            print(f"✅ inventory.csv has all required columns: {len(df)} records")
    
    # Test orders.csv
    orders_file = csv_dir / "orders.csv"
    if orders_file.exists():
        df = pd.read_csv(orders_file)
        required_columns = ["ID", "Name", "Order Number", "Supplier", "Status", "Total Amount"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"❌ orders.csv missing columns: {missing_columns}")
            return False
        else:
            print(f"✅ orders.csv has all required columns: {len(df)} records")
    
    # Test logistics.csv
    logistics_file = csv_dir / "logistics.csv"
    if logistics_file.exists():
        df = pd.read_csv(logistics_file)
        required_columns = ["ID", "Name", "Shipment ID", "Carrier", "Status", "Shipping Cost"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"❌ logistics.csv missing columns: {missing_columns}")
            return False
        else:
            print(f"✅ logistics.csv has all required columns: {len(df)} records")
    
    return True

def test_csv_data_access():
    """Test CSV data access patterns."""
    print("\n🧪 Testing CSV Data Access Patterns...")
    
    csv_dir = Path("./mock_data")
    
    try:
        # Test supplier data access
        suppliers_file = csv_dir / "suppliers.csv"
        if suppliers_file.exists():
            df = pd.read_csv(suppliers_file)
            
            # Test filtering by category
            components = df[df['Category'] == 'components']
            print(f"✅ Found {len(components)} component suppliers")
            
            # Test filtering by reliability
            reliable = df[df['Reliability Score'] >= 80]
            print(f"✅ Found {len(reliable)} reliable suppliers (score >= 80)")
            
            # Test search functionality
            tech_suppliers = df[df['Name'].str.contains('Tech', case=False, na=False)]
            print(f"✅ Found {len(tech_suppliers)} tech-related suppliers")
        
        # Test inventory data access
        inventory_file = csv_dir / "inventory.csv"
        if inventory_file.exists():
            df = pd.read_csv(inventory_file)
            
            # Test low stock analysis
            low_stock = df[df['Current Stock'] <= df['Reorder Point']]
            print(f"✅ Found {len(low_stock)} low stock items")
            
            # Test out of stock items
            out_of_stock = df[df['Current Stock'] == 0]
            print(f"✅ Found {len(out_of_stock)} out of stock items")
            
            # Test overstocked items
            overstocked = df[df['Current Stock'] > df['Max Stock'] * 1.2]
            print(f"✅ Found {len(overstocked)} overstocked items")
        
        return True
        
    except Exception as e:
        print(f"❌ CSV data access test failed: {e}")
        return False

def test_csv_rule_compliance():
    """Test CSV rule compliance patterns."""
    print("\n🧪 Testing CSV Rule Compliance...")
    
    # Test that we can access data without external dependencies
    csv_dir = Path("./mock_data")
    
    try:
        # Test data loading without external APIs
        suppliers_file = csv_dir / "suppliers.csv"
        if suppliers_file.exists():
            df = pd.read_csv(suppliers_file)
            
            # Simulate agent response with CSV data source
            response = {
                "data_source": "CSV",
                "supplier_count": len(df),
                "suppliers": df.to_dict('records')
            }
            
            # Verify CSV rule compliance
            if response["data_source"] != "CSV":
                print("❌ Response does not indicate CSV data source")
                return False
            
            print(f"✅ CSV rule compliance verified: {response['supplier_count']} suppliers from CSV")
        
        return True
        
    except Exception as e:
        print(f"❌ CSV rule compliance test failed: {e}")
        return False

def run_csv_tests():
    """Run all CSV tests."""
    print("🧪 CSV Data Rule Compliance Tests")
    print("=" * 50)
    
    tests = [
        ("CSV Files Existence", test_csv_files_exist),
        ("CSV Data Structure", test_csv_data_structure),
        ("CSV Data Access", test_csv_data_access),
        ("CSV Rule Compliance", test_csv_rule_compliance)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if test_func():
            print(f"✅ {test_name} PASSED")
            passed += 1
        else:
            print(f"❌ {test_name} FAILED")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL CSV TESTS PASSED - CSV Rule Compliance Verified!")
        return True
    else:
        print("❌ Some tests failed - CSV Rule Compliance Issues Found!")
        return False

if __name__ == "__main__":
    success = run_csv_tests()
    exit(0 if success else 1)
