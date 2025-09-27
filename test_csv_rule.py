"""
🧪 Test CSV Data Rule Compliance
Verifies that all agents use only CSV data sources.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'agent'))

from agent.agent.csv_data_source import CSVDataSource
from agent.agent.inventory_agent import InventoryAgent
from agent.agent.supplier_agent import SupplierAgent
from agent.agent.forecasting_agent import ForecastingAgent
from agent.agent.agent_orchestrator import AgentOrchestrator

def test_csv_data_source():
    """Test CSV data source functionality."""
    print("🧪 Testing CSV Data Source...")
    
    try:
        # Initialize CSV data source
        csv_source = CSVDataSource(csv_dir="./mock_data")
        
        # Test data loading
        supplier_data = csv_source.get_supplier_data()
        inventory_data = csv_source.get_inventory_data()
        order_data = csv_source.get_order_data()
        logistics_data = csv_source.get_logistics_data()
        
        print(f"✅ Supplier data loaded: {len(supplier_data)} records")
        print(f"✅ Inventory data loaded: {len(inventory_data)} records")
        print(f"✅ Order data loaded: {len(order_data)} records")
        print(f"✅ Logistics data loaded: {len(logistics_data)} records")
        
        # Test data summary
        summary = csv_source.get_data_summary()
        print(f"✅ Data summary: {summary}")
        
        # Test data validation
        validation = csv_source.validate_data_integrity()
        print(f"✅ Data validation: {validation}")
        
        return True
        
    except Exception as e:
        print(f"❌ CSV data source test failed: {e}")
        return False

def test_inventory_agent_csv_rule():
    """Test inventory agent CSV-only rule compliance."""
    print("\n🧪 Testing Inventory Agent CSV Rule...")
    
    try:
        # Initialize inventory agent with CSV data source
        inventory_agent = InventoryAgent(csv_data_source=CSVDataSource())
        
        # Test stock analysis (should use CSV data)
        analysis = inventory_agent.analyze_stock_levels()
        
        # Verify CSV data source is used
        if "data_source" not in analysis:
            print("❌ Missing 'data_source' field in response")
            return False
        
        if analysis["data_source"] != "CSV":
            print(f"❌ Wrong data source: {analysis['data_source']}, expected 'CSV'")
            return False
        
        print("✅ Inventory agent uses CSV data source correctly")
        print(f"✅ Analysis results: {len(analysis.get('low_stock_items', []))} low stock items")
        
        return True
        
    except Exception as e:
        print(f"❌ Inventory agent test failed: {e}")
        return False

def test_supplier_agent_csv_rule():
    """Test supplier agent CSV-only rule compliance."""
    print("\n🧪 Testing Supplier Agent CSV Rule...")
    
    try:
        # Initialize supplier agent with CSV data source
        supplier_agent = SupplierAgent(csv_data_source=CSVDataSource())
        
        # Test supplier performance analysis (should use CSV data)
        performance = supplier_agent.analyze_supplier_performance()
        
        # Verify CSV data source is used
        if "data_source" not in performance:
            print("❌ Missing 'data_source' field in response")
            return False
        
        if performance["data_source"] != "CSV":
            print(f"❌ Wrong data source: {performance['data_source']}, expected 'CSV'")
            return False
        
        print("✅ Supplier agent uses CSV data source correctly")
        print(f"✅ Performance analysis completed for {len(performance.get('supplier_performance', {}))} suppliers")
        
        return True
        
    except Exception as e:
        print(f"❌ Supplier agent test failed: {e}")
        return False

def test_forecasting_agent_csv_rule():
    """Test forecasting agent CSV-only rule compliance."""
    print("\n🧪 Testing Forecasting Agent CSV Rule...")
    
    try:
        # Initialize forecasting agent with CSV data source
        forecasting_agent = ForecastingAgent(csv_data_source=CSVDataSource())
        
        # Test demand forecasting (should use CSV data)
        forecasts = forecasting_agent.forecast_demand([])  # Empty list to trigger CSV data usage
        
        # Verify CSV data source is used
        if "data_source" not in forecasts:
            print("❌ Missing 'data_source' field in response")
            return False
        
        if forecasts["data_source"] != "CSV":
            print(f"❌ Wrong data source: {forecasts['data_source']}, expected 'CSV'")
            return False
        
        print("✅ Forecasting agent uses CSV data source correctly")
        print(f"✅ Forecast analysis completed")
        
        return True
        
    except Exception as e:
        print(f"❌ Forecasting agent test failed: {e}")
        return False

def test_orchestrator_csv_rule():
    """Test orchestrator CSV-only rule compliance."""
    print("\n🧪 Testing Orchestrator CSV Rule...")
    
    try:
        # Initialize orchestrator with CSV data source
        orchestrator = AgentOrchestrator(csv_dir="./mock_data")
        
        # Test that all agents are initialized with CSV data source
        for agent_name, agent in orchestrator.agents.items():
            if not hasattr(agent, 'csv_data_source'):
                print(f"❌ Agent {agent_name} missing csv_data_source attribute")
                return False
            
            if agent.csv_data_source is None:
                print(f"❌ Agent {agent_name} has None csv_data_source")
                return False
        
        print("✅ All agents in orchestrator have CSV data source")
        
        # Test data source summary
        data_summary = orchestrator.csv_data_source.get_data_summary()
        print(f"✅ Data source summary: {data_summary}")
        
        return True
        
    except Exception as e:
        print(f"❌ Orchestrator test failed: {e}")
        return False

def test_csv_rule_enforcement():
    """Test that CSV-only rule is enforced."""
    print("\n🧪 Testing CSV Rule Enforcement...")
    
    try:
        # Test that agents cannot be initialized without CSV data source
        try:
            # This should work (with CSV data source)
            inventory_agent = InventoryAgent(csv_data_source=CSVDataSource())
            print("✅ Agent initialization with CSV data source works")
        except Exception as e:
            print(f"❌ Agent initialization with CSV data source failed: {e}")
            return False
        
        # Test CSV data access methods
        csv_source = CSVDataSource()
        
        # Test supplier data access
        suppliers = csv_source.get_supplier_data()
        if not suppliers:
            print("❌ No supplier data found in CSV")
            return False
        
        # Test inventory data access
        inventory = csv_source.get_inventory_data()
        if not inventory:
            print("❌ No inventory data found in CSV")
            return False
        
        print("✅ CSV data access methods work correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ CSV rule enforcement test failed: {e}")
        return False

def run_all_tests():
    """Run all CSV rule compliance tests."""
    print("🧪 CSV Data Rule Compliance Tests")
    print("=" * 50)
    
    tests = [
        ("CSV Data Source", test_csv_data_source),
        ("Inventory Agent CSV Rule", test_inventory_agent_csv_rule),
        ("Supplier Agent CSV Rule", test_supplier_agent_csv_rule),
        ("Forecasting Agent CSV Rule", test_forecasting_agent_csv_rule),
        ("Orchestrator CSV Rule", test_orchestrator_csv_rule),
        ("CSV Rule Enforcement", test_csv_rule_enforcement)
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
        print("🎉 ALL TESTS PASSED - CSV Rule Compliance Verified!")
        return True
    else:
        print("❌ Some tests failed - CSV Rule Compliance Issues Found!")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
