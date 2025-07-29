'use client'; // Add if this provider is used in client components

import React, {
  createContext,
  useContext,
  useState,
  ReactNode,
  useCallback,
  useMemo,
  useEffect
} from 'react';
import { Context } from './types/context'; // Check path
import { useNotebookController } from '../context/NotebookControllerContext'; // Check path
import { CellData } from '../utils/extractCellData'; // Check path
import { ChatContextController } from './chatContextController'; // Import the controller class
import { NotebookPanel, INotebookTracker } from '@jupyterlab/notebook'; // Import NotebookPanel and INotebookTracker

// --- Context Definition ---

// Define the shape of the value provided by the context
export interface IChatContextValue {
  // Export if needed elsewhere, otherwise keep internal
  activeContexts: Context[];
  currentNotebookInContext: boolean;
  addContext: (context: Context) => void;
  addCurrentCellContext: () => void;
  hasCurrentCellInContext: () => boolean;
  removeContext: (context: Context) => void;
  getContextName: (context: Context) => string;
  getContextDataForApi: () => {
    currentNotebook: CellData[];
    selectedCells: CellData[];
  };
  setCurrentNotebookInContext: (value: boolean) => void;
  currentNotebookFileName: string;
}

// Create the context
const ChatContext = createContext<IChatContextValue | undefined>(undefined);

// --- Context Provider Component ---

