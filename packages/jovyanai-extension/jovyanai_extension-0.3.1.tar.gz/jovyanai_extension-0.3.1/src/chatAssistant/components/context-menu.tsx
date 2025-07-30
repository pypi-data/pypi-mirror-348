'use client';

import React, { useState, useRef, useEffect } from 'react';
import { ContextBadge } from './context-badge';
import { useChatContext } from '../ChatContextProvider';
import { Context, DocumentContext, GitRepoContext } from '../types/context';
import { AddDocPopup } from './add-docs-popup';
import { DocsView } from './docs-view';
import { ContextMenuItems } from './context-menu-items';
import { AddGitRepoPopup } from './add-git-repo-popup';
import { GitRepoView } from './git-repo-view';

interface IContextMenuProps {
  disabled?: boolean;
}

export const ContextMenu: React.FC<IContextMenuProps> = ({
  disabled = false
}) => {
  const [showContextMenu, setShowContextMenu] = useState(false);
  const [isDocsViewVisible, setIsDocsViewVisible] = useState(false);
  const [isGitRepoViewVisible, setIsGitRepoViewVisible] = useState(false);
  const [showAddDocPopup, setShowAddDocPopup] = useState(false);
  const [showAddGitRepoPopup, setShowAddGitRepoPopup] = useState(false);
  const [indexedDocumentNames, setIndexedDocumentNames] = useState<string[]>(
    []
  );
  const [indexedRepoNames, setIndexedRepoNames] = useState<string[]>([]);
  const contextMenuRef = useRef<HTMLDivElement>(null);
  const contextButtonRef = useRef<HTMLButtonElement>(null);
  const chatContextController = useChatContext();

  // Toggle context menu
  const toggleContextMenu = (e: React.MouseEvent) => {
    e.stopPropagation();
    setShowContextMenu(!showContextMenu);
    // Reset to initial view when opening
    if (!showContextMenu) {
      setIsDocsViewVisible(false);
      setIsGitRepoViewVisible(false);
    }
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
        setShowAddDocPopup(false);
        setShowAddGitRepoPopup(false);
        setIsDocsViewVisible(false);
        setIsGitRepoViewVisible(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleAddCellContext = () => {
    try {
      chatContextController.addCurrentCellContext();
    } catch (error) {
      console.error('Error creating cell context:', error);
    }
    setShowContextMenu(false);
  };

  const handleDocsClick = async () => {
    setIsDocsViewVisible(true);
    try {
      const names = await chatContextController.getIndexedDocumentNames();
      setIndexedDocumentNames(names);
    } catch (error) {
      console.error(
        'ContextMenu: Error fetching indexed document names:',
        error
      );
      setIndexedDocumentNames([]);
    }
  };

  const handleGitRepoClick = async () => {
    setIsGitRepoViewVisible(true);
    try {
      const names = await chatContextController.getIndexedRepoNames();
      setIndexedRepoNames(names);
    } catch (error) {
      console.error(
        'ContextMenu: Error fetching indexed repository names:',
        error
      );
      setIndexedRepoNames([]);
    }
  };

  const handleAddNewDoc = () => {
    setShowAddDocPopup(true);
    setShowContextMenu(false);
  };

  const handleAddNewRepo = () => {
    setShowAddGitRepoPopup(true);
    setShowContextMenu(false);
  };

  const handleDocSubmit = async (
    name: string,
    file: File | null,
    link: string | null
  ) => {
    console.debug('ContextMenu: handleDocSubmit called with:', { file, link });
    try {
      const newDocContext = await chatContextController.sendDocumentContext(
        name,
        file,
        link
      );
      if (newDocContext) {
        chatContextController.addContext(newDocContext);
        console.debug('ContextMenu: DocumentContext added to active contexts.');
      }
    } catch (error) {
      console.error('ContextMenu: Error submitting document context:', error);
    }
    setShowAddDocPopup(false);
  };

  const handleGitRepoSubmit = async (name: string, url: string) => {
    console.debug('ContextMenu: handleGitRepoSubmit called with:', {
      name,
      url
    });
    try {
      const newRepoContext = await chatContextController.sendGitRepoContext(
        name,
        url
      );
      if (newRepoContext) {
        chatContextController.addContext(newRepoContext);
        console.debug('ContextMenu: GitRepoContext added to active contexts.');
      }
    } catch (error) {
      console.error('ContextMenu: Error submitting Git repo context:', error);
    }
    setShowAddGitRepoPopup(false);
  };

  const handleSelectIndexedDocument = (docName: string) => {
    const newDocContext = new DocumentContext(docName, docName, null, null);
    chatContextController.addContext(newDocContext);
  };

  const handleSelectIndexedRepo = (repoName: string) => {
    // We need to get the URL for the repo from the backend
    const newRepoContext = new GitRepoContext(repoName, repoName, null);
    chatContextController.addContext(newRepoContext);
  };

  // Determine active states
  const isNotebookContextActive =
    chatContextController.currentNotebookInContext;
  const isCellContextActive = chatContextController.hasCurrentCellInContext();

  const onRemoveContext = (context: Context) => {
    chatContextController.removeContext(context);
  };

  return (
    <div className="context-badges" style={{ position: 'relative' }}>
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
        <div
          className="context-menu"
          ref={contextMenuRef}
          style={{
            position: 'absolute',
            top: '-4px',
            transform: 'translateY(-100%)',
            left: 0,
            border: '1px solid var(--jp-border-color1)',
            padding: '4px',
            backgroundColor: 'var(--jp-layout-color0)',
            minHeight: '100px',
            maxHeight: '200px',
            overflowY: 'auto',
            zIndex: 1000
          }}
        >
          {!isDocsViewVisible && !isGitRepoViewVisible ? (
            <ContextMenuItems
              isCellContextActive={isCellContextActive}
              onAddCellContext={handleAddCellContext}
              onDocsClick={handleDocsClick}
              onGitRepoClick={handleGitRepoClick}
            />
          ) : isDocsViewVisible ? (
            <DocsView
              onBack={() => setIsDocsViewVisible(false)}
              onAddNewDoc={handleAddNewDoc}
              indexedDocumentNames={indexedDocumentNames}
              onSelectDocument={handleSelectIndexedDocument}
              activeContexts={chatContextController.activeContexts}
            />
          ) : (
            <GitRepoView
              onBack={() => setIsGitRepoViewVisible(false)}
              onAddNewRepo={handleAddNewRepo}
              indexedRepoNames={indexedRepoNames}
              onSelectRepo={handleSelectIndexedRepo}
              activeContexts={chatContextController.activeContexts}
            />
          )}
        </div>
      )}
      {/* Render Context Badges */}
      {isNotebookContextActive && (
        <ContextBadge
          key={'current-notebook-context'}
          contextName={chatContextController.currentNotebookFileName}
          contextType={'current-notebook-context'}
          onRemove={() => {
            console.log('Removing current notebook context');
          }}
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
      {showAddDocPopup && (
        <AddDocPopup
          onClose={() => setShowAddDocPopup(false)}
          onSubmit={handleDocSubmit}
        />
      )}
      {showAddGitRepoPopup && (
        <AddGitRepoPopup
          onClose={() => setShowAddGitRepoPopup(false)}
          onSubmit={handleGitRepoSubmit}
        />
      )}
    </div>
  );
};
