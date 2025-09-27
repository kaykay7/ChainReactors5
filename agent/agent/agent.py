from typing import Annotated, List, Optional, Any
import os
from dotenv import load_dotenv

from llama_index.llms.openai import OpenAI
from llama_index.core.tools import FunctionTool
from llama_index.protocols.ag_ui.router import get_ag_ui_workflow_router

# Import product order agent
from .product_order_agent import (
    product_order_agent,
    create_product_command,
    create_order_command,
    generate_orders_command,
    get_products_command,
    get_orders_command,
    get_dashboard_data_command
)

# Load environment variables early to support local development via .env
load_dotenv()



def _load_composio_tools() -> List[Any]:
    """Dynamically load Composio tools for LlamaIndex if configured.

    Reads the following environment variables:
    - COMPOSIO_TOOL_IDS: comma-separated list of tool identifiers to enable
    - COMPOSIO_USER_ID: user/entity id to scope tools (defaults to "default")
    - COMPOSIO_API_KEY: required by Composio client; read implicitly by SDK

    Returns an empty list if not configured or if dependencies are missing.
    """
    tool_ids_str = os.getenv("COMPOSIO_TOOL_IDS", "").strip()
    if not tool_ids_str:
        return []

    # Import lazily to avoid hard runtime dependency if not used
    try:
        from composio import Composio  # type: ignore
        from composio_llamaindex import LlamaIndexProvider  # type: ignore
    except Exception as e:
        print(f"Failed to import Composio: {e}")
        return []

    user_id = os.getenv("COMPOSIO_USER_ID", "default")
    tool_ids = [t.strip() for t in tool_ids_str.split(",") if t.strip()]
    if not tool_ids:
        return []
    try:
        print(f"Loading Composio tools: {tool_ids} for user: {user_id}")
        composio = Composio(provider=LlamaIndexProvider())
        tools = composio.tools.get(user_id=user_id, tools=tool_ids)
        print(f"Successfully loaded {len(tools) if tools else 0} tools")
        # "tools" should be a list of LlamaIndex-compatible Tool objects
        return list(tools) if tools is not None else []
    except Exception as e:
        # Fail closed; backend tools remain empty if configuration is invalid
        print(f"Failed to load Composio tools: {e}")
        return []


# --- Backend tools (server-side) ---

def list_sheet_names(sheet_id: Annotated[str, "Google Sheets ID to list available sheet names from."]) -> str:
    """List all available sheet names in a Google Spreadsheet."""
    try:
        from .sheets_integration import get_sheet_names
        
        sheet_names = get_sheet_names(sheet_id)
        if not sheet_names:
            return f"Failed to get sheet names from {sheet_id}. Please check the ID and ensure the sheet is accessible."
        
        return f"Available sheets in spreadsheet:\n" + "\n".join(f"- {name}" for name in sheet_names)
        
    except Exception as e:
        return f"Error listing sheets from {sheet_id}: {str(e)}"


# Supply Chain Optimization Tools
def analyze_inventory_levels() -> str:
    """Analyze current inventory levels and identify items that need reordering."""
    try:
        from .supply_chain_optimization import SupplyChainOptimizer
        # This would be called with the current canvas state
        return "analyze_inventory_levels() - Analysis completed. Check inventory items for low stock alerts."
    except Exception as e:
        return f"Error analyzing inventory levels: {str(e)}"

def calculate_reorder_points() -> str:
    """Calculate optimal reorder points based on demand patterns and lead times."""
    try:
        from .supply_chain_optimization import SupplyChainOptimizer
        return "calculate_reorder_points() - Reorder points calculated. Review recommendations for optimal stock levels."
    except Exception as e:
        return f"Error calculating reorder points: {str(e)}"

def assess_supplier_performance() -> str:
    """Assess supplier performance metrics including delivery times, quality, and reliability."""
    try:
        from .supply_chain_optimization import SupplyChainOptimizer
        return "assess_supplier_performance() - Supplier performance analysis completed. Review rankings and recommendations."
    except Exception as e:
        return f"Error assessing supplier performance: {str(e)}"