export const ChatContextProvider: React.FC<{ children: ReactNode }> = ({
  children
}) => {
  const notebookController = useNotebookController();
  const [activeContexts, setActiveContexts] = useState<Context[]>([]);
  const [currentNotebookInContext, setCurrentNotebookInContext] =
    useState<boolean>(true);
  const [currentNotebookFileName, setCurrentNotebookFileName] =
    useState<string>('');

  // Create a stable instance of the controller logic class
  // Make sure ChatContextController is imported correctly
  const controller = useMemo(
    () => new ChatContextController(notebookController),
    [notebookController]
  );

  // Track current notebook filename
  useEffect(() => {
    // Check if notebookController and its tracker exist
    if (notebookController && (notebookController as any)._notebookTracker) {
      const tracker = (notebookController as any)._notebookTracker;

      // Define the handler function - now async and waits for context ready
      const updateFilename = async (
        sender: INotebookTracker,
        panel: NotebookPanel | null
      ) => {
        let filename = '';
        if (panel) {
          try {
            // console.debug(
            //   'Signal received. Waiting for panel context to be ready...'
            // );
            await panel.context.ready; // Wait for the context
            // console.debug('Panel context is ready.');

            // Now get the path
            const path = panel.context.contentsModel?.path;
            if (path) {
              const parts = path.split('/');
              filename = parts[parts.length - 1];
            }
            // console.debug(
            //   'Panel path after await:',
            //   path,
            //   'Extracted filename:',
            //   filename
            // );
          } catch (error) {
            console.error(
              'Error waiting for panel context or getting path:',
              error
            );
            filename = ''; // Set filename to empty on error
          }
        } else {
          // If panel is null (e.g., last notebook closed), clear filename
          // console.debug('Signal received with null panel. Clearing filename.');
          filename = ''; // Explicitly set to empty
        }

        // Check if the derived filename is different from the current state
        if (filename !== currentNotebookFileName) {
          // console.debug(
          //   'updateFilename: Notebook changed (',
          //   currentNotebookFileName,
          //   '->',
          //   filename,
          //   '). Clearing cell contexts...'
          // );
          // Clear cell contexts first
          setActiveContexts(currentContexts =>
            currentContexts.filter(ctx => ctx.type !== 'notebook-cell')
          );
          // Then, update the filename state
          setCurrentNotebookFileName(filename);
        } else {
          // If the filename is the same, just log (no state updates needed)
          // console.debug(
          //   'updateFilename: Filename (',
          //   filename,
          //   ') is the same as current state. No updates needed.'
          // );
        }

        // console.debug('updateFilename complete.');
      };

      // --- Attempt to set initial filename (Best Effort) ---
      const initialPanel = tracker.currentWidget;
      if (initialPanel) {
        // Use the async handler for the initial panel too, for consistency
        // console.debug(
        //   'Initial check: Found active widget. Calling updateFilename...'
        // );
        updateFilename(tracker, initialPanel);
      } else {
        // console.debug(
        //   'Initial check: No active widget found. Waiting for signal.'
        // );
      }

      // --- Connect the signal ---
      tracker.currentChanged.connect(updateFilename);
      // console.debug('Connected to tracker.currentChanged');

      // --- Cleanup ---
      return () => {
        // console.debug('Disconnecting from tracker.currentChanged');
        // Clear timeout (if we were still using it)
        // if (timeoutId) clearTimeout(timeoutId);
        // Disconnect signal
        if ((notebookController as any)?._notebookTracker) {
          try {
            (
              notebookController as any
            )._notebookTracker.currentChanged.disconnect(updateFilename);
          } catch (error) {
            console.warn('Error disconnecting from tracker signal:', error);
          }
        }
      };
    } else {
      // Handle case where controller or tracker is not available
      console.debug('Notebook controller or tracker not found initially.');
      setCurrentNotebookFileName(''); // Reset filename if controller/tracker disappears
    }
    // Dependency array: Re-run the effect if notebookController instance changes
    // No longer need currentNotebookFileName here as we read from signal/initial check
  }, [notebookController]);

  // --- Callback functions using the controller logic ---
  const addCurrentNotebookContextCallback = useCallback(() => {
    setActiveContexts(currentContexts =>
      controller.addCurrentNotebookContext(currentContexts)
    );
  }, [controller]);

  const addContextCallback = useCallback(
    (contextToAdd: Context) => {
      setActiveContexts(currentContexts =>
        controller.addContext(currentContexts, contextToAdd)
      );
    },
    [controller]
  ); // Depends only on the stable controller instance

  const addCurrentCellContextCallback = useCallback(() => {
    setActiveContexts(currentContexts =>
      controller.addCurrentCellContext(currentContexts)
    );
  }, [controller]);

  const removeContextCallback = useCallback(
    (contextToRemove: Context) => {
      setActiveContexts(currentContexts =>
        controller.removeContext(currentContexts, contextToRemove)
      );
    },
    [controller]
  );

  // Read functions need access to current state or controller
  const hasCurrentCellInContextCallback = useCallback(() => {
    // Logic is in controller, pass current state
    return controller.hasCurrentCellInContext(activeContexts);
  }, [controller, activeContexts]); // Depends on controller and current state

  const getContextNameCallback = useCallback(
    (context: Context) => {
      // Logic is in controller, doesn't need activeContexts state here
      return controller.getContextName(context);
    },
    [controller]
  );

  const getContextDataForApiCallback = useCallback(() => {
    // Logic is in controller, pass current state
    return controller.getContextDataForApi(
      activeContexts,
      currentNotebookInContext
    );
  }, [controller, activeContexts, currentNotebookInContext]);

  const setCurrentNotebookInContextCallback = useCallback((value: boolean) => {
    setCurrentNotebookInContext(value);
  }, []);

  // --- Effect to handle external command for adding cell context ---
  useEffect(() => {
    const handleAddCellContextEvent = () => {
      console.debug(
        'Received jovyanai:addCurrentCellContext event, calling callback.'
      );
      addCurrentCellContextCallback();
    };

    document.body.addEventListener(
      'jovyanai:addCurrentCellContext',
      handleAddCellContextEvent
    );
    console.debug(
      'ChatContextProvider mounted, listening for jovyanai:addCurrentCellContext event.'
    );

    return () => {
      document.body.removeEventListener(
        'jovyanai:addCurrentCellContext',
        handleAddCellContextEvent
      );
      console.debug(
        'ChatContextProvider unmounted, removing listener for jovyanai:addCurrentCellContext event.'
      );
    };
  }, [addCurrentCellContextCallback]); // Re-run if the callback instance changes

  // --- Context Value ---
  // Assemble the value to be provided by the context
  const providerValue: IChatContextValue = useMemo(
    () => ({
      activeContexts,
      currentNotebookInContext,
      currentNotebookFileName,
      addContext: addContextCallback,
      addCurrentCellContext: addCurrentCellContextCallback,
      hasCurrentCellInContext: hasCurrentCellInContextCallback,
      removeContext: removeContextCallback,
      getContextName: getContextNameCallback,
      getContextDataForApi: getContextDataForApiCallback,
      addCurrentNotebookContext: addCurrentNotebookContextCallback,
      setCurrentNotebookInContext: setCurrentNotebookInContextCallback
    }),
    [
      activeContexts,
      currentNotebookInContext,
      currentNotebookFileName,
      addContextCallback,
      addCurrentCellContextCallback,
      hasCurrentCellInContextCallback,
      removeContextCallback,
      getContextNameCallback,
      getContextDataForApiCallback,
      addCurrentNotebookContextCallback,
      setCurrentNotebookInContextCallback
    ]
  );

  return React.createElement(
    ChatContext.Provider,
    { value: providerValue },
    children
  );
};

// --- Hook to use the context ---
export const useChatContext = (): IChatContextValue => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChatContext must be used within a ChatContextProvider');
  }
  return context;
};
