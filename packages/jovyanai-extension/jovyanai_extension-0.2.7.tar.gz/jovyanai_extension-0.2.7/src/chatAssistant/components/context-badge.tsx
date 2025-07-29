'use client';

import React from 'react';
// import { X } from 'lucide-react'; // Removed unused import
import { notebookIcon, codeIcon } from '@jupyterlab/ui-components'; // Import icons
import '../../../style/context-badge.css';

// Remove ContextType definition
// export type ContextType = 'notebook' | 'cell';

// Revert props interface to original
interface IContextBadgeProps {
  contextName: string;
  contextType: string;
  onRemove: () => void;
}

export const ContextBadge: React.FC<IContextBadgeProps> = ({
  contextName,
  contextType,
  onRemove
}) => {
  // Revert display logic to original
  // const displayName = contextType === 'notebook' ? 'Notebook' : 'Cell';
  // const badgeClass = `context-badge ${contextType}`;

  // Determine the icon based on contextType
  const Icon =
    contextType === 'notebook' || contextType === 'current-notebook-context'
      ? notebookIcon
      : codeIcon;

  return (
    <div className={`context-badge ${contextType}`}>
      <span className="context-badge-prefix">
        {/* Render the icon */}
        <Icon.react tag="span" className="context-badge-icon" />
      </span>
      <span className="context-badge-name">{contextName}</span>
      {contextType !== 'current-notebook-context' && (
        <button
          className="context-badge-remove"
          onClick={e => {
            e.stopPropagation();
            onRemove();
          }}
        >
          ×
        </button>
      )}
    </div>
  );
};
