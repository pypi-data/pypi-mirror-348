// // Controller for the cellOps extension, responsible for handling the cellOps extension's state and interactions between the components
import { Cell } from '@jupyterlab/cells';
import { INotebookTracker, NotebookPanel } from '@jupyterlab/notebook';
import { CommandRegistry } from '@lumino/commands';
import { ISettingRegistry } from '@jupyterlab/settingregistry';

export class NotebookController {
  private _notebookTracker: INotebookTracker;
  private _commands: CommandRegistry;
  private _settingRegistry: ISettingRegistry;

  constructor(
    notebookTracker: INotebookTracker,
    commands: CommandRegistry,
    settingRegistry: ISettingRegistry
  ) {
    this._notebookTracker = notebookTracker;
    this._commands = commands;
    this._settingRegistry = settingRegistry;
  }

  public get settingRegistry(): ISettingRegistry {
    return this._settingRegistry;
  }

  public get activeCell() {
    return this._notebookTracker.currentWidget?.content.activeCell;
  }

  public addElementAfterCellInput(cell: Cell, element: HTMLElement) {
    const cellNode = cell.node;
    // Append the parentContainer to the input area of the cell
    const inputArea = cellNode.querySelector('.jp-Cell-inputWrapper');
    if (inputArea) {
      inputArea.insertAdjacentElement('afterend', element);
    } else {
      cellNode.appendChild(element);
    }
  }

  public addElementInCellChild(cell: Cell, element: HTMLElement) {
    const cellNode = cell.node;
    cellNode.appendChild(element);
  }

  public writeCodeInCell(cell: Cell, code: string) {
    cell.model.sharedModel.setSource(code);
  }

  public runCell(cell: Cell) {
    const notebook = this._notebookTracker.currentWidget;
    if (notebook) {
      notebook.content.activeCellIndex = notebook.content.widgets.indexOf(cell);
      this._commands.execute('notebook:run-cell');
    }
  }

  public insertCell(index: number, content?: string) {
    const notebook = this._notebookTracker.currentWidget;
    if (notebook) {
      notebook.model?.sharedModel.insertCell(index, {
        cell_type: 'code',
        source: content
      });
    }
  }

  public get currentCell() {
    return this._notebookTracker.currentWidget?.content.activeCell;
  }

  public get currentCellIndex(): number {
    return this._notebookTracker.currentWidget?.content.activeCellIndex || 0;
  }

  public getPreviousCells(cell: Cell): Cell[] {
    const notebook = this._notebookTracker.currentWidget?.content;
    const index = notebook?.activeCellIndex;
    if (index !== undefined && notebook) {
      return notebook.widgets.slice(0, index);
    }
    return [];
  }

  public getNextCells(cell: Cell): Cell[] {
    const notebook = this._notebookTracker.currentWidget?.content;
    const index = this.currentCellIndex;
    if (index !== undefined && notebook) {
      return notebook.widgets.slice(index + 1);
    }
    return [];
  }

  public getLanguage() {
    const notebook = this._notebookTracker.currentWidget?.model;
    const language = notebook?.defaultKernelLanguage || 'python';
    return language;
  }

  public runCommand(command: string) {
    this._commands.execute(command);
  }

  public getCurrentNotebookCells(): Cell[] {
    const notebook = this._notebookTracker.currentWidget?.content;
    if (notebook) {
      return notebook.widgets.map(widget => widget as Cell);
    }
    return [];
  }

  public getCurrentNotebookFileName(): string {
    // Get path from the widget's context contentsModel
    const path =
      this._notebookTracker.currentWidget?.context.contentsModel?.path;
    if (path) {
      // Extract filename from the path
      const parts = path.split('/');
      return parts[parts.length - 1];
    }
    return '';
  }

  public getCurrentNotebookFilePath(): string {
    // Get path from the widget's context contentsModel
    const path =
      this._notebookTracker.currentWidget?.context.contentsModel?.path;
    return path || '';
  }

  public getCellById(id: string): Cell | null {
    const notebook = this._notebookTracker.currentWidget?.content;
    if (notebook) {
      return notebook.widgets.find(widget => widget.model.id === id) as Cell;
    }
    return null;
  }

  public getNotebookByPath(path: string): NotebookPanel | null {
    let notebook: NotebookPanel | null = null;
    this._notebookTracker.forEach(panel => {
      if (panel.context.path === path) {
        notebook = panel;
      }
    });
    return notebook;
  }
}
