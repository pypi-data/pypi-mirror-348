import React from 'react';
// import { Code } from 'lucide-react'; // Removed unused import
import '../../../style/tool-indicator.css';
import type { IToolUse } from '../types';

interface IToolIndicatorProps {
  tool: IToolUse;
}

export const ToolIndicator: React.FC<IToolIndicatorProps> = ({ tool }) => {
  return (
    <div className="tool-indicator">
      <div className="tool-icon">
        {tool.type === 'thought' && '💭'}
        {tool.type === 'read' && '📖'}
        {tool.type === 'other' && '🔧'}
      </div>
      <div className="tool-text">
        {tool.content} {tool.seconds !== undefined && `${tool.seconds} seconds`}
        {tool.reference && (
          <span className="tool-reference">{tool.reference}</span>
        )}
      </div>
    </div>
  );
};
