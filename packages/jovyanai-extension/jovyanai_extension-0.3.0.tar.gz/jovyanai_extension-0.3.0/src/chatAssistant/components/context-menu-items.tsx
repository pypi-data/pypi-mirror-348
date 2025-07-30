'use client';

import React from 'react';
import { codeIcon, LabIcon } from '@jupyterlab/ui-components';
import { BookOpenText, FolderGit2 } from 'lucide-react';

interface IContextMenuItemsProps {
  isCellContextActive: boolean;
  onAddCellContext: () => void;
  onDocsClick: () => void;
  onGitRepoClick: () => void;
}

export const ContextMenuItems: React.FC<IContextMenuItemsProps> = ({
  isCellContextActive,
  onAddCellContext,
  onDocsClick,
  onGitRepoClick
}) => {
  return (
    <>
      {/* This Cell Option */}
      <div
        className={`context-menu-item ${isCellContextActive ? 'disabled' : ''}`}
        onClick={isCellContextActive ? undefined : onAddCellContext}
      >
        <div className="context-menu-item-content">
          {React.createElement((codeIcon as LabIcon).react, {
            tag: 'span',
            className: 'context-menu-icon'
          })}
          <span>This Cell</span>
        </div>
        {isCellContextActive && (
          <span className="context-menu-checkmark">✓</span>
        )}
      </div>
      <div
        style={{
          height: '1px',
          backgroundColor: 'var(--jp-border-color1)',
          margin: '4px 0'
        }}
      />
      {/* Docs Option */}
      <div className="context-menu-item" onClick={onDocsClick}>
        <div className="context-menu-item-content">
          <BookOpenText size={16} className="context-menu-icon" />
          <span>Docs</span>
        </div>
      </div>
      <div className="context-menu-item" onClick={onGitRepoClick}>
        <div className="context-menu-item-content">
          <FolderGit2 size={16} className="context-menu-icon" />
          <span>Git Repo</span>
        </div>
      </div>
    </>
  );
};
