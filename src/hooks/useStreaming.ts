import { useEffect, useRef, useState } from 'react';

interface StreamingEvent {
  event_type: string;
  item_id: string;
  data: any;
  timestamp: string;
  agent_id: string;
  user_id?: string;
}

interface StreamingResponse {
  type: string;
  message: string;
  data?: any;
  timestamp: string;
}

export const useStreaming = (url: string = 'ws://localhost:8765') => {
  const [isConnected, setIsConnected] = useState(false);
  const [events, setEvents] = useState<StreamingEvent[]>([]);
  const [responses, setResponses] = useState<StreamingResponse[]>([]);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const connect = () => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return;

    try {
      wsRef.current = new WebSocket(url);
      
      wsRef.current.onopen = () => {
        console.log('🔄 Connected to streaming server');
        setIsConnected(true);
        if (reconnectTimeoutRef.current) {
          clearTimeout(reconnectTimeoutRef.current);
          reconnectTimeoutRef.current = null;
        }
      };

      wsRef.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          
          if (data.event_type) {
            // Handle streaming events (item_added, item_removed, etc.)
            setEvents(prev => [...prev, data as StreamingEvent]);
          } else if (data.type) {
            // Handle streaming responses
            setResponses(prev => [...prev, data as StreamingResponse]);
          }
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      wsRef.current.onclose = () => {
        console.log('🔄 Disconnected from streaming server');
        setIsConnected(false);
        
        // Auto-reconnect after 3 seconds
        reconnectTimeoutRef.current = setTimeout(() => {
          console.log('🔄 Attempting to reconnect...');
          connect();
        }, 3000);
      };

      wsRef.current.onerror = (error) => {
        console.error('WebSocket error:', error);
        setIsConnected(false);
      };

    } catch (error) {
      console.error('Failed to connect to WebSocket:', error);
      setIsConnected(false);
    }
  };

  const disconnect = () => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }
    
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
    setIsConnected(false);
  };

  const sendMessage = (message: any) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message));
    } else {
      console.warn('WebSocket not connected');
    }
  };

  const sendUserRequest = (userInput: string, context: any = {}, userId?: string) => {
    sendMessage({
      type: 'user_request',
      user_input: userInput,
      context,
      user_id: userId
    });
  };

  useEffect(() => {
    connect();
    
    return () => {
      disconnect();
    };
  }, [url]);

  return {
    isConnected,
    events,
    responses,
    connect,
    disconnect,
    sendMessage,
    sendUserRequest
  };
};
