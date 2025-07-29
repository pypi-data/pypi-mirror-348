'use client';

import React, { useState, useRef, useEffect } from 'react';
import { ContextBadge } from './context-badge';
import { useChatContext } from '../ChatContextProvider';
import { Context } from '../types/context';

interface IContextMenuProps {
  disabled?: boolean;
}

export const ContextMenu: React.FC<IContextMenuProps> = ({
  disabled = false
}) => {
  const [showContextMenu, setShowContextMenu] = useState(false);
  const contextMenuRef = useRef<HTMLDivElement>(null);
  const contextButtonRef = useRef<HTMLButtonElement>(null);
  const chatContextController = useChatContext();

  // Toggle context menu
  const toggleContextMenu = (e: React.MouseEvent) => {
    e.stopPropagation();
    setShowContextMenu(!showContextMenu);
  };

  // Close context menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        contextMenuRef.current &&
        !contextMenuRef.current.contains(event.target as Node) &&
        contextButtonRef.current &&
        !contextButtonRef.current.contains(event.target as Node)
      ) {
        setShowContextMenu(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  // const handleAddNotebookContext = () => {
  //   chatContextController.addCurrentNotebookContext();
  //   setShowContextMenu(false);
  // };

  const handleAddCellContext = () => {
    try {
      chatContextController.addCurrentCellContext();
    } catch (error) {
      console.error('Error creating cell context:', error);
    }
    setShowContextMenu(false);
  };

  // Determine active states
  const isNotebookContextActive =
    chatContextController.currentNotebookInContext;
  const isCellContextActive = chatContextController.hasCurrentCellInContext();

  const onRemoveContext = (context: Context) => {
    chatContextController.removeContext(context);
  };

  return (
    <div className="context-badges">
      {' '}
      {/* Use the same wrapper class */}
      <button
        type="button"
        className="add-context-button"
        onClick={toggleContextMenu}
        ref={contextButtonRef}
        disabled={disabled}
      >
        @
      </button>
      {showContextMenu && (
        <div className="context-menu" ref={contextMenuRef}>
          {/* This Cell Option */}
          <div
            className={`context-menu-item ${isCellContextActive ? 'disabled' : ''}`}
            onClick={isCellContextActive ? undefined : handleAddCellContext}
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }} // Basic styling
          >
            <span>This Cell</span>
            {isCellContextActive && (
              <span style={{ marginLeft: '10px' }}>✓</span>
            )}
          </div>
        </div>
      )}
      {/* Render Context Badges */}
      {isNotebookContextActive && (
        <ContextBadge
          key={'current-notebook-context'}
          contextName={chatContextController.currentNotebookFileName}
          contextType={'current-notebook-context'}
          onRemove={() => {}}
        />
      )}
      {chatContextController.activeContexts.map(context => {
        // Use a more robust key, displayName might not be unique enough long term
        const key = `${context.type}-${chatContextController.getContextName(context)}`;
        return (
          <ContextBadge
            key={key}
            contextName={chatContextController.getContextName(context)}
            contextType={context.type}
            onRemove={() => onRemoveContext(context)}
          />
        );
      })}
    </div>
  );
};
