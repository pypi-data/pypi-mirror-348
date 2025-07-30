import React, { useState, useEffect, useRef } from 'react';
// import { RefreshCw, X } from 'lucide-react'; // Removed unused imports
import '../../../style/chat-header.css';
import { useNotebookController } from '../../context/NotebookControllerContext';
import { getJovyanClient, clientIsConnected } from '../../jovyanClient'; // Added jovyanClient import
import { Chat } from '@jovyan/client'; // Added Chat type import
import { formatRelativeTime } from '../../utils/time'; // Added time utility import

interface IChatHeaderProps {
  title: string;
  onNewChat: () => void;
  onLoadChat: (chatId: string) => void; // Added prop to handle loading a chat
}

export const ChatHeader: React.FC<IChatHeaderProps> = ({
  title,
  onNewChat,
  onLoadChat
}) => {
  const notebookController = useNotebookController();
  const [showHistory, setShowHistory] = useState(false);
  const [recentChats, setRecentChats] = useState<Chat[]>([]);
  const historyDropdownRef = useRef<HTMLDivElement>(null); // Ref for dropdown

  const handleClose = () => {
    notebookController.runCommand('jovyanai:toggle-chat');
  };

  const handleHistoryClick = async () => {
    if (showHistory) {
      setShowHistory(false);
    } else {

      try {
        const client = await getJovyanClient();

        if (!clientIsConnected()) {
          console.debug('Client not connected, skipping getChats');
          setRecentChats([]);
          setShowHistory(true);
          return;
        }

        const chats = await client.getChats();
        // Sort by creation date descending and take the top 10
        const sortedChats = chats
          .sort(
            (a, b) =>
              new Date(b.created_at).getTime() -
              new Date(a.created_at).getTime()
          )
          .slice(0, 10);
        setRecentChats(sortedChats);
        setShowHistory(true);
      } catch (error) {
        console.error('Failed to fetch chat history:', error);
        // Handle error appropriately, maybe show a notification
      }
    }
  };

  const handleHistoryItemClick = (chatId: string) => {
    onLoadChat(chatId);
    setShowHistory(false); // Close dropdown after selection
  };

  // Close dropdown if clicked outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        historyDropdownRef.current &&
        !historyDropdownRef.current.contains(event.target as Node)
      ) {
        setShowHistory(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [historyDropdownRef]);

  return (
    <div className="chat-header">
      <h2>{title}</h2>
      <div className="header-controls">
        <button
          className="header-button add-button"
          onClick={onNewChat}
          title="New Chat"
        >
          <span>+</span>
        </button>
        <div className="history-container" ref={historyDropdownRef}>
          <button
            className="header-button history-button"
            onClick={handleHistoryClick}
            title="Chat History"
          >
            <span>↻</span>
          </button>
          {showHistory && recentChats.length > 0 && (
            <div className="history-dropdown">
              <ul>
                {recentChats.map(chat => (
                  <li
                    key={chat.id}
                    onClick={() => handleHistoryItemClick(chat.id)}
                  >
                    <span className="chat-title">
                      {chat.title || 'Untitled Chat'}
                    </span>
                    <span className="chat-time">
                      {formatRelativeTime(chat.created_at)}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          )}
          {showHistory && recentChats.length === 0 && (
            <div className="history-dropdown">
              <p>No chat history found.</p>
            </div>
          )}
        </div>
        {/* <button className="header-button menu-button">
          <span>⋯</span>
        </button> */}
        <button
          className="header-button close-button"
          onClick={handleClose}
          title="Close Chat"
        >
          <span>×</span>
        </button>
      </div>
    </div>
  );
};
