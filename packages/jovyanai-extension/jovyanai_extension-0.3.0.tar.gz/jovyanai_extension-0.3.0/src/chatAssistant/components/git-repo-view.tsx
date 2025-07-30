'use client';

import React from 'react';
import { Context } from '../types/context';
import '../../../style/shared-menu.css';

interface IGitRepoViewProps {
  onBack: () => void;
  onAddNewRepo: () => void;
  indexedRepoNames: string[];
  onSelectRepo: (repoName: string) => void;
  activeContexts: Context[];
}

export const GitRepoView: React.FC<IGitRepoViewProps> = ({
  onBack,
  onAddNewRepo,
  indexedRepoNames,
  onSelectRepo,
  activeContexts
}) => {
  const isSelected = (repoName: string) => {
    return activeContexts.some(
      context => context.type === 'git-repo' && context.id === repoName
    );
  };

  return (
    <div className="menu-view">
      <div className="menu-header">
        <button onClick={onBack} className="menu-back-button" title="Back">
          &larr;
        </button>
      </div>
      <div className="menu-title">Git Repositories</div>

      {/* List of indexed repositories */}
      {indexedRepoNames.length > 0 && (
        <ul className="menu-list">
          {indexedRepoNames.map(repoName => (
            <li
              key={repoName}
              onClick={() => onSelectRepo(repoName)}
              className={`menu-item ${isSelected(repoName) ? 'selected' : ''}`}
            >
              <div className="menu-item-content">
                <span>{repoName}</span>
              </div>
              {isSelected(repoName) && (
                <span className="menu-checkmark">✓</span>
              )}
            </li>
          ))}
        </ul>
      )}

      <button onClick={onAddNewRepo} className="menu-add-button">
        + Add new repository
      </button>
    </div>
  );
};