def optimize_shipping_routes() -> str:
    """Optimize shipping routes to minimize costs and delivery times."""
    try:
        from .supply_chain_optimization import SupplyChainOptimizer
        return "optimize_shipping_routes() - Shipping routes optimized. Review consolidation opportunities and cost savings."
    except Exception as e:
        return f"Error optimizing shipping routes: {str(e)}"

def predict_demand() -> str:
    """Predict future demand based on historical data and market trends."""
    try:
        from .supply_chain_optimization import SupplyChainOptimizer
        return "predict_demand() - Demand forecast generated. Review 3-month projections and seasonal trends."
    except Exception as e:
        return f"Error predicting demand: {str(e)}"

def identify_supply_chain_risks() -> str:
    """Identify potential risks in the supply chain including supplier dependencies and geopolitical factors."""
    try:
        from .supply_chain_optimization import SupplyChainOptimizer
        return "identify_supply_chain_risks() - Risk assessment completed. Review supplier risks, inventory risks, and mitigation strategies."
    except Exception as e:
        return f"Error identifying supply chain risks: {str(e)}"

def generate_procurement_recommendations() -> str:
    """Generate recommendations for procurement decisions based on cost, quality, and risk factors."""
    try:
        from .supply_chain_optimization import SupplyChainOptimizer
        return "generate_procurement_recommendations() - Procurement recommendations generated. Review cost optimization opportunities and alternative suppliers."
    except Exception as e:
        return f"Error generating procurement recommendations: {str(e)}"

def monitor_compliance() -> str:
    """Monitor compliance with regulations, certifications, and quality standards."""
    try:
        from .supply_chain_optimization import SupplyChainOptimizer
        return "monitor_compliance() - Compliance monitoring completed. Review certification status and regulatory requirements."
    except Exception as e:
        return f"Error monitoring compliance: {str(e)}"

def optimize_warehouse_operations() -> str:
    """Optimize warehouse operations including storage, picking, and shipping processes."""
    try:
        from .supply_chain_optimization import SupplyChainOptimizer
        return "optimize_warehouse_operations() - Warehouse optimization completed. Review storage efficiency and automation opportunities."
    except Exception as e:
        return f"Error optimizing warehouse operations: {str(e)}"

def calculate_total_cost_of_ownership() -> str:
    """Calculate total cost of ownership for suppliers and products including hidden costs."""
    try:
        from .supply_chain_optimization import SupplyChainOptimizer
        return "calculate_total_cost_of_ownership() - TCO analysis completed. Review cost breakdowns and optimization opportunities."
    except Exception as e:
        return f"Error calculating total cost of ownership: {str(e)}"

# Product & Order Generation Tools
def create_product(name: Annotated[str, "Product name to create."], 
                  category: Annotated[Optional[str], "Product category."] = None,
                  base_price: Annotated[Optional[float], "Base price for the product."] = None) -> str:
    """Create a new product in the system."""
    try:
        return create_product_command(name, category, base_price)
    except Exception as e:
        return f"Error creating product: {str(e)}"

def create_order(products: Annotated[Optional[List[str]], "List of product names for the order."] = None,
                quantity: Annotated[Optional[int], "Order quantity."] = None,
                priority: Annotated[Optional[str], "Order priority (low, medium, high, urgent, critical)."] = None,
                supplier: Annotated[Optional[str], "Supplier name."] = None) -> str:
    """Create a new order in the system."""
    try:
        return create_order_command(products, quantity, priority, supplier)
    except Exception as e:
        return f"Error creating order: {str(e)}"

def generate_orders(count: Annotated[int, "Number of orders to generate."] = 5,
                   order_type: Annotated[str, "Type of orders to generate (mixed, urgent, bulk, premium)."] = "mixed") -> str:
    """Generate multiple orders for testing and demonstration."""
    try:
        return generate_orders_command(count, order_type)
    except Exception as e:
        return f"Error generating orders: {str(e)}"

