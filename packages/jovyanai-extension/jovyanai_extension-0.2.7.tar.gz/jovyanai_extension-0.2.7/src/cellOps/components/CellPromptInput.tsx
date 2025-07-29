// AI prompt input component with a text input and a button to send the prompt to AI

import React, { useState, useRef, useEffect } from 'react';
import { Editor, Monaco } from '@monaco-editor/react';
import * as monaco from 'monaco-editor';

interface IInputComponentProps {
  isEnabled: boolean;
  placeholderEnabled: string;
  placeholderDisabled: string;
  initialInput?: string;
  onSubmit: (input: string) => void;
  onCancel: () => void;
}

interface IButtonProps {
  onClick: () => void;
  disabled?: boolean;
  className?: string;
  children: React.ReactNode;
}

const Button: React.FC<IButtonProps> = ({
  onClick,
  disabled = false,
  className,
  children
}) => {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={className || 'jv-default-button'}
      style={{
        cursor: disabled ? 'not-allowed' : 'pointer',
        opacity: disabled ? 0.6 : 1
      }}
    >
      {children}
    </button>
  );
};

const InputComponent: React.FC<IInputComponentProps> = ({
  isEnabled,
  placeholderEnabled,
  placeholderDisabled,
  initialInput,
  onSubmit,
  onCancel
}) => {
  const [editorValue, setEditorValue] = useState(initialInput || '');
  const editorRef = useRef<monaco.editor.IStandaloneCodeEditor | null>(null);

  const handleEditorChange = (value: string | undefined) => {
    if (value !== undefined) {
      setEditorValue(value);
    }
  };

  const handleEditorMount = (
    editor: monaco.editor.IStandaloneCodeEditor,
    monaco: Monaco
  ) => {
    editorRef.current = editor;
    // Add event listeners
    editor.onKeyDown(async (event: any) => {
      // Check if autocomplete widget is visible
      const isAutocompleteWidgetVisible = () => {
        const editorElement = editor.getContainerDomNode();
        const suggestWidget = editorElement.querySelector(
          '.editor-widget.suggest-widget.visible'
        );
        return (
          suggestWidget !== null &&
          suggestWidget.getAttribute('monaco-visible-content-widget') === 'true'
        );
      };

      if (isAutocompleteWidgetVisible()) {
        // Let Monaco handle the key events when autocomplete is open
        return;
      }

      if (event.code === 'Escape') {
        event.preventDefault();
        // Explicitly blur the editor's DOM element
        const editorDomElement = editorRef.current?.getDomNode();
        if (editorDomElement && typeof editorDomElement.blur === 'function') {
          console.debug('blurring editor');
            editorDomElement.blur();
        }
        // Defer the onCancel call to the next tick of the event loop
        setTimeout(() => {
            onCancel();
        }, 0);
      }

      if (event.code === 'Enter') {
        event.preventDefault();
        if (event.shiftKey) {
          editor.trigger('keyboard', 'type', { text: '\n' });
        } else {
          handleSubmit();
        }
      }
    });

    // Try focusing with a slight delay
    setTimeout(() => {
      if (editorRef.current) { // Ensure component hasn't unmounted
        editorRef.current.focus();
      }
    }, 100); // 50ms delay, can be adjusted (0 might also work)
  };

  // Add this useEffect for cleanup
  useEffect(() => {
    return () => {
      // Access the .current property of the ref directly *inside* the cleanup function.
      if (editorRef.current) {
        console.debug('Disposing editor instance');
        editorRef.current.dispose();
        editorRef.current = null; 
      } else {
        console.debug('Cleanup called, but editorRef.current was already null.');
      }
    };
  }, []); // Empty dependency array ensures this runs on mount and cleans up on unmount.

  const handleSubmit = () => {
    // Get the most current value directly from the editor
    const currentValue = editorRef.current?.getValue() || editorValue;

    if (currentValue.trim() === '') {
      return;
    }

    onSubmit(currentValue);
    setEditorValue('');
  };

  return (
    <div className="jv-cell-ai-input-container">
      <div className="jv-cell-ai-input-editor">
        <Editor
          defaultLanguage="markdown"
          theme={
            document.body.getAttribute('data-jp-theme-light') === 'true'
              ? 'vs'
              : 'vs-dark'
          }
          value={editorValue}
          onChange={handleEditorChange}
          onMount={handleEditorMount}
          options={{
            minimap: { enabled: false },
            lineNumbers: 'off',
            glyphMargin: false,
            folding: false,
            wordWrap: 'on',
            wrappingIndent: 'same',
            automaticLayout: true,
            scrollBeyondLastLine: false,
            readOnly: !isEnabled,
            placeholder: isEnabled ? placeholderEnabled : placeholderDisabled
          }}
        />
      </div>
      <div className="jv-cell-ai-input-buttons">
        <Button
          onClick={handleSubmit}
          disabled={!isEnabled || editorValue.trim() === ''}
          className="jv-cell-ai-input-submit-button"
        >
          Submit
          <span style={{ fontSize: '0.7em', marginLeft: '5px' }}>Enter</span>
        </Button>
        <Button onClick={onCancel} className="jv-cell-ai-input-cancel-button">
          Cancel
          <span style={{ fontSize: '0.7em', marginLeft: '5px' }}>Escape</span>
        </Button>
      </div>
    </div>
  );
};

export default InputComponent;
