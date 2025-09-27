#!/usr/bin/env python3
"""
Load local CSV data directly into the Supply Chain Optimization Agent.
This bypasses Composio and Google Sheets integration.
"""

import csv
import json
import sys
from pathlib import Path
from typing import Dict, List, Any

def load_csv_data(csv_file_path: str, item_type: str) -> List[Dict[str, Any]]:
    """
    Load data from a CSV file and convert to canvas format.
    
    Args:
        csv_file_path: Path to the CSV file
        item_type: Type of items (supplier, inventory, order, logistics)
        
    Returns:
        List of canvas items
    """
    items = []
    item_id = 1
    
    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                item_id_str = f"{item_id:04d}"
                
                if item_type == 'supplier':
                    item = {
                        "id": item_id_str,
                        "type": "supplier",
                        "name": row['Name'],
                        "subtitle": row['Subtitle'],
                        "data": {
                            "field1": row['Company Name'],
                            "field2": row['Category'],
                            "field3": row['Location'],
                            "field4": row['Certifications'].split(';') if row['Certifications'] else [],
                            "field5": int(row['Reliability Score']) if row['Reliability Score'].isdigit() else 0,
                            "field6": row['Contact Info'],
                            "field7": row['Products'].split(';') if row['Products'] else [],
                            "field8": int(row['Delivery Time']) if row['Delivery Time'].isdigit() else 0,
                            "field9": row['Payment Terms'],
                            "field10": row['Risk Level']
                        }
                    }
                elif item_type == 'inventory':
                    item = {
                        "id": item_id_str,
                        "type": "inventory",
                        "name": row['Name'],
                        "subtitle": row['Subtitle'],
                        "data": {
                            "field1": row['Product Name'],
                            "field2": row['SKU'],
                            "field3": int(row['Current Stock']) if row['Current Stock'].isdigit() else 0,
                            "field4": int(row['Min Stock']) if row['Min Stock'].isdigit() else 0,
                            "field5": int(row['Max Stock']) if row['Max Stock'].isdigit() else 0,
                            "field6": int(row['Reorder Point']) if row['Reorder Point'].isdigit() else 0,
                            "field7": row['Unit of Measure'],
                            "field8": float(row['Unit Cost']) if row['Unit Cost'] else 0.0,
                            "field9": row['Supplier'],
                            "field10": row['Location'],
                            "field11": int(row['Lead Time']) if row['Lead Time'].isdigit() else 0,
                            "field12": row['Status']
                        }
                    }
                elif item_type == 'order':
                    item = {
                        "id": item_id_str,
                        "type": "order",
                        "name": row['Name'],
                        "subtitle": row['Subtitle'],
                        "data": {
                            "field1": row['Order Number'],
                            "field2": row['Supplier'],
                            "field3": row['Order Date'],
                            "field4": row['Expected Delivery'],
                            "field5": row['Status'],
                            "field6": float(row['Total Amount']) if row['Total Amount'] else 0.0,
                            "field7": row['Currency'],
                            "field8": row['Items Ordered'].split(';') if row['Items Ordered'] else [],
                            "field9": row['Priority'],
                            "field10": row['Notes']
                        }
                    }
                elif item_type == 'logistics':
                    item = {
                        "id": item_id_str,
                        "type": "logistics",
                        "name": row['Name'],
                        "subtitle": row['Subtitle'],
                        "data": {
                            "field1": row['Shipment ID'],
                            "field2": row['Carrier'],
                            "field3": row['Origin Location'],
                            "field4": row['Destination Location'],
                            "field5": row['Shipping Date'],
                            "field6": row['Expected Arrival'],
                            "field7": row['Status'],
                            "field8": row['Tracking Number'],
                            "field9": float(row['Shipping Cost']) if row['Shipping Cost'] else 0.0,
                            "field10": row['Shipping Method'],
                            "field11": row['Special Requirements'],
                            "field12": int(row['Weight/Volume']) if row['Weight/Volume'].isdigit() else 0
                        }
                    }
                else:
                    continue  # Skip unknown types
                
                items.append(item)
                item_id += 1
                
    except Exception as e:
        print(f"❌ Error loading {csv_file_path}: {e}")
        return []
    
    return items

def load_all_local_data():
    """Load all local CSV data and create canvas format."""
    print("🚀 Loading local CSV data...")
    
    # Define the CSV files and their types
    csv_files = [
        ('mock_data/suppliers.csv', 'supplier'),
        ('mock_data/inventory.csv', 'inventory'),
        ('mock_data/orders.csv', 'order'),
        ('mock_data/logistics.csv', 'logistics')
    ]
    
    all_items = []
    
    for csv_file, item_type in csv_files:
        csv_path = Path(csv_file)
        
        if not csv_path.exists():
            print(f"❌ CSV file not found: {csv_path}")
            continue
        
        try:
            items = load_csv_data(str(csv_path), item_type)
            all_items.extend(items)
            print(f"✅ Loaded {csv_file}: {len(items)} {item_type} items")
        except Exception as e:
            print(f"❌ Error loading {csv_file}: {e}")
            continue
    
    if not all_items:
        print("❌ No items loaded")
        return None
    
    # Create the canvas data structure
    canvas_data = {
        "items": all_items,
        "globalTitle": "Supply Chain Management Dashboard",
        "globalDescription": "Comprehensive supply chain optimization with AI-powered insights and real-time monitoring",
        "lastAction": "loaded_from_local_csv",
        "itemsCreated": len(all_items),
        "syncSheetId": "",
        "syncSheetName": ""
    }
    
    return canvas_data

def save_canvas_data(canvas_data: Dict[str, Any], output_file: str = "local_canvas_data.json"):
    """Save canvas data to JSON file."""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(canvas_data, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved canvas data to: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error saving canvas data: {e}")
        return False

def main():
    """Main function to load local data."""
    print("🚀 Loading local CSV data into canvas format...")
    print("=" * 50)
    
    # Load all data
    canvas_data = load_all_local_data()
    
    if not canvas_data:
        print("❌ Failed to load data")
        return
    
    # Save to JSON file
    if save_canvas_data(canvas_data):
        print(f"\n✅ Successfully loaded {len(canvas_data['items'])} items")
        
        # Print summary
        item_types = {}
        for item in canvas_data['items']:
            item_type = item['type']
            item_types[item_type] = item_types.get(item_type, 0) + 1
        
        print("\n📈 Item Summary:")
        for item_type, count in item_types.items():
            print(f"  - {item_type}: {count} items")
        
        print(f"\n🎯 Next Steps:")
        print(f"1. Use the JSON data from: local_canvas_data.json")
        print(f"2. Import it into your Supply Chain Optimization Agent")
        print(f"3. Or use it to populate the canvas directly")
    
    else:
        print("❌ Failed to save canvas data")

if __name__ == "__main__":
    main()
