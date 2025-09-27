export interface ChecklistItem {
  id: string;
  text: string;
  done: boolean;
  proposed: boolean;
}

export interface LinkItem {
  title: string;
  url: string;
}

export type CardType = "project" | "entity" | "note" | "chart" | "supplier" | "inventory" | "order" | "logistics";

export interface ProjectData {
  field1: string; // text
  field2: string; // select
  field3: string; // date
  field4: ChecklistItem[]; // checklist
  field4_id: number; // id counter
}

export interface EntityData {
  field1: string; // text
  field2: string; // select
  field3: string[]; // tags
  field3_options: string[]; // options
}

export interface NoteData {
  field1?: string; // textarea
}

export interface ChartMetric {
  id: string;
  label: string;
  value: number | ""; // 0..100
}

export interface ChartData {
  field1: ChartMetric[]; // metrics
  field1_id: number; // id counter
}

// Supply Chain Data Interfaces
export interface SupplierData {
  field1: string; // name
  field2: string; // category
  field3: number; // rating (1-5)
  field4: string; // lastRatedDate (YYYY-MM-DD format)
}

export interface InventoryData {
  field1: string; // product name
  field2: string; // SKU/part number
  field3: number; // current stock level
  field4: number; // minimum stock level
  field5: number; // maximum stock level
  field6: number; // reorder point
  field7: string; // unit of measure
  field8: number; // unit cost
  field9: string; // supplier
  field10: string; // location/warehouse
  field11: number; // lead time (days)
  field12: string; // status (in stock, low stock, out of stock)
}

export interface OrderData {
  field1: string; // order number
  field2: string; // supplier
  field3: string; // order date
  field4: string; // expected delivery date
  field5: string; // status (pending, confirmed, shipped, delivered, cancelled)
  field6: number; // total amount
  field7: string; // currency
  field8: string[]; // items ordered
  field9: string; // priority (low, medium, high, urgent)
  field10: string; // notes/special instructions
}

export interface LogisticsData {
  field1: string; // shipment ID
  field2: string; // carrier/transport company
  field3: string; // origin location
  field4: string; // destination location
  field5: string; // shipping date
  field6: string; // expected arrival date
  field7: string; // status (picked up, in transit, delivered, delayed)
  field8: string; // tracking number
  field9: number; // shipping cost
  field10: string; // shipping method (ground, air, sea)
  field11: string; // special handling requirements
  field12: number; // weight/volume
}

export type ItemData = ProjectData | EntityData | NoteData | ChartData | SupplierData | InventoryData | OrderData | LogisticsData;

export interface Item {
  id: string;
  type: CardType;
  name: string; // editable title
  subtitle: string; // subtitle shown under the title
  data: ItemData;
}

export interface AgentState {
  items: Item[];
  globalTitle: string;
  globalDescription: string;
  lastAction?: string;
  itemsCreated: number;
  syncSheetId?: string; // Google Sheet ID for auto-sync
  syncSheetName?: string; // Google Sheet name that was imported from
}




