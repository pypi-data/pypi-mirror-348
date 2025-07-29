import { Context, NotebookCellContext, NotebookContext } from './types/context';
import { CellData } from '../utils/extractCellData';
import { NotebookController } from '../controller';

// --- Controller Class (Logic) ---
// Export the class so it can be imported by the provider
export class ChatContextController {
  private notebookController: NotebookController;

  constructor(notebookController: NotebookController) {
    this.notebookController = notebookController;
  }

  // Modifier logic: Takes current state, returns new state
  addContext(currentContexts: Context[], contextToAdd: Context): Context[] {
    if (
      !currentContexts.some(existingCtx => existingCtx.id === contextToAdd.id)
    ) {
      return [...currentContexts, contextToAdd];
    }
    return currentContexts; // Return unchanged state if already exists
  }

  // Modifier logic: Takes current state, returns new state
  addCurrentCellContext(currentContexts: Context[]): Context[] {
    const notebookPath = this.notebookController.getCurrentNotebookFilePath();
    const activeCell = this.notebookController.activeCell;
    if (activeCell) {
      const cellContext = new NotebookCellContext(
        activeCell.model.id,
        notebookPath
      );
      if (
        !currentContexts.some(
          ctx => ctx.id === cellContext.id && ctx.type === 'notebook-cell'
        )
      ) {
        console.debug('Controller adding current cell context', cellContext.id);
        return [...currentContexts, cellContext];
      } else {
        console.debug(
          'Controller: Current cell context already exists',
          cellContext.id
        );
      }
    } else {
      console.warn('Controller: No active cell found to add context for.');
    }
    return currentContexts; // Return unchanged state if no cell or already exists
  }

  addCurrentNotebookContext(currentContexts: Context[]): Context[] {
    const notebookPath = this.notebookController.getCurrentNotebookFilePath();
    if (notebookPath) {
      const notebookContext = new NotebookContext(notebookPath);
      return this.addContext(currentContexts, notebookContext);
    }
    return currentContexts;
  }

  // Modifier logic: Takes current state, returns new state
  removeContext(
    currentContexts: Context[],
    contextToRemove: Context
  ): Context[] {
    return currentContexts.filter(ctx => ctx.id !== contextToRemove.id);
  }

  // Read logic: Operates on current state
  hasCurrentCellInContext(currentContexts: Context[]): boolean {
    const activeCellId = this.notebookController.activeCell?.model.id;
    if (!activeCellId) {
      return false;
    }
    return currentContexts.some(
      ctx => ctx.id === activeCellId && ctx.type === 'notebook-cell'
    );
  }

  // Read logic: Doesn't depend on activeContexts state, only notebookController
  getContextName(context: Context): string {
    // Ensure notebookController is available, handle potential undefined case
    return this.notebookController
      ? context.getDisplayName(this.notebookController)
      : 'Context';
  }

  // Read logic: Operates on current state
  getContextDataForApi(
    currentContexts: Context[],
    currentNotebookInContext: boolean
  ): {
    currentNotebook: CellData[];
    selectedCells: CellData[];
  } {
    if (!this.notebookController) {
      console.error(
        'NotebookController not available in ChatContextController logic'
      );
      return { currentNotebook: [], selectedCells: [] };
    }

    const currentNotebookContext = new NotebookContext(
      this.notebookController.getCurrentNotebookFilePath()
    );
    const currentNotebook = currentNotebookInContext
      ? currentNotebookContext.getContextDataForApi(this.notebookController)
      : [];
    const selectedCells = currentContexts
      .filter(ctx => ctx.type === 'notebook-cell')
      .map(ctx => ctx.getContextDataForApi(this.notebookController));

    return {
      currentNotebook: currentNotebook,
      selectedCells: selectedCells.filter(
        (cell): cell is CellData => cell !== null
      )
    };
  }
}
