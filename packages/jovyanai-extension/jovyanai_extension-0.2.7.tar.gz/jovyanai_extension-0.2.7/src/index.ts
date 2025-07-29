import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { INotebookTracker, NotebookActions } from '@jupyterlab/notebook';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { JovyanCellController } from './cellOps/jovyanCellController';
import { NotebookController } from './controller';
import { initializeClient } from './jovyanClient';
import { attachChatAssistant } from './chatAssistant';

/**
 * Initialization data for the @jovyanai/labextension extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: '@jovyanai/labextension:plugin',
  description: 'A JupyterLab extension to integrate Jovyan AI',
  autoStart: true,
  requires: [INotebookTracker],
  optional: [ISettingRegistry],
  activate: async (
    app: JupyterFrontEnd,
    notebookTracker: INotebookTracker,
    settingRegistry: ISettingRegistry | null
  ) => {
    console.debug(
      'JupyterLab extension @jovyanai/labextension is activated! Hello!'
    );

    // Initialize settings if settingRegistry is available
    if (settingRegistry) {
      await initializeClient(settingRegistry);

      // Listen for setting changes
      settingRegistry
        .load('@jovyanai/labextension:plugin')
        .then(settings => {
          settings.changed.connect(async () => {
            await initializeClient(settingRegistry);
          });
        })
        .catch(error => {
          console.error(
            'Failed to load settings for @jovyanai/labextension:',
            error
          );
        });
    }

    // Only proceed if settingRegistry is available
    if (settingRegistry) {
      const notebookController = new NotebookController(
        notebookTracker,
        app.commands,
        settingRegistry
      );

      // on notebook active cell changed, add the cell activate button
      notebookTracker.activeCellChanged.connect((sender, cell) => {
        if (cell) {
          const jovyanCellController = new JovyanCellController(
            cell,
            notebookController
          );
          jovyanCellController.activate();
        }
      });

      // When a cell is executed, add the fix error button
      NotebookActions.executed.connect((sender, args) => {
        const cell = args.cell;
        console.debug('Cell executed', cell);
        if (cell) {
          const jovyanCellController = new JovyanCellController(
            cell,
            notebookController
          );
          jovyanCellController.addFixErrorButton();
        }
      });

      // Initialize and attach the chat assistant
      attachChatAssistant({ app, notebookController });
    } else {
      console.warn('ISettingRegistry not found, Jovyan AI features disabled.');
    }
  }
};

export default plugin;