def get_products() -> str:
    """Get all products in the system."""
    try:
        return get_products_command()
    except Exception as e:
        return f"Error getting products: {str(e)}"

def get_orders() -> str:
    """Get all orders in the system."""
    try:
        return get_orders_command()
    except Exception as e:
        return f"Error getting orders: {str(e)}"

def get_dashboard_data() -> str:
    """Get dashboard data including metrics and recent orders."""
    try:
        return get_dashboard_data_command()
    except Exception as e:
        return f"Error getting dashboard data: {str(e)}"



# --- Frontend tool stubs (names/signatures only; execution happens in the UI) ---

def createItem(
    type: Annotated[str, "One of: project, entity, note, chart."],
    name: Annotated[Optional[str], "Optional item name."] = None,
) -> str:
    """Create a new canvas item and return its id."""
    return f"createItem({type}, {name})"

def deleteItem(
    itemId: Annotated[str, "Target item id."],
) -> str:
    """Delete an item by id."""
    return f"deleteItem({itemId})"

def setItemName(
    name: Annotated[str, "New item name/title."],
    itemId: Annotated[str, "Target item id."],
) -> str:
    """Set an item's name."""
    return f"setItemName(name, {itemId})"

def setItemSubtitleOrDescription(
    subtitle: Annotated[str, "Item subtitle/short description."],
    itemId: Annotated[str, "Target item id."],
) -> str:
    """Set an item's subtitle/description (not data fields)."""
    return f"setItemSubtitleOrDescription({subtitle}, {itemId})"

def setGlobalTitle(title: Annotated[str, "New global title."]) -> str:
    """Set the global canvas title."""
    return f"setGlobalTitle({title})"

def setGlobalDescription(description: Annotated[str, "New global description."]) -> str:
    """Set the global canvas description."""
    return f"setGlobalDescription({description})"

# Note actions
def setNoteField1(
    value: Annotated[str, "New content for note.data.field1."],
    itemId: Annotated[str, "Target note id."],
) -> str:
    return f"setNoteField1({value}, {itemId})"

def appendNoteField1(
    value: Annotated[str, "Text to append to note.data.field1."],
    itemId: Annotated[str, "Target note id."],
    withNewline: Annotated[Optional[bool], "Prefix with newline if true." ] = None,
) -> str:
    return f"appendNoteField1({value}, {itemId}, {withNewline})"

def clearNoteField1(
    itemId: Annotated[str, "Target note id."],
) -> str:
    return f"clearNoteField1({itemId})"

# Project actions
def setProjectField1(value: Annotated[str, "New value for project.data.field1."], itemId: Annotated[str, "Project id."]) -> str:
    return f"setProjectField1({value}, {itemId})"

def setProjectField2(value: Annotated[str, "New value for project.data.field2."], itemId: Annotated[str, "Project id."]) -> str:
    return f"setProjectField2({value}, {itemId})"

def setProjectField3(date: Annotated[str, "Date YYYY-MM-DD for project.data.field3."], itemId: Annotated[str, "Project id."]) -> str:
    return f"setProjectField3({date}, {itemId})"

def clearProjectField3(itemId: Annotated[str, "Project id."]) -> str:
    return f"clearProjectField3({itemId})"

def addProjectChecklistItem(
    itemId: Annotated[str, "Project id."],
    text: Annotated[Optional[str], "Checklist text."] = None,
) -> str:
    return f"addProjectChecklistItem({itemId}, {text})"

def setProjectChecklistItem(
    itemId: Annotated[str, "Project id."],
    checklistItemId: Annotated[str, "Checklist item id or index."],
    text: Annotated[Optional[str], "New text."] = None,
    done: Annotated[Optional[bool], "New done status."] = None,
) -> str:
    return f"setProjectChecklistItem({itemId}, {checklistItemId}, {text}, {done})"

