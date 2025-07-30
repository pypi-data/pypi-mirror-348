'use client';

import React from 'react';
import { Context } from '../types/context'; // Import Context to check active contexts
import '../../../style/shared-menu.css';

interface IDocsViewProps {
  onBack: () => void;
  onAddNewDoc: () => void;
  indexedDocumentNames: string[];
  onSelectDocument: (docName: string) => void;
  activeContexts: Context[];
}

export const DocsView: React.FC<IDocsViewProps> = ({
  onBack,
  onAddNewDoc,
  indexedDocumentNames,
  onSelectDocument,
  activeContexts
}) => {
  const isSelected = (docName: string) => {
    return activeContexts.some(
      context => context.type === 'document' && context.id === docName
    );
  };

  return (
    <div className="menu-view">
      <div className="menu-header">
        <button onClick={onBack} className="menu-back-button" title="Back">
          &larr;
        </button>
      </div>
      <div className="menu-title">Docs</div>

      {/* List of indexed documents */}
      {indexedDocumentNames.length > 0 && (
        <ul className="menu-list">
          {indexedDocumentNames.map(docName => (
            <li
              key={docName}
              onClick={() => onSelectDocument(docName)}
              className={`menu-item ${isSelected(docName) ? 'selected' : ''}`}
            >
              <div className="menu-item-content">
                <span>{docName}</span>
              </div>
              {isSelected(docName) && <span className="menu-checkmark">✓</span>}
            </li>
          ))}
        </ul>
      )}

      <button onClick={onAddNewDoc} className="menu-add-button">
        + Add new doc
      </button>
    </div>
  );
};
