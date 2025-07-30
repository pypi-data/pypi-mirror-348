import { createContext, useContext } from 'react';
import { NotebookController } from '../controller'; // Adjust path if necessary

export const NotebookControllerContext = createContext<
  NotebookController | undefined
>(undefined);

export const useNotebookController = () => {
  const context = useContext(NotebookControllerContext);
  if (context === undefined) {
    throw new Error(
      'useNotebookController must be used within a NotebookControllerProvider'
    );
  }
  return context;
};
