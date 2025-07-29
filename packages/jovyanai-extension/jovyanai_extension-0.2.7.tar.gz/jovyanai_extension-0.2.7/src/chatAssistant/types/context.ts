import { CellData } from '@jovyan/client';
import { NotebookController } from '../../controller';
import { convertCellToCellData } from '../../utils/extractCellData';

/**
 * Base interface for all context types
 */
export interface IBaseContext {
  id: string;
  type: string;
  getDisplayName(notebookController: NotebookController): string;
  getContextDataForApi(notebookController: NotebookController): any;
}

/**
 * Context for a file
 */
export interface IFileContext extends IBaseContext {
  type: 'file';
  format: 'text' | 'image' | 'audio';
  content: string;
  path: string;
}

export class NotebookCellContext implements IBaseContext {
  readonly type = 'notebook-cell';
  readonly id: string;
  readonly notebookId: string;

  constructor(cellId: string, notebookId: string) {
    this.id = cellId;
    this.notebookId = notebookId;
  }

  getDisplayName(notebookController: NotebookController): string {
    const cell = notebookController.getCellById(this.id);
    if (cell) {
      const index = notebookController.getCurrentNotebookCells().indexOf(cell);
      return `cell ${index >= 0 ? index + 1 : '?'.toString()}`;
    }
    return 'Unknown Cell';
  }

  getContextDataForApi(
    notebookController: NotebookController
  ): CellData | null {
    const cell = notebookController.getCellById(this.id);
    if (cell) {
      return convertCellToCellData(cell);
    }
    return null;
  }
}

export class NotebookContext implements IBaseContext {
  readonly type = 'notebook';
  id: string;

  constructor(notebookId: string) {
    this.id = notebookId;
  }

  getDisplayName(notebookController: NotebookController): string {
    // return the filename of the notebook
    return this.id.split('/').pop() || this.id;
  }

  getContextDataForApi(notebookController: NotebookController): CellData[] {
    const cells = notebookController.getCurrentNotebookCells();
    return cells.map(cell => convertCellToCellData(cell));
  }
}

/**
 * Union type of all possible context types
 */
export type Context = IFileContext | NotebookCellContext | NotebookContext;