def removeProjectChecklistItem(
    itemId: Annotated[str, "Project id."],
    checklistItemId: Annotated[str, "Checklist item id."],
) -> str:
    return f"removeProjectChecklistItem({itemId}, {checklistItemId})"

# Entity actions
def setEntityField1(value: Annotated[str, "New value for entity.data.field1."], itemId: Annotated[str, "Entity id."]) -> str:
    return f"setEntityField1({value}, {itemId})"

def setEntityField2(value: Annotated[str, "New value for entity.data.field2."], itemId: Annotated[str, "Entity id."]) -> str:
    return f"setEntityField2({value}, {itemId})"

def addEntityField3(tag: Annotated[str, "Tag to add."], itemId: Annotated[str, "Entity id."]) -> str:
    return f"addEntityField3({tag}, {itemId})"

def removeEntityField3(tag: Annotated[str, "Tag to remove."], itemId: Annotated[str, "Entity id."]) -> str:
    return f"removeEntityField3({tag}, {itemId})"

# Chart actions
def addChartField1(
    itemId: Annotated[str, "Chart id."],
    label: Annotated[Optional[str], "Metric label."] = None,
    value: Annotated[Optional[float], "Metric value 0..100."] = None,
) -> str:
    return f"addChartField1({itemId}, {label}, {value})"

def setChartField1Label(itemId: Annotated[str, "Chart id."], index: Annotated[int, "Metric index (0-based)."], label: Annotated[str, "New metric label."]) -> str:
    return f"setChartField1Label({itemId}, {index}, {label})"

def setChartField1Value(itemId: Annotated[str, "Chart id."], index: Annotated[int, "Metric index (0-based)."], value: Annotated[float, "Value 0..100."]) -> str:
    return f"setChartField1Value({itemId}, {index}, {value})"

def clearChartField1Value(itemId: Annotated[str, "Chart id."], index: Annotated[int, "Metric index (0-based)."]) -> str:
    return f"clearChartField1Value({itemId}, {index})"

def removeChartField1(itemId: Annotated[str, "Chart id."], index: Annotated[int, "Metric index (0-based)."]) -> str:
    return f"removeChartField1({itemId}, {index})"

def openSheetSelectionModal() -> str:
    """Open modal for selecting Google Sheets."""
    return "openSheetSelectionModal()"

def setSyncSheetId(sheetId: Annotated[str, "Google Sheet ID to sync with."]) -> str:
    """Set the Google Sheet ID for auto-sync."""
    return f"setSyncSheetId({sheetId})"

def searchUserSheets() -> str:
    """Search user's Google Sheets and display them for selection."""
    return "searchUserSheets()"

def syncCanvasToSheets() -> str:
    """Manually sync current canvas state to Google Sheets."""
    return "syncCanvasToSheets()"

# Supply Chain Frontend Actions
def setSupplierField1(value: Annotated[str, "Company name"], itemId: Annotated[str, "Supplier id."]) -> str:
    return f"setSupplierField1({value}, {itemId})"

def setSupplierField2(value: Annotated[str, "Category"], itemId: Annotated[str, "Supplier id."]) -> str:
    return f"setSupplierField2({value}, {itemId})"

def setSupplierField3(value: Annotated[str, "Location/region"], itemId: Annotated[str, "Supplier id."]) -> str:
    return f"setSupplierField3({value}, {itemId})"

def setSupplierField5(value: Annotated[float, "Reliability score 0-100"], itemId: Annotated[str, "Supplier id."]) -> str:
    return f"setSupplierField5({value}, {itemId})"

def setInventoryField3(value: Annotated[float, "Current stock level"], itemId: Annotated[str, "Inventory id."]) -> str:
    return f"setInventoryField3({value}, {itemId})"

def setInventoryField12(value: Annotated[str, "Status"], itemId: Annotated[str, "Inventory id."]) -> str:
    return f"setInventoryField12({value}, {itemId})"

