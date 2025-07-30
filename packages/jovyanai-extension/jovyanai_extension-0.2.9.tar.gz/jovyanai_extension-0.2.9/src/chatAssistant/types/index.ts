// Update the Message interface to include toolUse
import { Context } from './context';

export interface IMessage {
  role: 'user' | 'assistant';
  content: string;
  isStreaming?: boolean;
  contexts?: Array<Context>;
}

// Add a ToolUse interface
export interface IToolUse {
  id: string;
  type: 'thought' | 'read' | 'other';
  content: string;
  seconds?: number;
  reference?: string;
}
