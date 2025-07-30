import { getJovyanClient } from '../../jovyanClient';

export const getChatTitle = async (message: string): Promise<string> => {
  // Get the Jovyan client instance
  const client = await getJovyanClient();

  try {
    const title = await client.generateChatTitle(message);
    return title || 'Chat';
  } catch (error) {
    console.error('Failed to generate chat title from backend:', error);
    return message
      .split(' ')
      .slice(0, 3)
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  }
};