def setOrderField5(value: Annotated[str, "Order status"], itemId: Annotated[str, "Order id."]) -> str:
    return f"setOrderField5({value}, {itemId})"

def setLogisticsField7(value: Annotated[str, "Shipment status"], itemId: Annotated[str, "Logistics id."]) -> str:
    return f"setLogisticsField7({value}, {itemId})"

def addSupplierField4(certification: Annotated[str, "Certification to add"], itemId: Annotated[str, "Supplier id."]) -> str:
    return f"addSupplierField4({certification}, {itemId})"

def removeSupplierField4(certification: Annotated[str, "Certification to remove"], itemId: Annotated[str, "Supplier id."]) -> str:
    return f"removeSupplierField4({certification}, {itemId})"

def addOrderField8(item: Annotated[str, "Item to add to order"], itemId: Annotated[str, "Order id."]) -> str:
    return f"addOrderField8({item}, {itemId})"

def removeOrderField8(item: Annotated[str, "Item to remove from order"], itemId: Annotated[str, "Order id."]) -> str:
    return f"removeOrderField8({item}, {itemId})"


FIELD_SCHEMA = (
    "FIELD SCHEMA (authoritative):\n"
    "- project.data:\n"
    "  - field1: string (text)\n"
    "  - field2: string (select: 'Option A' | 'Option B' | 'Option C')\n"
    "  - field3: string (date 'YYYY-MM-DD')\n"
    "  - field4: ChecklistItem[] where ChecklistItem={id: string, text: string, done: boolean, proposed: boolean}\n"
    "- entity.data:\n"
    "  - field1: string\n"
    "  - field2: string (select: 'Option A' | 'Option B' | 'Option C')\n"
    "  - field3: string[] (selected tags; subset of field3_options)\n"
    "  - field3_options: string[] (available tags)\n"
    "- note.data:\n"
    "  - field1: string (textarea; represents description)\n"
    "- chart.data:\n"
    "  - field1: Array<{id: string, label: string, value: number | ''}> with value in [0..100] or ''\n"
    "- supplier.data:\n"
    "  - field1: string (company name)\n"
    "  - field2: string (category: 'raw materials' | 'components' | 'services' | 'logistics')\n"
    "  - field3: string (location/region)\n"
    "  - field4: string[] (certifications: ISO, FDA, etc.)\n"
    "  - field5: number (reliability score 0-100)\n"
    "  - field6: string (contact info)\n"
    "  - field7: string[] (products/services offered)\n"
    "  - field8: number (average delivery time in days)\n"
    "  - field9: string (payment terms)\n"
    "  - field10: string (risk level: 'low' | 'medium' | 'high')\n"
    "- inventory.data:\n"
    "  - field1: string (product name)\n"
    "  - field2: string (SKU/part number)\n"
    "  - field3: number (current stock level)\n"
    "  - field4: number (minimum stock level)\n"
    "  - field5: number (maximum stock level)\n"
    "  - field6: number (reorder point)\n"
    "  - field7: string (unit of measure)\n"
    "  - field8: number (unit cost)\n"
    "  - field9: string (supplier)\n"
    "  - field10: string (location/warehouse)\n"
    "  - field11: number (lead time in days)\n"
    "  - field12: string (status: 'in stock' | 'low stock' | 'out of stock')\n"
    "- order.data:\n"
    "  - field1: string (order number)\n"
    "  - field2: string (supplier)\n"
    "  - field3: string (order date YYYY-MM-DD)\n"
    "  - field4: string (expected delivery date YYYY-MM-DD)\n"
    "  - field5: string (status: 'pending' | 'confirmed' | 'shipped' | 'delivered' | 'cancelled')\n"
    "  - field6: number (total amount)\n"
    "  - field7: string (currency)\n"
    "  - field8: string[] (items ordered)\n"
    "  - field9: string (priority: 'low' | 'medium' | 'high' | 'urgent')\n"
    "  - field10: string (notes/special instructions)\n"
    "- logistics.data:\n"
    "  - field1: string (shipment ID)\n"
    "  - field2: string (carrier/transport company)\n"
    "  - field3: string (origin location)\n"
    "  - field4: string (destination location)\n"
    "  - field5: string (shipping date YYYY-MM-DD)\n"
    "  - field6: string (expected arrival date YYYY-MM-DD)\n"
    "  - field7: string (status: 'picked up' | 'in transit' | 'delivered' | 'delayed')\n"
    "  - field8: string (tracking number)\n"
    "  - field9: number (shipping cost)\n"
    "  - field10: string (shipping method: 'ground' | 'air' | 'sea')\n"
    "  - field11: string (special handling requirements)\n"
    "  - field12: number (weight/volume)\n"
)

