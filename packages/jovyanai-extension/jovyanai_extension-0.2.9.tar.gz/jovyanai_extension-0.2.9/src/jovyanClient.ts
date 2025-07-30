import { JovyanClient } from '@jovyan/client';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { ServerConnection } from '@jupyterlab/services';

// Default settings
let backendUrl = 'wss://backend.jovyan-ai.com';
// let authToken = ''; // authToken will now be determined dynamically

// Global client instance
let jovyanClientInstance: JovyanClient | null = null;

// Connection state management
let isConnecting = false;
let connectionPromise: Promise<JovyanClient> | null = null;
let isConnected = false;

// Function to fetch token from the backend endpoint
const fetchTokenFromServer = async (): Promise<string | null> => {
  try {
    const settings = ServerConnection.makeSettings();
    const response = await ServerConnection.makeRequest(
      `${settings.baseUrl}jovyanai_token`, // Correct endpoint path relative to base URL
      { method: 'GET' },
      settings
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    if (data && data.token) {
      console.info('[JovyanAI] Fetched token from backend.');
      return data.token;
    } else {
      console.info('[JovyanAI] Backend endpoint did not provide a token.');
      return null;
    }
  } catch (error) {
    console.error('Failed to fetch token from backend:', error);
    return null;
  }
};

// Function to initialize settings from the registry
export const initializeClient = async (
  settingRegistry: ISettingRegistry
): Promise<void> => {
  console.debug('Initializing client from settings...');
  let settingsObject: ISettingRegistry.ISettings | null = null;
  let localAuthToken: string | null = null;

  try {
    settingsObject = await settingRegistry.load(
      '@jovyanai/labextension:plugin'
    );

    backendUrl = settingsObject.get('backendUrl').composite as string;
    localAuthToken = settingsObject.get('authToken').composite as string;

    console.debug(
      `Loaded settings: backendUrl=${backendUrl}, authToken=${localAuthToken ? '***' : '<empty>'}`
    );

    // If token is missing in settings, try fetching from the backend
    if (!localAuthToken) {
      console.debug(
        'Auth token missing in settings, attempting to fetch from backend...'
      );
      const fetchedToken = await fetchTokenFromServer();
      if (fetchedToken) {
        localAuthToken = fetchedToken;
        // Save the fetched token back to settings
        try {
          await settingsObject.set('authToken', fetchedToken);
          console.debug('Saved fetched token to settings.');
        } catch (saveError) {
          console.error('Failed to save fetched token to settings:', saveError);
          // Continue without saving, but use the fetched token for this session
        }
      } else {
        console.warn('Could not retrieve auth token from settings or backend.');
        // localAuthToken remains null or empty
      }
    } else {
      console.debug('Using auth token from settings.');
    }

    // Create the new client instance with the determined token (might still be empty)
    console.debug('Creating new JovyanClient instance.');
    // Ensure authToken is a string, even if null/undefined was fetched/set
    jovyanClientInstance = new JovyanClient(
      backendUrl,
      localAuthToken || '',
      ''
    );

    // Reset connection state as we have a new instance
    isConnecting = false;
    connectionPromise = null;
    isConnected = false;
    console.debug('JovyanClient instance created (not connected yet).');
  } catch (error) {
    console.error('Failed to load settings or create client instance:', error);
    jovyanClientInstance = null;
    isConnecting = false;
    connectionPromise = null;
    isConnected = false;
  }
};

export const getJovyanClient = async (): Promise<JovyanClient> => {
  if (!jovyanClientInstance) {
    // This might happen if initializeClient failed or hasn't run yet.
    // Maybe wait for initialization? Or throw a clearer error.
    console.error(
      'getJovyanClient called before instance was successfully created.'
    );
    throw new Error(
      'JovyanClient instance not available. Initialization might have failed.'
    );
  }

  // If already connected, return immediately.
  if (isConnected) {
    console.debug('getJovyanClient: Already connected.');
    return jovyanClientInstance;
  }

  // If currently connecting, wait for the existing connection attempt to finish.
  if (isConnecting && connectionPromise) {
    console.debug('getJovyanClient: Connection in progress, waiting...');
    try {
      // Wait for the ongoing connection attempt
      await connectionPromise;
      // Check status again after waiting, as it might have failed
      if (isConnected) {
        console.debug('getJovyanClient: Waited for connection, now connected.');
        return jovyanClientInstance;
      } else {
        console.warn('getJovyanClient: Waited for connection, but it failed.');
        // Decide whether to retry or throw. Throwing seems safer to avoid loops.
        throw new Error('Connection attempt failed.');
      }
    } catch (error) {
      console.error(
        'getJovyanClient: Error while waiting for connection:',
        error
      );
      throw error; // Re-throw the error from the failed connection attempt
    }
  }

  // If not connected and not connecting, start a new connection attempt.
  console.debug('getJovyanClient: Not connected, initiating connection...');
  isConnecting = true;
  const currentInstance = jovyanClientInstance; // Capture instance in case it changes

  connectionPromise = (async () => {
    try {
      await currentInstance.connect();
      // Check if connect() implicitly starts session or if needed explicitly. Assuming connect handles auth/session.
      // If explicit session start is needed:
      // await currentInstance.startSession();
      console.debug('getJovyanClient: Connection and session successful.');
      isConnected = true;
      return currentInstance;
    } catch (error) {
      console.error('getJovyanClient: Failed to connect/start session:', error);
      isConnected = false;
      connectionPromise = null; // Clear promise on failure
      throw error; // Propagate the error
    } finally {
      // Regardless of success or failure, we are no longer in the 'connecting' state
      isConnecting = false;
      console.debug('getJovyanClient: Connection attempt finished.');
      // We don't clear connectionPromise here, it resolves or rejects
    }
  })();

  // The connectionPromise will handle its own errors (logging and re-throwing).
  // Simply await it and let errors propagate.
  return connectionPromise;
};

export const clientIsConnected = (): boolean => {
  // Use optional chaining in case instance is null
  return isConnected;
};
