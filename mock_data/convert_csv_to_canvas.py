#!/usr/bin/env python3
"""
Convert CSV data to canvas format for the Supply Chain Optimization Agent.

This script reads the mock CSV data and converts it to the proper canvas format
that can be imported into the application.
"""

import csv
import json
import sys
from typing import Dict, List, Any
from pathlib import Path

def convert_csv_to_canvas(csv_file_path: str) -> Dict[str, Any]:
    """
    Convert CSV data to canvas format.
    
    Args:
        csv_file_path: Path to the CSV file
        
    Returns:
        Dictionary with canvas state structure
    """
    items = []
    item_id = 1
    
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            item_type = row['Type'].lower()
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
                        "field4": row['Reliability Score'].split(';') if row['Reliability Score'] else [],
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
                        "field6": int(row['Min Stock']) if row['Min Stock'].isdigit() else 0,  # Reorder point
                        "field7": "units",
                        "field8": float(row['Unit Cost']) if row['Unit Cost'] else 0.0,
                        "field9": row['Supplier'],
                        "field10": "Warehouse A",
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
                        "field2": row['Supplier Name'],
                        "field3": row['Order Date'],
                        "field4": row['Expected Delivery'],
                        "field5": row['Order Status'],
                        "field6": float(row['Total Amount']) if row['Total Amount'] else 0.0,
                        "field7": row['Currency'],
                        "field8": ["Product A", "Product B"],  # Default items
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
                        "field3": row['Origin'],
                        "field4": row['Destination'],
                        "field5": row['Shipping Date'],
                        "field6": row['Expected Arrival'],
                        "field7": row['Shipment Status'],
                        "field8": row['Tracking Number'],
                        "field9": float(row['Shipping Cost']) if row['Shipping Cost'] else 0.0,
                        "field10": row['Shipping Method'],
                        "field11": row['Special Requirements'],
                        "field12": 0  # Weight/volume placeholder
                    }
                }
            else:
                continue  # Skip unknown types
            
            items.append(item)
            item_id += 1
    
    return {
        "items": items,
        "globalTitle": "Supply Chain Management Dashboard",
        "globalDescription": "Comprehensive supply chain optimization with AI-powered insights",
        "lastAction": "imported_from_csv",
        "itemsCreated": len(items),
        "syncSheetId": "",
        "syncSheetName": ""
    }

def main():
    """Main function to convert CSV to canvas format."""
    if len(sys.argv) != 2:
        print("Usage: python convert_csv_to_canvas.py <csv_file_path>")
        sys.exit(1)
    
    csv_file_path = sys.argv[1]
    
    if not Path(csv_file_path).exists():
        print(f"Error: CSV file '{csv_file_path}' not found")
        sys.exit(1)
    
    try:
        canvas_data = convert_csv_to_canvas(csv_file_path)
        
        # Save to JSON file
        output_file = "canvas_data.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(canvas_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Successfully converted CSV to canvas format")
        print(f"📊 Created {len(canvas_data['items'])} items")
        print(f"💾 Saved to: {output_file}")
        
        # Print summary
        item_types = {}
        for item in canvas_data['items']:
            item_type = item['type']
            item_types[item_type] = item_types.get(item_type, 0) + 1
        
        print("\n📈 Item Summary:")
        for item_type, count in item_types.items():
            print(f"  - {item_type}: {count} items")
        
    except Exception as e:
        print(f"❌ Error converting CSV: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