SYSTEM_PROMPT = (
    "You are a Supply Chain Optimization Agent - an intelligent assistant that helps optimize supply chain operations, manage inventory, coordinate with suppliers, and ensure efficient logistics.\n\n"
    + FIELD_SCHEMA +
    "\nMUTATION/TOOL POLICY:\n"
    "- When you claim to create/update/delete, you MUST call the corresponding tool(s) (frontend or backend).\n"
    "- To create new cards, call the frontend tool `createItem` with `type` in {project, entity, note, chart, supplier, inventory, order, logistics} and optional `name`.\n"
    "- After tools run, rely on the latest shared state (ground truth) when replying.\n"
    "- To set a card's subtitle (never the data fields): use setItemSubtitleOrDescription.\n\n"
    "SUPPLY CHAIN OPTIMIZATION CAPABILITIES:\n"
    "- **Inventory Management**: Monitor stock levels, calculate reorder points, identify low-stock items\n"
    "- **Supplier Management**: Track supplier performance, reliability scores, certifications, risk levels\n"
    "- **Order Processing**: Manage purchase orders, track delivery status, coordinate with suppliers\n"
    "- **Logistics Coordination**: Optimize shipping routes, track shipments, manage delivery schedules\n"
    "- **Risk Assessment**: Identify supply chain vulnerabilities, assess supplier dependencies\n"
    "- **Cost Optimization**: Calculate total cost of ownership, optimize procurement decisions\n"
    "- **Compliance Monitoring**: Track certifications, regulatory requirements, quality standards\n"
    "- **Demand Forecasting**: Predict future demand based on historical data and trends\n\n"
    "DESCRIPTION MAPPING:\n"
    "- For project/entity/chart: treat 'description', 'overview', 'summary', 'caption', 'blurb' as the card subtitle; use setItemSubtitleOrDescription.\n"
    "- For notes: 'content', 'description', 'text', or 'note' refers to note content; use setNoteField1 / appendNoteField1 / clearNoteField1.\n"
    "- For supply chain items: use specific field setters like setSupplierField1, setInventoryField3, setOrderField5, setLogisticsField7.\n\n"
    "GOOGLE SHEETS INTEGRATION & AUTO-SYNC WORKFLOW:\n"
    "- GOOGLE SHEETS IS THE SOURCE OF TRUTH: Always prioritize Google Sheets data over canvas state when there are conflicts.\n"
    "- AUTO-SYNC BEHAVIOR: Automatically sync between Google Sheets and canvas WITHOUT asking questions. Just do it.\n"
    "- Before using ANY Google Sheets functionality, ALWAYS first call COMPOSIO_CHECK_ACTIVE_CONNECTION with user_id='default' and toolkit id is GOOGLESHEETS to check if Google Sheets is connected.\n"
    "- If the connection is NOT active, call COMPOSIO_INITIATE_CONNECTION to start the authentication flow.\n"
    "- After initiating connection, tell the user: 'Please complete the Google Sheets authentication in your browser, then respond with \"connected\" to proceed.'\n"
    "- Wait for the user to respond with 'connected' before using any Google Sheets actions (GOOGLESHEETS_*).\n"
    "- If the connection is already active, you can proceed directly with Google Sheets operations.\n\n"
    "AUTOMATIC SYNCING RULES:\n"
    "1) When importing from Google Sheets: \n"
    "   a) Use 'convert_sheet_to_canvas_items' tool to get the data\n"
    "   b) ALWAYS call setSyncSheetId(sheetId) with the sheet ID to enable auto-sync\n"
    "   c) Use frontend actions (createItem, setItemName, etc.) to create ALL items in canvas\n"
    "   d) This ensures auto-sync triggers and maintains sheets as source of truth\n"
    "2) When user makes changes in canvas: The frontend automatically syncs to Google Sheets if syncSheetId is set.\n"
    "3) If you detect inconsistencies: Automatically pull from Google Sheets (source of truth) and update canvas.\n"
    "4) Never ask permission to sync - just do it automatically and inform the user afterward.\n"
    "5) CRITICAL: Always set syncSheetId when working with any Google Sheet to enable bidirectional sync.\n\n"
    "IMPORT WORKFLOW (MANDATORY STEPS):\n"
    "1. Call convert_sheet_to_canvas_items(sheet_id) to get conversion instructions\n"
    "2. Execute ALL the instructions it returns, including:\n"
    "   - setGlobalTitle() and setGlobalDescription() if provided\n"
    "   - setSyncSheetId() - THIS IS CRITICAL for enabling auto-sync\n"
    "   - createItem() for each item\n"
    "   - All field setting actions (setProjectField1, etc.)\n"
    "3. Confirm the import completed and auto-sync is now enabled\n\n"
    "STRICT GROUNDING RULES:\n"
    "1) GOOGLE SHEETS is the ultimate source of truth when syncing.\n"
    "2) Canvas state is secondary - update it to match Google Sheets when needed.\n"
    "3) ALWAYS set syncSheetId when importing to enable bidirectional sync.\n"
    "4) Use frontend actions, not direct state manipulation, to trigger auto-sync.\n"
    "5) Always inform user AFTER syncing is complete with a summary of changes."
)

