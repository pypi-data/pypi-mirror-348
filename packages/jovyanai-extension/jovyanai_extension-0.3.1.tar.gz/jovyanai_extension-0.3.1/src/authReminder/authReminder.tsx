import React, { useState, useCallback } from 'react';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
// Import real client functions
import { getJovyanClient } from '../jovyanClient';

interface IAuthReminderProps {
  /**
   * JupyterLab Settings Registry instance.
   */
  settingRegistry: ISettingRegistry;
  /**
   * Optional callback triggered upon successful connection.
   */
  onConnected?: () => void;
  /**
   * Optional callback triggered when the user cancels.
   */
  onCancel?: () => void;
}

/**
 * A React component prompting the user for an auth token
 * and attempting to save it and establish a connection.
 */
export const AuthReminder: React.FC<IAuthReminderProps> = ({
  settingRegistry,
  onConnected,
  onCancel
}) => {
  const [token, setToken] = useState<string>('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleSubmit = useCallback(
    async (event: React.FormEvent) => {
      event.preventDefault();
      setIsLoading(true);
      setError(null);

      try {
        // 1. Validate token (basic check)
        if (!token.trim()) {
          throw new Error('Token cannot be empty.');
        }

        // 2. Save the token to settings
        await settingRegistry.set(
          '@jovyanai/labextension:plugin',
          'authToken',
          token
        );
        console.debug('Auth token setting updated.');

        // 3. Re-initialize the client with the new settings (including the token)
        //    This function reads settings and attempts connection.
        const client = await getJovyanClient();
        try {
          // Explicitly check connection status AFTER attempting to connect
          if (client.isConnected) {
            console.debug('Connection successful.');
            if (onConnected) {
              onConnected();
            }
          } else {
            // This case might happen if connect() resolves but connection fails silently
            // or if the status check has latency. Provide feedback.
            console.error(
              'Connection attempt finished, but client is not connected.'
            );
            throw new Error(
              'Connection failed. Please verify your token and network.'
            );
          }
        } catch (err: any) {
          console.error('Failed to connect:', err);
          // Keep the original error message if available, otherwise provide a default
          const connectionError =
            err.message && err.message.includes('Connection failed')
              ? err.message
              : 'Connection failed. Please check your token and network.';
          throw new Error(connectionError);
        }
      } catch (err: any) {
        console.error('Failed to save token or connect:', err);
        setError(err.message || 'An unexpected error occurred.');
      } finally {
        setIsLoading(false);
      }
    },
    [token, settingRegistry, onConnected]
  );

  // Basic styling, can be replaced with JupyterLab UI components later
  return (
    <div className="jp-AuthReminder-container">
      <h4>Please enter your authentication token to proceed:</h4>
      <p>
        Your token is available in your Jovyan AI account{' '}
        <a href="https://jovyan-ai.com/account">here</a>.
      </p>
      <form onSubmit={handleSubmit} className="jp-AuthReminder-form">
        <input
          type="password"
          value={token}
          onChange={e => setToken(e.target.value)}
          placeholder="Enter your token"
          disabled={isLoading}
          className="jp-AuthReminder-input"
        />
        <button
          type="submit"
          disabled={isLoading || !token.trim()}
          className="jp-AuthReminder-button jp-AuthReminder-button-submit"
        >
          {isLoading ? 'Connecting...' : 'Connect'}
        </button>
        <button
          type="button"
          onClick={onCancel}
          disabled={isLoading}
          className="jp-AuthReminder-button"
        >
          Cancel
        </button>
      </form>
      {error && <p className="jp-AuthReminder-error">Error: {error}</p>}
    </div>
  );
};
