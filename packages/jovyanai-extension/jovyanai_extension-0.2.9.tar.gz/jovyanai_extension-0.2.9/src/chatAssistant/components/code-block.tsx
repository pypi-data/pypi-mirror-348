'use client';

import React, { useRef, useEffect, useState } from 'react';
import { Clipboard, Check, Play, Plus } from 'lucide-react';
import { EditorView } from '@codemirror/view';
import { EditorState, Extension } from '@codemirror/state';
import { python } from '@codemirror/lang-python';
import { jupyterTheme } from '@jupyterlab/codemirror';
import '../../../style/code-block.css';
import { useNotebookController } from '../../context/NotebookControllerContext';

interface ICodeBlockProps {
  code: string;
  language: string;
}

export const CodeBlock: React.FC<ICodeBlockProps> = ({ code, language }) => {
  const [isCopied, setIsCopied] = useState(false);
  const editorRef = useRef<HTMLDivElement>(null);
  const viewRef = useRef<EditorView>();
  const notebookController = useNotebookController();

  useEffect(() => {
    if (editorRef.current) {
      if (viewRef.current) {
        viewRef.current.destroy();
      }

      const extensions: Extension[] = [
        jupyterTheme,
        EditorView.editable.of(false),
        EditorState.readOnly.of(true),
        EditorView.lineWrapping
      ];

      if (language === 'python') {
        extensions.push(python());
      }

      const state = EditorState.create({
        doc: code,
        extensions
      });

      const view = new EditorView({
        state: state,
        parent: editorRef.current
      });

      viewRef.current = view;

      return () => {
        view.destroy();
        viewRef.current = undefined;
      };
    }
  }, [code, language]);

  const handleCopy = () => {
    navigator.clipboard.writeText(code).then(() => {
      setIsCopied(true);
      setTimeout(() => setIsCopied(false), 2000);
    });
  };

  const handleApplyCode = () => {
    const cell = notebookController.currentCell;
    if (cell) {
      notebookController.writeCodeInCell(cell, code);
      // Optionally run the cell after applying
      // notebookController.runCell(cell);
    }
  };

  const handleInsertCodeBelow = () => {
    const currentCellIndex = notebookController.currentCellIndex;
    notebookController.insertCell(currentCellIndex + 1, code);
  };

  return (
    <div className="code-block">
      <div className="code-header">
        <span className="language-tag">{language}</span>
        <div className="code-header-buttons">
          <button
            onClick={handleCopy}
            className="code-action-button"
            title="Copy code"
          >
            {isCopied ? <Check size={14} /> : <Clipboard size={14} />}
          </button>
          <button
            onClick={handleApplyCode}
            className="code-action-button"
            title="Apply to active cell"
          >
            <Play size={14} />
          </button>
          <button
            onClick={handleInsertCodeBelow}
            className="code-action-button"
            title="Insert cell below"
          >
            <Plus size={14} />
          </button>
        </div>
      </div>
      <div className="code-content" ref={editorRef} />
    </div>
  );
};
