"use client";

import { useCoAgent, useCopilotAction, useCopilotAdditionalInstructions } from "@copilotkit/react-core";
import { CopilotKitCSSProperties, CopilotChat, CopilotPopup } from "@copilotkit/react-ui";
import { useCallback, useEffect, useRef, useState } from "react";
import type React from "react";
import { Button } from "@/components/ui/button"
import { useStreaming } from "@/hooks/useStreaming";
import { useMediaQuery } from "@/hooks/use-media-query";
import { EmptyState } from "@/components/empty-state";
import { cn } from "@/lib/utils";
import type { AgentState, Item, CardType } from "@/lib/canvas/types";
import { initialState, isNonEmptyAgentState } from "@/lib/canvas/state";
import SimpleLoadDataButton from "@/components/SimpleLoadDataButton";
import NewItemMenu from "@/components/canvas/NewItemMenu";
import CardRenderer from "@/components/canvas/CardRenderer";
import ItemHeader from "@/components/canvas/ItemHeader";
import { X } from "lucide-react";

export default function StreamingCanvas() {
  const { state, setState } = useCoAgent<AgentState>({
    name: "sample_agent",
    initialState,
  });
  
  // Streaming integration
  const { isConnected, events, responses, sendUserRequest } = useStreaming();
  
  // Global cache for the last non-empty agent state
  const cachedStateRef = useRef<AgentState>(state ?? initialState);
  useEffect(() => {
    if (isNonEmptyAgentState(state)) {
      cachedStateRef.current = state as AgentState;
    }
  }, [state]);
  
  const viewState: AgentState = isNonEmptyAgentState(state) ? (state as AgentState) : cachedStateRef.current;
  const isDesktop = useMediaQuery("(min-width: 768px)");

  // Handle streaming events
  useEffect(() => {
    events.forEach(event => {
      switch (event.event_type) {
        case 'item_added':
          handleItemAdded(event);
          break;
        case 'item_removed':
          handleItemRemoved(event);
          break;
        case 'item_updated':
          handleItemUpdated(event);
          break;
        case 'field_changed':
          handleFieldChanged(event);
          break;
      }
    });
  }, [events]);

  // Handle streaming responses
  useEffect(() => {
    responses.forEach(response => {
      console.log(`🔄 Streaming: ${response.type} - ${response.message}`);
    });
  }, [responses]);

  const handleItemAdded = (event: any) => {
    const newItem = {
      id: event.item_id,
      type: event.data.type || 'inventory',
      name: event.data.name || 'New Item',
      subtitle: event.data.subtitle || '',
      data: event.data
    };
    
    setState(prev => ({
      ...prev,
      items: [...(prev.items || []), newItem]
    }));
  };

  const handleItemRemoved = (event: any) => {
    setState(prev => ({
      ...prev,
      items: (prev.items || []).filter(item => item.id !== event.item_id)
    }));
  };

  const handleItemUpdated = (event: any) => {
    setState(prev => ({
      ...prev,
      items: (prev.items || []).map(item => 
        item.id === event.item_id 
          ? { ...item, ...event.data }
          : item
      )
    }));
  };

  const handleFieldChanged = (event: any) => {
    setState(prev => ({
      ...prev,
      items: (prev.items || []).map(item => 
        item.id === event.item_id 
          ? { 
              ...item, 
              data: { 
                ...item.data, 
                ...event.data 
              } 
            }
          : item
      )
    }));
  };

  // Enhanced CopilotKit actions with streaming
  useCopilotAction({
    name: "streamingCreateItem",
    description: "Create a new item with streaming updates.",
    available: "remote",
    parameters: [
      { name: "type", type: "string", required: true, description: "Item type." },
      { name: "name", type: "string", required: false, description: "Item name." },
    ],
    handler: ({ type, name }: { type: string; name?: string }) => {
      // Send streaming request
      sendUserRequest(`Create a new ${type} item${name ? ` named ${name}` : ''}`, {
        item_type: type,
        item_name: name
      });
      
      return `Streaming creation of ${type} item...`;
    },
  });

  useCopilotAction({
    name: "streamingRemoveItem",
    description: "Remove an item with streaming updates.",
    available: "remote",
    parameters: [
      { name: "itemId", type: "string", required: true, description: "Item ID to remove." },
    ],
    handler: ({ itemId }: { itemId: string }) => {
      // Send streaming request
      sendUserRequest(`Remove item ${itemId}`, {
        item_id: itemId,
        action: 'remove'
      });
      
      return `Streaming removal of item ${itemId}...`;
    },
  });

  useCopilotAction({
    name: "streamingBulkOperation",
    description: "Perform bulk operations with streaming updates.",
    available: "remote",
    parameters: [
      { name: "operation", type: "string", required: true, description: "Operation type (add_multiple, remove_multiple, update_multiple)." },
      { name: "items", type: "string", required: true, description: "JSON string of items to process." },
    ],
    handler: ({ operation, items }: { operation: string; items: string }) => {
      try {
        const itemsData = JSON.parse(items);
        
        // Send streaming request
        sendUserRequest(`Perform ${operation} on ${itemsData.length} items`, {
          operation,
          items: itemsData
        });
        
        return `Streaming ${operation} of ${itemsData.length} items...`;
      } catch (error) {
        return `Error parsing items: ${error}`;
      }
    },
  });

  // Regular item management functions
  const updateItem = useCallback(
    (itemId: string, updates: Partial<Item>) => {
      setState((prev) => {
        const base = prev ?? initialState;
        const items: Item[] = base.items ?? [];
        const nextItems = items.map((p) => (p.id === itemId ? { ...p, ...updates } : p));
        return { ...base, items: nextItems } as AgentState;
      });
    },
    [setState]
  );

  const updateItemData = useCallback(
    (itemId: string, updater: (prev: any) => any) => {
      setState((prev) => {
        const base = prev ?? initialState;
        const items: Item[] = base.items ?? [];
        const nextItems = items.map((p) => (p.id === itemId ? { ...p, data: updater(p.data) } : p));
        return { ...base, items: nextItems } as AgentState;
      });
    },
    [setState]
  );

  const deleteItem = useCallback((itemId: string) => {
    setState((prev) => {
      const base = prev ?? initialState;
      const existed = (base.items ?? []).some((p) => p.id === itemId);
      const items: Item[] = (base.items ?? []).filter((p) => p.id !== itemId);
      return { ...base, items, lastAction: existed ? `deleted:${itemId}` : `not_found:${itemId}` } as AgentState;
    });
  }, [setState]);

  const defaultDataFor = useCallback((type: CardType): any => {
    switch (type) {
      case "project":
        return {
          field1: "",
          field2: "",
          field3: "",
          field4: [],
          field4_id: 0,
        };
      case "entity":
        return {
          field1: "",
          field2: "",
          field3: [],
          field3_options: ["Tag 1", "Tag 2", "Tag 3"],
        };
      case "note":
        return { field1: "" };
      case "chart":
        return { field1: [], field1_id: 0 };
      default:
        return { content: "" };
    }
  }, []);

  const addItem = useCallback((type: CardType, name?: string) => {
    const t: CardType = type;
    let createdId = "";
    setState((prev) => {
      const base = prev ?? initialState;
      const items: Item[] = base.items ?? [];
      const maxExisting = items.reduce((max, it) => {
        const parsed = Number.parseInt(String(it.id ?? "0"), 10);
        return Number.isFinite(parsed) ? Math.max(max, parsed) : max;
      }, 0);
      const priorCount = Number.isFinite(base.itemsCreated) ? (base.itemsCreated as number) : 0;
      const nextNumber = Math.max(priorCount, maxExisting) + 1;
      createdId = String(nextNumber).padStart(4, "0");
      const item: Item = {
        id: createdId,
        type: t,
        name: name && name.trim() ? name.trim() : "",
        subtitle: "",
        data: defaultDataFor(t),
      };
      const nextItems = [...items, item];
      return { ...base, items: nextItems, itemsCreated: nextNumber, lastAction: `created:${createdId}` } as AgentState;
    });
    return createdId;
  }, [defaultDataFor, setState]);

  const toggleTag = useCallback((itemId: string, tag: string) => {
    updateItemData(itemId, (prev) => {
      const anyPrev = prev as { field3?: string[] };
      if (Array.isArray(anyPrev.field3)) {
        const selected = new Set<string>(anyPrev.field3 ?? []);
        if (selected.has(tag)) selected.delete(tag); else selected.add(tag);
        return { ...anyPrev, field3: Array.from(selected) } as any;
      }
      return prev;
    });
  }, [updateItemData]);

  return (
    <div
      style={{ "--copilot-kit-primary-color": "#2563eb" } as CopilotKitCSSProperties}
      className="h-screen flex flex-col"
    >
      {/* Connection Status */}
      <div className="bg-gray-100 px-4 py-2 text-sm">
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
          <span>Streaming: {isConnected ? 'Connected' : 'Disconnected'}</span>
          {events.length > 0 && <span>({events.length} events)</span>}
          {responses.length > 0 && <span>({responses.length} responses)</span>}
        </div>
      </div>

      {/* Main Layout */}
      <div className="flex flex-1 overflow-hidden">
        {/* Chat Sidebar */}
        <aside className="-order-1 max-md:hidden flex flex-col min-w-80 w-[30vw] max-w-120 p-4 pr-0">
          <div className="h-full flex flex-col align-start w-full shadow-lg rounded-2xl border border-sidebar-border overflow-hidden">
            <div className="p-4 border-b">
              <h3 className="font-semibold">AI Agent</h3>
              <p className="text-sm text-gray-600">Streaming enabled</p>
            </div>
            {isDesktop && (
              <CopilotChat
                className="flex-1 overflow-auto w-full"
                labels={{
                  title: "Agent",
                  initial: "👋 I can add and remove items in real-time. Try: 'Add 5 inventory items' or 'Remove low stock items'",
                }}
                suggestions={[
                  {
                    title: "Add Multiple Items",
                    message: "Add 5 new inventory items for Q1 planning",
                  },
                  {
                    title: "Remove Items",
                    message: "Remove all low stock items",
                  },
                  {
                    title: "Bulk Operations",
                    message: "Create multiple suppliers and inventory items",
                  },
                ]}
              />
            )}
          </div>
        </aside>

        {/* Main Content */}
        <main className="relative flex flex-1 h-full">
          <div className="relative overflow-auto size-full px-4 sm:px-8 md:px-10 py-4">
            <div className="relative mx-auto max-w-7xl h-full min-h-8">
              {/* Global Title & Description */}
              <div className="sticky top-0 mb-6">
                <input
                  value={viewState?.globalTitle ?? initialState.globalTitle}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                    setState((prev) => ({ ...(prev ?? initialState), globalTitle: e.target.value }))
                  }
                  placeholder="Canvas title..."
                  className="w-full outline-none rounded-md px-2 py-1 text-2xl font-semibold bg-transparent placeholder:text-gray-400 ring-1 ring-transparent transition-all ease-out hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10"
                />
                <input
                  value={viewState?.globalDescription ?? initialState.globalDescription}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                    setState((prev) => ({ ...(prev ?? initialState), globalDescription: e.target.value }))
                  }
                  placeholder="Canvas description..."
                  className="w-full outline-none rounded-md px-2 py-1 mt-2 text-sm leading-6 resize-none overflow-hidden bg-transparent placeholder:text-gray-400 ring-1 ring-transparent transition-all ease-out hover:ring-border focus:ring-2 focus:ring-accent/50 focus:shadow-sm focus:bg-accent/10"
                />
              </div>
              
              {(viewState.items ?? []).length === 0 ? (
                <EmptyState className="flex-1">
                  <div className="mx-auto max-w-lg text-center">
                    <h2 className="text-lg font-semibold text-foreground">Nothing here yet</h2>
                    <p className="mt-2 text-sm text-muted-foreground">Create your first item to get started.</p>
                    
                    {/* Load Sample Data Button */}
                    <div className="mt-6 mb-6">
                      <SimpleLoadDataButton onLoadData={(data) => setState(data)} />
                    </div>
                    
                    <div className="mt-6 flex justify-center">
                      <NewItemMenu onSelect={(t: CardType) => addItem(t)} align="center" className="md:h-10" />
                    </div>
                  </div>
                </EmptyState>
              ) : (
                <div className="flex-1 py-0 overflow-hidden">
                  <div className="grid gap-6 lg:grid-cols-2 pb-20">
                    {(viewState.items ?? []).map((item) => (
                      <article key={item.id} className="relative rounded-2xl border p-5 shadow-sm transition-colors ease-out bg-card hover:border-accent/40 focus-within:border-accent/60">
                        <button
                          type="button"
                          aria-label="Delete card"
                          className="absolute right-2 top-2 inline-flex h-7 w-7 items-center justify-center rounded-full bg-card text-gray-400 hover:bg-accent/10 hover:text-accent transition-colors"
                          onClick={() => deleteItem(item.id)}
                        >
                          <X className="h-4 w-4" />
                        </button>
                        <ItemHeader
                          id={item.id}
                          name={item.name}
                          subtitle={item.subtitle}
                          description=""
                          onNameChange={(v) => updateItem(item.id, { name: v })}
                          onSubtitleChange={(v) => updateItem(item.id, { subtitle: v })}
                        />

                        <div className="mt-6">
                          <CardRenderer item={item} onUpdateData={(updater) => updateItemData(item.id, updater)} onToggleTag={(tag) => toggleTag(item.id, tag)} />
                        </div>
                      </article>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
          
          {(viewState.items ?? []).length > 0 ? (
            <div className="absolute left-1/2 -translate-x-1/2 bottom-4 inline-flex rounded-lg shadow-lg bg-card">
              <NewItemMenu
                onSelect={(t: CardType) => addItem(t)}
                align="center"
                className="rounded-r-none border-r-0 peer"
              />
            </div>
          ) : null}
        </main>
      </div>
      
      {/* Mobile Chat Popup */}
      <div className="md:hidden">
        {!isDesktop && (
          <CopilotPopup
            labels={{
              title: "Agent",
              initial: "👋 I can add and remove items in real-time. Try: 'Add 5 inventory items' or 'Remove low stock items'",
            }}
            suggestions={[
              {
                title: "Add Multiple Items",
                message: "Add 5 new inventory items for Q1 planning",
              },
              {
                title: "Remove Items",
                message: "Remove all low stock items",
              },
              {
                title: "Bulk Operations",
                message: "Create multiple suppliers and inventory items",
              },
            ]}
          />
        )}
      </div>
    </div>
  );
}
