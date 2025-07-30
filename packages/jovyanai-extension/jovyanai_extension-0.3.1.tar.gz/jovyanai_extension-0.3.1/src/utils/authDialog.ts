import { Dialog } from '@jupyterlab/apputils';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { Widget } from '@lumino/widgets';
import { createRoot } from 'react-dom/client';
import React from 'react';
import { AuthReminder } from '../authReminder/authReminder'; // Adjust path as needed

/**
 * Shows an authentication reminder dialog.
 * @param settingRegistry - The ISettingRegistry instance.
 * @returns A promise that resolves to true if the dialog was cancelled by the user,
 *          false otherwise (e.g., connection established or dialog closed implicitly).
 */
export function showAuthReminderDialog(
  settingRegistry: ISettingRegistry | null | undefined
): Promise<boolean> {
  // Returns a promise that resolves to true if cancelled, false otherwise.
  return new Promise(resolve => {
    if (!settingRegistry) {
      console.error('SettingRegistry not provided to showAuthReminderDialog.');
      resolve(true); // Treat as cancellation if registry is missing
      return;
    }

    const body = document.createElement('div');
    const root = createRoot(body);
    let dialog: Dialog<any> | null = null;
    let bodyWidget: Widget | null = null;
    let explicitlyClosed = false;

    const closeDialogAndResolve = (didCancel: boolean) => {
      if (explicitlyClosed) {
        return;
      }
      explicitlyClosed = true;
      console.debug(`Auth Dialog close requested. Cancelled: ${didCancel}`);
      try {
        root.unmount();
      } catch (e) {
        console.warn('Error unmounting React root during close:', e);
      }
      if (dialog && !dialog.isDisposed) {
        dialog.dispose();
        dialog = null;
      }
      if (bodyWidget && !bodyWidget.isDisposed) {
        bodyWidget.dispose();
        bodyWidget = null;
      }
      resolve(didCancel);
    };

    const handleConnected = () => {
      console.debug('AuthReminder reported connected.');
      closeDialogAndResolve(false);
    };

    const handleCancel = () => {
      console.debug('AuthReminder cancelled by component.');
      closeDialogAndResolve(true);
    };

    const authReminderComponent = React.createElement(AuthReminder, {
      settingRegistry: settingRegistry,
      onConnected: handleConnected,
      onCancel: handleCancel
    });
    root.render(authReminderComponent);

    bodyWidget = new Widget({ node: body });

    dialog = new Dialog({
      title: 'Jovyan AI Authentication',
      body: bodyWidget,
      buttons: []
    });

    dialog.disposed.connect(() => {
      dialog = null;
      if (bodyWidget && !bodyWidget.isDisposed) {
        bodyWidget.dispose();
      }
      bodyWidget = null;
    });
    if (bodyWidget) {
      bodyWidget.disposed.connect(() => {
        bodyWidget = null;
      });
    }

    dialog
      .launch()
      .then(() => {
        console.debug('Dialog launch() promise resolved (dialog closed).');
        if (!explicitlyClosed) {
          console.debug('Dialog closed implicitly. Treating as Cancel.');
          closeDialogAndResolve(true);
        }
        dialog = null;
        bodyWidget = null;
      })
      .catch(error => {
        if (!explicitlyClosed) {
          console.error('Error during dialog lifecycle:', error);
          console.debug('Treating dialog error as Cancel.');
          closeDialogAndResolve(true);
        } else {
          console.debug(
            'Dialog launch promise rejected, likely due to explicit closure:',
            error
          );
        }
        dialog = null;
        bodyWidget = null;
      });
  });
}
