#!/usr/bin/env python3
"""
Generate canvas data from separate CSV files for each supply chain category.

This script reads the separate CSV files (suppliers.csv, inventory.csv, orders.csv, logistics.csv)
and converts them to the proper canvas format.
"""

import csv
import json
import sys
from typing import Dict, List, Any
from pathlib import Path

def convert_csv_to_canvas(csv_file_path: str, item_type: str) -> List[Dict[str, Any]]:
    """
    Convert a single CSV file to canvas format.
    
    Args:
        csv_file_path: Path to the CSV file
        item_type: Type of items (supplier, inventory, order, logistics)
        
    Returns:
        List of canvas items
    """
    items = []
    item_id = 1
    
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
    
    return items

def main():
    """Main function to convert separate CSV files to canvas format."""
    print("🚀 Converting separate CSV files to canvas format...")
    
    # Define the CSV files and their types
    csv_files = [
        ('suppliers.csv', 'supplier'),
        ('inventory.csv', 'inventory'),
        ('orders.csv', 'order'),
        ('logistics.csv', 'logistics')
    ]
    
    all_items = []
    
    for csv_file, item_type in csv_files:
        csv_path = Path(__file__).parent / csv_file
        
        if not csv_path.exists():
            print(f"❌ CSV file not found: {csv_path}")
            continue
        
        try:
            items = convert_csv_to_canvas(str(csv_path), item_type)
            all_items.extend(items)
            print(f"✅ Converted {csv_file}: {len(items)} {item_type} items")
        except Exception as e:
            print(f"❌ Error converting {csv_file}: {e}")
            continue
    
    if not all_items:
        print("❌ No items converted")
        return
    
    # Create the canvas data structure
    canvas_data = {
        "items": all_items,
        "globalTitle": "Supply Chain Management Dashboard",
        "globalDescription": "Comprehensive supply chain optimization with AI-powered insights and real-time monitoring",
        "lastAction": "imported_from_separate_csvs",
        "itemsCreated": len(all_items),
        "syncSheetId": "",
        "syncSheetName": ""
    }
    
    # Save to JSON file
    output_file = Path(__file__).parent / "supply_chain_canvas_data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(canvas_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Successfully converted all CSV files to canvas format")
    print(f"📊 Created {len(all_items)} total items")
    print(f"💾 Saved to: {output_file}")
    
    # Print summary
    item_types = {}
    for item in all_items:
        item_type = item['type']
        item_types[item_type] = item_types.get(item_type, 0) + 1
    
    print("\n📈 Item Summary:")
    for item_type, count in item_types.items():
        print(f"  - {item_type}: {count} items")
    
    print(f"\n🎯 Next Steps:")
    print(f"1. Use the JSON data from: {output_file}")
    print(f"2. Or create separate Google Sheets using create_separate_sheets.py")
    print(f"3. Import the data into your Supply Chain Optimization Agent")

if __name__ == "__main__":
    main()
