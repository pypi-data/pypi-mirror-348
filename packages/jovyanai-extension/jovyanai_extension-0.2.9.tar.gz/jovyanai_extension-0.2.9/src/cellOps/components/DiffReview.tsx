import React, { useState, useEffect, useRef } from 'react';
import { EditorView } from '@codemirror/view';
import { CodeMirrorEditor } from '@jupyterlab/codemirror';
import { EditorState, Extension } from '@codemirror/state';
import { unifiedMergeView } from '@codemirror/merge';
import { python } from '@codemirror/lang-python';
import { highlightSpecialChars } from '@codemirror/view';
import { jupyterTheme } from '@jupyterlab/codemirror';
import { Cell } from '@jupyterlab/cells';
import { ButtonsContainer } from './DiffReviewButtons';
import { stopIcon } from '@jupyterlab/ui-components';

function applyDiffToEditor(
  editor: CodeMirrorEditor,
  original: string,
  modified: string,
  isNewCodeGeneration = false
): EditorView {
  // This function
  const extensions: Extension[] = [
    python(),
    jupyterTheme,
    EditorView.editable.of(false),
    EditorState.readOnly.of(true),
    highlightSpecialChars()
  ];

  if (!isNewCodeGeneration) {
    extensions.push(
      unifiedMergeView({
        original: original,
        mergeControls: false,
        gutter: false
      })
    );
  }
  // Create a new EditorView with the diff content
  const newView = new EditorView({
    state: EditorState.create({
      doc: modified,
      extensions: extensions
    }),
    parent: editor.editor.dom
  });

  // Hide the original editor view
  editor.editor.dom.classList.add('hidden-editor');

  // Add a class for new code generation
  if (isNewCodeGeneration) {
    newView.dom.classList.add('new-code-generation');
  }

  // add a streaming-now class to the new view
  newView.dom.classList.add('streaming-now');
  // Append the new view to the same parent as the original editor
  editor.host.appendChild(newView.dom);
  return newView;
}

interface IDiffReviewProps {
  activeCell: Cell;
  oldCode: string;
  generateCodeStream: AsyncIterable<string>; // Fixed type definition
  acceptCodeHandler: (code: string) => void;
  rejectCodeHandler: () => void;
  editPromptHandler: (code: string) => void;
  acceptAndRunHandler: (code: string) => void;
  prompt: string; // Add prompt prop
  retryHandler: () => void; // Add retry handler prop
}

