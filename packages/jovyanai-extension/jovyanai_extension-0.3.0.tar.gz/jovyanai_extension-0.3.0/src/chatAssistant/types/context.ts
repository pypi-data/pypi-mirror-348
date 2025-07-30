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

export class DocumentContext implements IBaseContext {
  readonly type = 'document';
  id: string;
  name: string;
  file?: File | null;
  link?: string | null;

  constructor(
    id: string,
    name: string,
    file: File | null,
    link: string | null
  ) {
    this.id = id;
    this.name = name;
    this.file = file;
    this.link = link;
  }

  getDisplayName(notebookController?: NotebookController): string {
    return this.name;
  }

  // The data sent to API might be different, handled by ChatContextController
  getContextDataForApi(notebookController?: NotebookController): any {
    return {
      id: this.id,
      name: this.name,
      type: this.type,
      hasFile: !!this.file,
      link: this.link
    };
  }
}

export class GitRepoContext implements IBaseContext {
  readonly type = 'git-repo';
  id: string;
  name: string;
  url: string | null;

  constructor(id: string, name: string, url: string | null) {
    this.id = id;
    this.name = name;
    this.url = url;
  }

  getDisplayName(notebookController?: NotebookController): string {
    return this.name;
  }

  getContextDataForApi(notebookController?: NotebookController): any {
    return {
      id: this.id,
      name: this.name,
      type: this.type,
      url: this.url
    };
  }
}

/**
 * Union type of all possible context types
 */
export type Context =
  | IFileContext
  | NotebookCellContext
  | NotebookContext
  | DocumentContext
  | GitRepoContext;