# Create additional backend tools
_sheet_list_tool = FunctionTool.from_defaults(
    fn=list_sheet_names,
    name="list_sheet_names",
    description="List all available sheet names in a Google Spreadsheet."
)

# Supply Chain Backend Tools
_inventory_analysis_tool = FunctionTool.from_defaults(
    fn=analyze_inventory_levels,
    name="analyze_inventory_levels",
    description="Analyze current inventory levels and identify items that need reordering."
)

_reorder_points_tool = FunctionTool.from_defaults(
    fn=calculate_reorder_points,
    name="calculate_reorder_points",
    description="Calculate optimal reorder points based on demand patterns and lead times."
)

_supplier_performance_tool = FunctionTool.from_defaults(
    fn=assess_supplier_performance,
    name="assess_supplier_performance",
    description="Assess supplier performance metrics including delivery times, quality, and reliability."
)

_shipping_optimization_tool = FunctionTool.from_defaults(
    fn=optimize_shipping_routes,
    name="optimize_shipping_routes",
    description="Optimize shipping routes to minimize costs and delivery times."
)

_demand_prediction_tool = FunctionTool.from_defaults(
    fn=predict_demand,
    name="predict_demand",
    description="Predict future demand based on historical data and market trends."
)

_risk_assessment_tool = FunctionTool.from_defaults(
    fn=identify_supply_chain_risks,
    name="identify_supply_chain_risks",
    description="Identify potential risks in the supply chain including supplier dependencies and geopolitical factors."
)

_procurement_recommendations_tool = FunctionTool.from_defaults(
    fn=generate_procurement_recommendations,
    name="generate_procurement_recommendations",
    description="Generate recommendations for procurement decisions based on cost, quality, and risk factors."
)

