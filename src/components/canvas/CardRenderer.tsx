"use client";

import { cn } from "@/lib/utils";
import { X, Plus } from "lucide-react";
import TextareaAutosize from "react-textarea-autosize";
import { Progress } from "@/components/ui/progress";
import type { ChartData, EntityData, Item, ItemData, NoteData, ProjectData, SupplierData, InventoryData, OrderData, LogisticsData } from "@/lib/canvas/types";
import { chartAddField1Metric, chartRemoveField1Metric, chartSetField1Label, chartSetField1Value, projectAddField4Item, projectRemoveField4Item, projectSetField4ItemDone, projectSetField4ItemText } from "@/lib/canvas/updates";

export function CardRenderer(props: {
  item: Item;
  onUpdateData: (updater: (prev: ItemData) => ItemData) => void;
  onToggleTag: (tag: string) => void;
}) {
  const { item, onUpdateData, onToggleTag } = props;

  if (item.type === "note") {
    const d = item.data as NoteData;
    return (
      <div className="mt-4">
        <label className="mb-1 block text-xs font-medium text-gray-500">Field 1 (textarea)</label>
        <TextareaAutosize
          value={d.field1 ?? ""}
          onChange={(e) => onUpdateData(() => ({ field1: e.target.value }))}
          placeholder="Write note..."
          className="min-h-40 w-full resize-none rounded-md border bg-white/60 p-3 text-sm leading-6 outline-none placeholder:text-gray-400 transition-colors hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent focus:placeholder:text-accent/65"
          minRows={6}
        />
      </div>
    );
  }

  if (item.type === "chart") {
    const d = item.data as ChartData;
    return (
      <div className="mt-4">
        <div className="mb-2 flex items-center justify-between">
          <span className="text-sm font-medium">Field 1 (metrics)</span>
          <button
            type="button"
            className="inline-flex items-center gap-1 text-xs font-medium text-accent hover:underline"
            onClick={() => onUpdateData((prev) => chartAddField1Metric(prev as ChartData, "", "").next)}
          >
            <Plus className="size-3.5" />
            Add new
          </button>
        </div>
        <div className="space-y-3">
          {(!d.field1 || d.field1.length === 0) && (
            <div className="grid place-items-center py-1.75 text-xs text-primary/50 font-medium text-pretty">
              Nothing here yet. Add a metric to get started.
            </div>
          )}
          {d.field1.map((m, i) => {
            const number = String(m.id ?? String(i + 1)).padStart(3, "0");
            return (
            <div key={m.id ?? `metric-${i}`} className="flex items-center gap-3">
              <span className="text-xs font-mono text-muted-foreground/80">{number}</span>
              <input
                value={m.label}
                placeholder="Metric label"
                onChange={(e) => onUpdateData((prev) => chartSetField1Label(prev as ChartData, i, e.target.value))}
                className="w-25 rounded-md border px-2 py-1 text-sm outline-none transition-colors placeholder:text-gray-400 hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent focus:placeholder:text-accent/65"
              />
              <div className="flex items-center gap-3 flex-1">
                <Progress value={m.value || 0} />
              </div>
              <input
                className={cn(
                  "w-10 rounded-md border px-2 py-1 text-xs outline-none appearance-none [-moz-appearance:textfield]",
                  "[&::-webkit-outer-spin-button]:[-webkit-appearance:none] [&::-webkit-outer-spin-button]:m-0",
                  "[&::-webkit-inner-spin-button]:[-webkit-appearance:none] [&::-webkit-inner-spin-button]:m-0",
                  "transition-colors hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm",
                  "focus:bg-accent/10 focus:text-accent font-mono",
                )}
                type="number"
                min={0}
                max={100}
                value={m.value}
                onChange={(e) => onUpdateData((prev) => chartSetField1Value(prev as ChartData, i, e.target.value === "" ? "" : Number(e.target.value)))}
                placeholder="0"
              />
              <button
                type="button"
                aria-label="Delete metric"
                className="text-gray-400 hover:text-accent"
                onClick={() => onUpdateData((prev) => chartRemoveField1Metric(prev as ChartData, i))}
              >
                <X className="h-5 w-5 md:h-6 md:w-6" />
              </button>
            </div>
          );})}
        </div>
      </div>
    );
  }

  if (item.type === "project") {
    const d = item.data as ProjectData;
    const set = (partial: Partial<ProjectData>) => onUpdateData((prev) => ({ ...(prev as ProjectData), ...partial }));
    return (
      <div className="mt-4 @container">
        <div className="mb-3">
          <label className="mb-1 block text-xs font-medium text-gray-500">Field 1 (Text)</label>
          <input
            value={d.field1}
            onChange={(e) => set({ field1: e.target.value })}
            className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors placeholder:text-gray-400 hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent focus:placeholder:text-accent/65"
            placeholder="Field 1 value"
          />
        </div>
        <div className="contents @xs:grid gap-3 md:grid-cols-2">
          <div className="@max-xs:mb-3">
            <label className="mb-1 block text-xs font-medium text-gray-500">Field 2 (Select)</label>
            <select
              value={d.field2}
              onChange={(e) => set({ field2: e.target.value })}
              required
              className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent invalid:text-gray-400"
            >
              <option value="">Select...</option>
              {["Option A", "Option B", "Option C"].map((opt) => (
                <option key={opt} value={opt}>{opt}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="mb-1 block text-xs font-medium text-gray-500">Field 3 (Date)</label>
            <input
              type="date"
              value={d.field3}
              onChange={(e) => set({ field3: e.target.value })}
              required
              className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent invalid:text-gray-400"
            />
          </div>
        </div>
        <div className="mt-4">
          <div className="mb-2 flex items-center justify-between">
            <label className="block text-xs font-medium text-gray-500">Field 4 (checklist)</label>
            <button
              type="button"
              className="inline-flex items-center gap-1 text-xs font-medium text-accent hover:underline"
              onClick={() => onUpdateData((prev) => projectAddField4Item(prev as ProjectData, "").next)}
            >
              <Plus className="size-3.5" />
              Add new
            </button>
          </div>
          <div className="space-y-2">
            {(!d.field4 || d.field4.length === 0) && (
              <div className="grid place-items-center py-1.75 text-xs text-primary/50 font-medium text-pretty">
                Nothing here yet. Add a checklist item to get started.
              </div>
            )}
            {(d.field4 ?? []).map((c, i) => (
              <div key={c.id} className="flex items-center gap-3">
                <span className="text-xs font-mono text-muted-foreground/80">{String(c.id ?? String(i + 1)).padStart(3, "0")}</span>
                <input
                  type="checkbox"
                  checked={!!c.done}
                  onChange={(e) => onUpdateData((prev) => projectSetField4ItemDone(prev as ProjectData, c.id, e.target.checked))}
                  className="h-4 w-4"
                />
                <input
                  value={c.text}
                  placeholder="Checklist item label"
                  onChange={(e) => onUpdateData((prev) => projectSetField4ItemText(prev as ProjectData, c.id, e.target.value))}
                  className="flex-1 rounded-md border px-2 py-1 text-sm outline-none transition-colors placeholder:text-gray-400 hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:bg-accent/10 focus:text-accent focus:placeholder:text-accent/65"
                />
                <button
                  type="button"
                  aria-label="Delete checklist item"
                  className="text-gray-400 hover:text-accent"
                  onClick={() => onUpdateData((prev) => projectRemoveField4Item(prev as ProjectData, c.id))}
                >
                  <X className="h-5 w-5 md:h-6 md:w-6" />
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  // Supply Chain Card Types
  if (item.type === "supplier") {
    const d = item.data as SupplierData;
    const set = (partial: Partial<SupplierData>) => onUpdateData((prev) => ({ ...(prev as SupplierData), ...partial }));
    return (
      <div className="mt-4 @container">
        <div className="mb-3">
          <label className="mb-1 block text-xs font-medium text-gray-500">Company Name</label>
          <input
            value={d.field1}
            onChange={(e) => set({ field1: e.target.value })}
            className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors placeholder:text-gray-400 hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent focus:placeholder:text-accent/65"
            placeholder="Supplier company name"
          />
        </div>
        <div className="contents @xs:grid gap-3 md:grid-cols-2">
          <div className="@max-xs:mb-3">
            <label className="mb-1 block text-xs font-medium text-gray-500">Category</label>
            <select
              value={d.field2}
              onChange={(e) => set({ field2: e.target.value })}
              className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent"
            >
              <option value="">Select category...</option>
              {["raw materials", "components", "services", "logistics"].map((opt) => (
                <option key={opt} value={opt}>{opt}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="mb-1 block text-xs font-medium text-gray-500">Location/Region</label>
            <input
              value={d.field3}
              onChange={(e) => set({ field3: e.target.value })}
              className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors placeholder:text-gray-400 hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent focus:placeholder:text-accent/65"
              placeholder="Location or region"
            />
          </div>
        </div>
        <div className="contents @xs:grid gap-3 md:grid-cols-2">
          <div className="@max-xs:mb-3">
            <label className="mb-1 block text-xs font-medium text-gray-500">Reliability Score (0-100)</label>
            <input
              type="number"
              min="0"
              max="100"
              value={d.field5}
              onChange={(e) => set({ field5: Number(e.target.value) })}
              className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors placeholder:text-gray-400 hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent focus:placeholder:text-accent/65"
              placeholder="0-100"
            />
          </div>
          <div>
            <label className="mb-1 block text-xs font-medium text-gray-500">Risk Level</label>
            <select
              value={d.field10}
              onChange={(e) => set({ field10: e.target.value })}
              className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent"
            >
              <option value="">Select risk level...</option>
              {["low", "medium", "high"].map((opt) => (
                <option key={opt} value={opt}>{opt}</option>
              ))}
            </select>
          </div>
        </div>
        <div className="mt-3">
          <label className="mb-1 block text-xs font-medium text-gray-500">Contact Information</label>
          <input
            value={d.field6}
            onChange={(e) => set({ field6: e.target.value })}
            className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors placeholder:text-gray-400 hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent focus:placeholder:text-accent/65"
            placeholder="Contact email, phone, address"
          />
        </div>
      </div>
    );
  }

  if (item.type === "inventory") {
    const d = item.data as InventoryData;
    const set = (partial: Partial<InventoryData>) => onUpdateData((prev) => ({ ...(prev as InventoryData), ...partial }));
    return (
      <div className="mt-4 @container">
        <div className="mb-3">
          <label className="mb-1 block text-xs font-medium text-gray-500">Product Name</label>
          <input
            value={d.field1}
            onChange={(e) => set({ field1: e.target.value })}
            className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors placeholder:text-gray-400 hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent focus:placeholder:text-accent/65"
            placeholder="Product name"
          />
        </div>
        <div className="contents @xs:grid gap-3 md:grid-cols-2">
          <div className="@max-xs:mb-3">
            <label className="mb-1 block text-xs font-medium text-gray-500">SKU/Part Number</label>
            <input
              value={d.field2}
              onChange={(e) => set({ field2: e.target.value })}
              className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors placeholder:text-gray-400 hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent focus:placeholder:text-accent/65"
              placeholder="SKU or part number"
            />
          </div>
          <div>
            <label className="mb-1 block text-xs font-medium text-gray-500">Status</label>
            <select
              value={d.field12}
              onChange={(e) => set({ field12: e.target.value })}
              className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent"
            >
              <option value="">Select status...</option>
              {["in stock", "low stock", "out of stock", "overstock"].map((opt) => (
                <option key={opt} value={opt}>{opt}</option>
              ))}
            </select>
          </div>
        </div>
        <div className="contents @xs:grid gap-3 md:grid-cols-3">
          <div className="@max-xs:mb-3">
            <label className="mb-1 block text-xs font-medium text-gray-500">Current Stock</label>
            <input
              type="number"
              value={d.field3}
              onChange={(e) => set({ field3: Number(e.target.value) })}
              className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors placeholder:text-gray-400 hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent focus:placeholder:text-accent/65"
              placeholder="Current stock level"
            />
          </div>
          <div>
            <label className="mb-1 block text-xs font-medium text-gray-500">Min Stock</label>
            <input
              type="number"
              value={d.field4}
              onChange={(e) => set({ field4: Number(e.target.value) })}
              className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors placeholder:text-gray-400 hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent focus:placeholder:text-accent/65"
              placeholder="Minimum stock"
            />
          </div>
          <div>
            <label className="mb-1 block text-xs font-medium text-gray-500">Max Stock</label>
            <input
              type="number"
              value={d.field5}
              onChange={(e) => set({ field5: Number(e.target.value) })}
              className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors placeholder:text-gray-400 hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent focus:placeholder:text-accent/65"
              placeholder="Maximum stock"
            />
          </div>
        </div>
        <div className="contents @xs:grid gap-3 md:grid-cols-2">
          <div className="@max-xs:mb-3">
            <label className="mb-1 block text-xs font-medium text-gray-500">Unit Cost</label>
            <input
              type="number"
              step="0.01"
              value={d.field8}
              onChange={(e) => set({ field8: Number(e.target.value) })}
              className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors placeholder:text-gray-400 hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent focus:placeholder:text-accent/65"
              placeholder="Unit cost"
            />
          </div>
          <div>
            <label className="mb-1 block text-xs font-medium text-gray-500">Lead Time (days)</label>
            <input
              type="number"
              value={d.field11}
              onChange={(e) => set({ field11: Number(e.target.value) })}
              className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors placeholder:text-gray-400 hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent focus:placeholder:text-accent/65"
              placeholder="Lead time in days"
            />
          </div>
        </div>
      </div>
    );
  }

  if (item.type === "order") {
    const d = item.data as OrderData;
    const set = (partial: Partial<OrderData>) => onUpdateData((prev) => ({ ...(prev as OrderData), ...partial }));
    return (
      <div className="mt-4 @container">
        <div className="mb-3">
          <label className="mb-1 block text-xs font-medium text-gray-500">Order Number</label>
          <input
            value={d.field1}
            onChange={(e) => set({ field1: e.target.value })}
            className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors placeholder:text-gray-400 hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent focus:placeholder:text-accent/65"
            placeholder="Order number"
          />
        </div>
        <div className="contents @xs:grid gap-3 md:grid-cols-2">
          <div className="@max-xs:mb-3">
            <label className="mb-1 block text-xs font-medium text-gray-500">Supplier</label>
            <input
              value={d.field2}
              onChange={(e) => set({ field2: e.target.value })}
              className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors placeholder:text-gray-400 hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent focus:placeholder:text-accent/65"
              placeholder="Supplier name"
            />
          </div>
          <div>
            <label className="mb-1 block text-xs font-medium text-gray-500">Status</label>
            <select
              value={d.field5}
              onChange={(e) => set({ field5: e.target.value })}
              className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent"
            >
              <option value="">Select status...</option>
              {["pending", "confirmed", "shipped", "delivered", "cancelled", "delayed"].map((opt) => (
                <option key={opt} value={opt}>{opt}</option>
              ))}
            </select>
          </div>
        </div>
        <div className="contents @xs:grid gap-3 md:grid-cols-2">
          <div className="@max-xs:mb-3">
            <label className="mb-1 block text-xs font-medium text-gray-500">Order Date</label>
            <input
              type="date"
              value={d.field3}
              onChange={(e) => set({ field3: e.target.value })}
              className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent"
            />
          </div>
          <div>
            <label className="mb-1 block text-xs font-medium text-gray-500">Expected Delivery</label>
            <input
              type="date"
              value={d.field4}
              onChange={(e) => set({ field4: e.target.value })}
              className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent"
            />
          </div>
        </div>
        <div className="contents @xs:grid gap-3 md:grid-cols-3">
          <div className="@max-xs:mb-3">
            <label className="mb-1 block text-xs font-medium text-gray-500">Total Amount</label>
            <input
              type="number"
              step="0.01"
              value={d.field6}
              onChange={(e) => set({ field6: Number(e.target.value) })}
              className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors placeholder:text-gray-400 hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent focus:placeholder:text-accent/65"
              placeholder="Total amount"
            />
          </div>
          <div>
            <label className="mb-1 block text-xs font-medium text-gray-500">Currency</label>
            <select
              value={d.field7}
              onChange={(e) => set({ field7: e.target.value })}
              className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent"
            >
              <option value="">Select currency...</option>
              {["USD", "EUR", "GBP", "CAD", "AUD"].map((opt) => (
                <option key={opt} value={opt}>{opt}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="mb-1 block text-xs font-medium text-gray-500">Priority</label>
            <select
              value={d.field9}
              onChange={(e) => set({ field9: e.target.value })}
              className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent"
            >
              <option value="">Select priority...</option>
              {["low", "medium", "high", "urgent"].map((opt) => (
                <option key={opt} value={opt}>{opt}</option>
              ))}
            </select>
          </div>
        </div>
        <div className="mt-3">
          <label className="mb-1 block text-xs font-medium text-gray-500">Notes/Special Instructions</label>
          <TextareaAutosize
            value={d.field10}
            onChange={(e) => set({ field10: e.target.value })}
            placeholder="Special instructions or notes..."
            className="min-h-20 w-full resize-none rounded-md border bg-white/60 p-3 text-sm leading-6 outline-none placeholder:text-gray-400 transition-colors hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent focus:placeholder:text-accent/65"
            minRows={3}
          />
        </div>
      </div>
    );
  }

  if (item.type === "logistics") {
    const d = item.data as LogisticsData;
    const set = (partial: Partial<LogisticsData>) => onUpdateData((prev) => ({ ...(prev as LogisticsData), ...partial }));
    return (
      <div className="mt-4 @container">
        <div className="mb-3">
          <label className="mb-1 block text-xs font-medium text-gray-500">Shipment ID</label>
          <input
            value={d.field1}
            onChange={(e) => set({ field1: e.target.value })}
            className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors placeholder:text-gray-400 hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent focus:placeholder:text-accent/65"
            placeholder="Shipment ID"
          />
        </div>
        <div className="contents @xs:grid gap-3 md:grid-cols-2">
          <div className="@max-xs:mb-3">
            <label className="mb-1 block text-xs font-medium text-gray-500">Carrier/Transport Company</label>
            <input
              value={d.field2}
              onChange={(e) => set({ field2: e.target.value })}
              className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors placeholder:text-gray-400 hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent focus:placeholder:text-accent/65"
              placeholder="Carrier name"
            />
          </div>
          <div>
            <label className="mb-1 block text-xs font-medium text-gray-500">Status</label>
            <select
              value={d.field7}
              onChange={(e) => set({ field7: e.target.value })}
              className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent"
            >
              <option value="">Select status...</option>
              {["picked up", "in transit", "delivered", "delayed"].map((opt) => (
                <option key={opt} value={opt}>{opt}</option>
              ))}
            </select>
          </div>
        </div>
        <div className="contents @xs:grid gap-3 md:grid-cols-2">
          <div className="@max-xs:mb-3">
            <label className="mb-1 block text-xs font-medium text-gray-500">Origin Location</label>
            <input
              value={d.field3}
              onChange={(e) => set({ field3: e.target.value })}
              className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors placeholder:text-gray-400 hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent focus:placeholder:text-accent/65"
              placeholder="Origin location"
            />
          </div>
          <div>
            <label className="mb-1 block text-xs font-medium text-gray-500">Destination Location</label>
            <input
              value={d.field4}
              onChange={(e) => set({ field4: e.target.value })}
              className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors placeholder:text-gray-400 hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent focus:placeholder:text-accent/65"
              placeholder="Destination location"
            />
          </div>
        </div>
        <div className="contents @xs:grid gap-3 md:grid-cols-2">
          <div className="@max-xs:mb-3">
            <label className="mb-1 block text-xs font-medium text-gray-500">Shipping Date</label>
            <input
              type="date"
              value={d.field5}
              onChange={(e) => set({ field5: e.target.value })}
              className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent"
            />
          </div>
          <div>
            <label className="mb-1 block text-xs font-medium text-gray-500">Expected Arrival</label>
            <input
              type="date"
              value={d.field6}
              onChange={(e) => set({ field6: e.target.value })}
              className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent"
            />
          </div>
        </div>
        <div className="contents @xs:grid gap-3 md:grid-cols-3">
          <div className="@max-xs:mb-3">
            <label className="mb-1 block text-xs font-medium text-gray-500">Tracking Number</label>
            <input
              value={d.field8}
              onChange={(e) => set({ field8: e.target.value })}
              className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors placeholder:text-gray-400 hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent focus:placeholder:text-accent/65"
              placeholder="Tracking number"
            />
          </div>
          <div>
            <label className="mb-1 block text-xs font-medium text-gray-500">Shipping Cost</label>
            <input
              type="number"
              step="0.01"
              value={d.field9}
              onChange={(e) => set({ field9: Number(e.target.value) })}
              className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors placeholder:text-gray-400 hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent focus:placeholder:text-accent/65"
              placeholder="Shipping cost"
            />
          </div>
          <div>
            <label className="mb-1 block text-xs font-medium text-gray-500">Shipping Method</label>
            <select
              value={d.field10}
              onChange={(e) => set({ field10: e.target.value })}
              className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent"
            >
              <option value="">Select method...</option>
              {["ground", "air", "sea"].map((opt) => (
                <option key={opt} value={opt}>{opt}</option>
              ))}
            </select>
          </div>
        </div>
        <div className="mt-3">
          <label className="mb-1 block text-xs font-medium text-gray-500">Special Handling Requirements</label>
          <TextareaAutosize
            value={d.field11}
            onChange={(e) => set({ field11: e.target.value })}
            placeholder="Special handling requirements..."
            className="min-h-20 w-full resize-none rounded-md border bg-white/60 p-3 text-sm leading-6 outline-none placeholder:text-gray-400 transition-colors hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent focus:placeholder:text-accent/65"
            minRows={3}
          />
        </div>
      </div>
    );
  }

  const e = item.data as EntityData;
  const setEntity = (partial: Partial<EntityData>) => onUpdateData((prev) => ({ ...(prev as EntityData), ...partial }));
  return (
    <div className="mt-4">
      <div className="mb-3">
        <label className="mb-1 block text-xs font-medium text-gray-500">Field 1 (Text)</label>
        <input
          value={e.field1}
          onChange={(ev) => setEntity({ field1: ev.target.value })}
          className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors placeholder:text-gray-400 hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent focus:placeholder:text-accent/65"
          placeholder="Field 1 value"
        />
      </div>
      <div className="mb-3">
        <label className="mb-1 block text-xs font-medium text-gray-500">Field 2 (Select)</label>
        <select
          value={e.field2}
          onChange={(ev) => setEntity({ field2: ev.target.value })}
          required
          className="w-full rounded-md border px-2 py-1.5 text-sm outline-none transition-colors hover:ring-1 hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10 focus:text-accent invalid:text-gray-400"
        >
          <option value="">Select...</option>
          {["Option A", "Option B", "Option C"].map((opt) => (
            <option key={opt} value={opt}>{opt}</option>
          ))}
        </select>
      </div>
      <div className="mt-4">
        <label className="mb-1 block text-xs font-medium text-gray-500">Field 3 (Tags)</label>
        <div className="flex flex-wrap gap-2">
          {(e.field3_options ?? []).map((t) => {
            const active = (e.field3 ?? []).includes(t);
            return (
              <button
                key={t}
                onClick={() => onToggleTag(t)}
                className={cn(
                  "inline-flex items-center gap-1 rounded-full border px-2 py-0.5 text-xs",
                  active ? "bg-accent/20 border-accent text-accent" : "text-gray-600"
                )}
              >
                {t}
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export default CardRenderer;