export const DiffReview: React.FC<IDiffReviewProps> = ({
  activeCell,
  oldCode,
  generateCodeStream,
  acceptCodeHandler,
  rejectCodeHandler,
  editPromptHandler,
  acceptAndRunHandler,
  prompt, // Destructure prompt
  retryHandler // Destructure retryHandler
}) => {
  const [diffView, setDiffView] = useState<EditorView | null>(null);
  const [stream, setStream] = useState<AsyncIterable<string> | null>(null);
  const [newCode, setNewCode] = useState<string>('');
  const [streamingDone, setStreamingDone] = useState<boolean>(false);
  const [statusText, setStatusText] = useState<string>('Thinking...');
  const buttonsRef = useRef<HTMLDivElement>(null);
  const [isCancelled, setIsCancelled] = useState<boolean>(false);
  const [isServerError, setIsServerError] = useState<boolean>(false); // Add server error state
  const timeoutId = useRef<ReturnType<typeof setTimeout> | null>(null); // Use ReturnType<typeof setTimeout>
  const firstChunkReceived = useRef<boolean>(false); // Add ref to track first chunk
  // Create the diff view once the active cell and old code are available.
  useEffect(() => {
    if (activeCell && oldCode !== undefined) {
      const editor = activeCell.editor as CodeMirrorEditor;
      const initialDiffView = applyDiffToEditor(
        editor,
        oldCode,
        oldCode,
        oldCode.trim() === '' // flag for new code generation
      );
      setDiffView(initialDiffView);
    }
    activeCell.node.scrollIntoView({
      behavior: 'smooth',
      block: 'center'
    });
  }, [activeCell, oldCode]);

  // Start the code generation stream.
  useEffect(() => {
    const initiateStream = async () => {
      try {
        setIsServerError(false); // Reset server error state on new attempt
        setStatusText('Thinking...'); // Reset status text
        setNewCode(''); // Reset new code
        setStreamingDone(false); // Reset streaming done state
        firstChunkReceived.current = false; // Reset first chunk flag

        const codeStream = generateCodeStream;
        setStream(codeStream);
      } catch (error: any) {
        console.error('Error generating code stream:', error);
        setStreamingDone(true);
        setIsServerError(true); // Set server error state
        // Don't clean up here, let the status text show the error and Try Again button
        setStatusText('Error generating code. Please try again.');
      }
    };
    initiateStream();
    // Dependency array includes generateCodeStream to re-run if it changes (e.g., on retry)
  }, [generateCodeStream]);

  // Accumulate code from the stream.
  useEffect(() => {
    if (stream) {
      const accumulate = async () => {
        firstChunkReceived.current = false; // Reset flag
        setIsServerError(false); // Reset server error state at start of accumulation
        // Set timeout for the first chunk
        timeoutId.current = setTimeout(() => {
          if (!firstChunkReceived.current) {
            setStreamingDone(true); // Stop further processing
            setIsServerError(true); // Set server error state for timeout
            setStatusText(
              'Error: Server took too long to respond. Please try again.'
            );
            // Don't clean up here, let the error message show
          }
        }, 120000); // 2 minutes timeout

        try {
          for await (const chunk of stream) {
            // Clear timeout once the first chunk arrives
            if (!firstChunkReceived.current) {
              firstChunkReceived.current = true;
              if (timeoutId.current) {
                clearTimeout(timeoutId.current);
                timeoutId.current = null;
              }
              setStatusText('Writing...'); // Update status once streaming starts
            }
            setNewCode(prevCode => prevCode + chunk);
          }
          setStreamingDone(true);
          if (firstChunkReceived.current) {
            // Only clear status if we actually received something
            setStatusText('');
          } else if (!isServerError) {
            // If stream ended without chunks and no timeout error, maybe empty response?
            setStatusText('Received empty response.'); // Or handle as appropriate
            setIsServerError(true); // Consider empty response a server issue?
          }
        } catch (error) {
          console.error('Error processing stream:', error);
          setStreamingDone(true);
          setIsServerError(true); // Assume processing errors are server-related for retry
          // Check if timeout already triggered the error message
          if (!timeoutId.current && firstChunkReceived.current) {
            setStatusText('Error processing stream.');
          } else if (!firstChunkReceived.current && !timeoutId.current) {
            // If timeout hasn't fired and we haven't received a chunk, maybe network error before timeout
            setStatusText('Error starting stream.');
          } // else timeout message is already set or will be set
        } finally {
          // Ensure timeout is cleared if stream ends or errors out before timeout fires
          if (timeoutId.current) {
            clearTimeout(timeoutId.current);
            timeoutId.current = null;
          }
        }
      };
      accumulate();
    }

    // Cleanup function to clear timeout if component unmounts or stream changes
    return () => {
      if (timeoutId.current) {
        clearTimeout(timeoutId.current);
        timeoutId.current = null;
      }
    };
  }, [stream]); // Re-run if the stream object itself changes (e.g., on retry)

  // When streaming is complete, finalize the diff view by applying fixed code.
  useEffect(() => {
    if (streamingDone && diffView) {
      diffView.dom.classList.remove('streaming-now');
      diffView.dispatch({
        changes: {
          from: 0,
          to: diffView.state.doc.length,
          insert: newCode
        }
      });
    }
  }, [streamingDone, diffView, newCode]);

  // when streming is done, scroll the button container into view
  // useEffect(() => {
  //   if (streamingDone && buttonsRef.current) {
  //     buttonsRef.current.scrollIntoView({
  //       behavior: 'smooth',
  //       block: 'center'
  //     });
  //   }
  // }, [streamingDone]);

  // Continuously update the diff view while new code arrives.
  useEffect(() => {
    if (!streamingDone && activeCell && diffView) {
      const oldCodeLines = oldCode.split('\n');
      const newCodeLines = newCode.split('\n');
      if (newCodeLines.length > 1) {
        let diffCode = '';
        if (newCodeLines.length < oldCodeLines.length) {
          diffCode = [
            ...newCodeLines.slice(0, -1),
            oldCodeLines[newCodeLines.length - 1] + '\u200B',
            ...oldCodeLines.slice(newCodeLines.length)
          ].join('\n');
        } else {
          diffCode = newCode.split('\n').slice(0, -1).join('\n');
        }
        diffView.dispatch({
          changes: {
            from: 0,
            to: diffView.state.doc.length,
            insert: diffCode
          }
        });
        // Optionally, mark the last changed line.
        const changedLines = diffView.dom.querySelectorAll('.cm-changedLine');
        if (changedLines.length > 0) {
          changedLines[
            changedLines.length - 1
          ].previousElementSibling?.classList.add('hidden-diff');
        }
      }
    }
  }, [newCode, streamingDone, activeCell, diffView, oldCode]);

  const cleanUp = () => {
    // remove the diff review and restore the original editor
    const diffReviewContainer = diffView?.dom;
    if (diffReviewContainer) {
      diffReviewContainer.remove();
    }
    const editor = activeCell.editor as CodeMirrorEditor;
    editor.editor.dom.classList.remove('hidden-editor');
    // remove the buttons container
    const buttonsContainer = buttonsRef.current;
    if (buttonsContainer) {
      buttonsContainer.remove();
    }
  };

  const onAcceptAndRun = () => {
    acceptAndRunHandler(newCode);
    cleanUp();
  };

  const onAccept = () => {
    acceptCodeHandler(newCode);
    cleanUp();
  };

  const onReject = () => {
    rejectCodeHandler();
    cleanUp();
  };

  const onEditPrompt = () => {
    editPromptHandler(newCode);
    cleanUp();
  };

  const onCancel = () => {
    setIsCancelled(true);
    setStreamingDone(true);
    setStatusText('');
    setStream(null);
    rejectCodeHandler();
    cleanUp();
  };

  const handleRetry = () => {
    // No need to call cleanUp here as the parent will re-render/replace this instance
    retryHandler();
  };

  return (
    <div>
      {statusText && !isCancelled && (
        <div className="status-container">
          {/* Show spinner only when actively streaming/thinking and not yet an error */}
          {!streamingDone && !isServerError && !isCancelled && (
            <div className="spinner-container">
              <div className="spinner-border"></div>
              <button
                className="cancel-button"
                onClick={onCancel}
                title="Cancel request"
              >
                <stopIcon.react />
              </button>
            </div>
          )}
          <p className="status-element">{statusText}</p>
          {/* Show Try Again button only on server error */}
          {isServerError && streamingDone && !isCancelled && (
            <button
              className="jp-mod-styled jp-mod-reject"
              onClick={handleRetry}
              title="Retry Request"
            >
              Try Again
            </button>
          )}
        </div>
      )}
      {diffView &&
        streamingDone &&
        !isCancelled &&
        !isServerError && ( // Only show buttons if no server error
          <ButtonsContainer
            buttonsRef={buttonsRef}
            onAcceptAndRun={onAcceptAndRun}
            onAccept={onAccept}
            onReject={onReject}
            onEditPrompt={onEditPrompt}
          />
        )}
    </div>
  );
};