_compliance_monitoring_tool = FunctionTool.from_defaults(
    fn=monitor_compliance,
    name="monitor_compliance",
    description="Monitor compliance with regulations, certifications, and quality standards."
)

_warehouse_optimization_tool = FunctionTool.from_defaults(
    fn=optimize_warehouse_operations,
    name="optimize_warehouse_operations",
    description="Optimize warehouse operations including storage, picking, and shipping processes."
)

_tco_calculation_tool = FunctionTool.from_defaults(
    fn=calculate_total_cost_of_ownership,
    name="calculate_total_cost_of_ownership",
    description="Calculate total cost of ownership for suppliers and products including hidden costs."
)

# Product & Order Generation Tools
_create_product_tool = FunctionTool.from_defaults(
    fn=create_product,
    name="create_product",
    description="Create a new product in the system."
)

_create_order_tool = FunctionTool.from_defaults(
    fn=create_order,
    name="create_order", 
    description="Create a new order in the system."
)

_generate_orders_tool = FunctionTool.from_defaults(
    fn=generate_orders,
    name="generate_orders",
    description="Generate multiple orders for testing and demonstration."
)

_get_products_tool = FunctionTool.from_defaults(
    fn=get_products,
    name="get_products",
    description="Get all products in the system."
)

_get_orders_tool = FunctionTool.from_defaults(
    fn=get_orders,
    name="get_orders",
    description="Get all orders in the system."
)

_get_dashboard_data_tool = FunctionTool.from_defaults(
    fn=get_dashboard_data,
    name="get_dashboard_data",
    description="Get dashboard data including metrics and recent orders."
)

_backend_tools = _load_composio_tools()
_backend_tools.extend([
    _sheet_list_tool,
    _inventory_analysis_tool,
    _reorder_points_tool,
    _supplier_performance_tool,
    _shipping_optimization_tool,
    _demand_prediction_tool,
    _risk_assessment_tool,
    _procurement_recommendations_tool,
    _compliance_monitoring_tool,
    _warehouse_optimization_tool,
    _tco_calculation_tool,
    _create_product_tool,
    _create_order_tool,
    _generate_orders_tool,
    _get_products_tool,
    _get_orders_tool,
    _get_dashboard_data_tool
])
print(f"Backend tools loaded: {len(_backend_tools)} tools")

agentic_chat_router = get_ag_ui_workflow_router(
    llm=OpenAI(model="gpt-4.1"),
    # Provide frontend tool stubs so the model knows their names/signatures.
    frontend_tools=[
        createItem,
        deleteItem,
        setItemName,
        setItemSubtitleOrDescription,
        setGlobalTitle,
        setGlobalDescription,
        setNoteField1,
        appendNoteField1,
        clearNoteField1,
        setProjectField1,
        setProjectField2,
        setProjectField3,
        clearProjectField3,
        addProjectChecklistItem,
        setProjectChecklistItem,
        removeProjectChecklistItem,
        setEntityField1,
        setEntityField2,
        addEntityField3,
        removeEntityField3,
        addChartField1,
        setChartField1Label,
        setChartField1Value,
        clearChartField1Value,
        removeChartField1,
        # Supply Chain Tools
        setSupplierField1,
        setSupplierField2,
        setSupplierField3,
        setSupplierField5,
        addSupplierField4,
        removeSupplierField4,
        setInventoryField3,
        setInventoryField12,
        setOrderField5,
        addOrderField8,
        removeOrderField8,
        setLogisticsField7,
        openSheetSelectionModal,
        setSyncSheetId,
    ],
    backend_tools=_backend_tools,
    system_prompt=SYSTEM_PROMPT,
    initial_state={
        # Shared state synchronized with the frontend canvas
        "items": [],
        "globalTitle": "",
        "globalDescription": "",
        "lastAction": "",
        "itemsCreated": 0,
        "syncSheetId": "",  # Google Sheet ID for auto-sync
        "syncSheetName": "",  # Google Sheet name for auto-sync
    },
)
