"""
📊 CSV Data Source Manager
Supplementary CSV data source for all agents to access supplier information.
Agents can use this alongside external APIs, databases, and other data sources.
"""

import pandas as pd
import os
from typing import Dict, List, Any, Optional
from pathlib import Path
import json

class CSVDataSource:
    """Centralized CSV data source for all agents."""
    
    def __init__(self, csv_dir: str = "./mock_data"):
        self.csv_dir = Path(csv_dir)
        self.supplier_data = None
        self.inventory_data = None
        self.order_data = None
        self.logistics_data = None
        
        # Load all CSV data on initialization
        self._load_all_csv_data()
    
    def _load_all_csv_data(self):
        """Load all CSV data from the mock_data directory."""
        try:
            # Load supplier data
            supplier_csv = self.csv_dir / "suppliers.csv"
            if supplier_csv.exists():
                self.supplier_data = pd.read_csv(supplier_csv)
                print(f"✅ Loaded supplier data: {len(self.supplier_data)} records")
            else:
                print(f"❌ Supplier CSV not found: {supplier_csv}")
            
            # Load inventory data
            inventory_csv = self.csv_dir / "inventory.csv"
            if inventory_csv.exists():
                self.inventory_data = pd.read_csv(inventory_csv)
                print(f"✅ Loaded inventory data: {len(self.inventory_data)} records")
            else:
                print(f"❌ Inventory CSV not found: {inventory_csv}")
            
            # Load order data
            order_csv = self.csv_dir / "orders.csv"
            if order_csv.exists():
                self.order_data = pd.read_csv(order_csv)
                print(f"✅ Loaded order data: {len(self.order_data)} records")
            else:
                print(f"❌ Order CSV not found: {order_csv}")
            
            # Load logistics data
            logistics_csv = self.csv_dir / "logistics.csv"
            if logistics_csv.exists():
                self.logistics_data = pd.read_csv(logistics_csv)
                print(f"✅ Loaded logistics data: {len(self.logistics_data)} records")
            else:
                print(f"❌ Logistics CSV not found: {logistics_csv}")
                
        except Exception as e:
            print(f"❌ Error loading CSV data: {e}")
    
    def get_supplier_data(self, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Get supplier data from CSV with optional filters."""
        if self.supplier_data is None:
            return []
        
        df = self.supplier_data.copy()
        
        # Apply filters if provided
        if filters:
            for column, value in filters.items():
                if column in df.columns:
                    if isinstance(value, list):
                        df = df[df[column].isin(value)]
                    else:
                        df = df[df[column] == value]
        
        return df.to_dict('records')
    
    def get_inventory_data(self, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Get inventory data from CSV with optional filters."""
        if self.inventory_data is None:
            return []
        
        df = self.inventory_data.copy()
        
        # Apply filters if provided
        if filters:
            for column, value in filters.items():
                if column in df.columns:
                    if isinstance(value, list):
                        df = df[df[column].isin(value)]
                    else:
                        df = df[df[column] == value]
        
        return df.to_dict('records')
    
    def get_order_data(self, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Get order data from CSV with optional filters."""
        if self.order_data is None:
            return []
        
        df = self.order_data.copy()
        
        # Apply filters if provided
        if filters:
            for column, value in filters.items():
                if column in df.columns:
                    if isinstance(value, list):
                        df = df[df[column].isin(value)]
                    else:
                        df = df[df[column] == value]
        
        return df.to_dict('records')
    
    def get_logistics_data(self, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Get logistics data from CSV with optional filters."""
        if self.logistics_data is None:
            return []
        
        df = self.logistics_data.copy()
        
        # Apply filters if provided
        if filters:
            for column, value in filters.items():
                if column in df.columns:
                    if isinstance(value, list):
                        df = df[df[column].isin(value)]
                    else:
                        df = df[df[column] == value]
        
        return df.to_dict('records')
    
    def get_supplier_by_id(self, supplier_id: str) -> Optional[Dict[str, Any]]:
        """Get specific supplier by ID."""
        if self.supplier_data is None:
            return None
        
        supplier = self.supplier_data[self.supplier_data['ID'] == supplier_id]
        if not supplier.empty:
            return supplier.iloc[0].to_dict()
        return None
    
    def get_supplier_by_name(self, supplier_name: str) -> Optional[Dict[str, Any]]:
        """Get specific supplier by name."""
        if self.supplier_data is None:
            return None
        
        supplier = self.supplier_data[self.supplier_data['Name'] == supplier_name]
        if not supplier.empty:
            return supplier.iloc[0].to_dict()
        return None
    
    def get_suppliers_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get suppliers by category."""
        return self.get_supplier_data(filters={"Category": category})
    
    def get_suppliers_by_location(self, location: str) -> List[Dict[str, Any]]:
        """Get suppliers by location."""
        return self.get_supplier_data(filters={"Location": location})
    
    def get_suppliers_by_reliability(self, min_score: float = 0.0) -> List[Dict[str, Any]]:
        """Get suppliers with minimum reliability score."""
        if self.supplier_data is None:
            return []
        
        df = self.supplier_data.copy()
        df['Reliability Score'] = pd.to_numeric(df['Reliability Score'], errors='coerce')
        reliable_suppliers = df[df['Reliability Score'] >= min_score]
        return reliable_suppliers.to_dict('records')
    
    def get_inventory_by_supplier(self, supplier_name: str) -> List[Dict[str, Any]]:
        """Get inventory items from specific supplier."""
        return self.get_inventory_data(filters={"Supplier": supplier_name})
    
    def get_orders_by_supplier(self, supplier_name: str) -> List[Dict[str, Any]]:
        """Get orders from specific supplier."""
        return self.get_order_data(filters={"Supplier": supplier_name})
    
    def get_logistics_by_supplier(self, supplier_name: str) -> List[Dict[str, Any]]:
        """Get logistics data for specific supplier."""
        return self.get_logistics_data(filters={"Carrier": supplier_name})
    
    def search_suppliers(self, query: str) -> List[Dict[str, Any]]:
        """Search suppliers by name, company, or products."""
        if self.supplier_data is None:
            return []
        
        df = self.supplier_data.copy()
        query_lower = query.lower()
        
        # Search in multiple columns
        mask = (
            df['Name'].str.lower().str.contains(query_lower, na=False) |
            df['Company Name'].str.lower().str.contains(query_lower, na=False) |
            df['Products'].str.lower().str.contains(query_lower, na=False)
        )
        
        return df[mask].to_dict('records')
    
    def get_data_summary(self) -> Dict[str, Any]:
        """Get summary of all CSV data."""
        summary = {
            "supplier_count": len(self.supplier_data) if self.supplier_data is not None else 0,
            "inventory_count": len(self.inventory_data) if self.inventory_data is not None else 0,
            "order_count": len(self.order_data) if self.order_data is not None else 0,
            "logistics_count": len(self.logistics_data) if self.logistics_data is not None else 0,
            "csv_files_loaded": []
        }
        
        # Check which CSV files are loaded
        csv_files = ["suppliers.csv", "inventory.csv", "orders.csv", "logistics.csv"]
        for csv_file in csv_files:
            if (self.csv_dir / csv_file).exists():
                summary["csv_files_loaded"].append(csv_file)
        
        return summary
    
    def refresh_data(self):
        """Refresh all CSV data from disk."""
        print("🔄 Refreshing CSV data...")
        self._load_all_csv_data()
        print("✅ CSV data refreshed")
    
    def validate_data_integrity(self) -> Dict[str, Any]:
        """Validate CSV data integrity."""
        validation_results = {
            "supplier_data": {"valid": True, "issues": []},
            "inventory_data": {"valid": True, "issues": []},
            "order_data": {"valid": True, "issues": []},
            "logistics_data": {"valid": True, "issues": []}
        }
        
        # Validate supplier data
        if self.supplier_data is not None:
            required_columns = ["ID", "Name", "Company Name", "Category", "Location", "Reliability Score"]
            missing_columns = [col for col in required_columns if col not in self.supplier_data.columns]
            if missing_columns:
                validation_results["supplier_data"]["valid"] = False
                validation_results["supplier_data"]["issues"].append(f"Missing columns: {missing_columns}")
        
        # Validate inventory data
        if self.inventory_data is not None:
            required_columns = ["ID", "Name", "Product Name", "Current Stock", "Supplier"]
            missing_columns = [col for col in required_columns if col not in self.inventory_data.columns]
            if missing_columns:
                validation_results["inventory_data"]["valid"] = False
                validation_results["inventory_data"]["issues"].append(f"Missing columns: {missing_columns}")
        
        return validation_results
