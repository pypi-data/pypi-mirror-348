'use client';

import React from 'react';
import { useState, useRef, useEffect } from 'react';
import '../../../style/chat-interface.css';
import { ChatHeader } from './chat-header';
import { ChatInput } from './chat-input';
import { ChatMessage } from './chat-message';
import { IMessage } from '../types';
import { getJovyanClient, clientIsConnected } from '../../jovyanClient';
import { useChatContext } from '../ChatContextProvider';
import { getChatTitle } from './utils';
// Define props interface for the component
export interface IChatInterfaceProps {
  // onMessageSent: (message: IMessage) => Promise<AsyncIterableIterator<string>>;
  title?: string;
}

const getLastChat = async () => {
  if (!clientIsConnected()) {
    console.debug('Client not connected, skipping getLastChat');
    return null;
  }
  const client = await getJovyanClient();
  const chats = await client.getChats();
  // console.debug('Get chats', chats);
  // if last chat exists
  if (chats.length > 0) {
    const lastChat = chats.sort(
      (a, b) =>
        new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
    )[0];
    // if last chat has messages
    const messages = await client.getMessages(lastChat.id);
    // console.debug('Get messages', messages);
    if (messages.length > 0) {
      return { chat: lastChat, messages: messages };
    }
  }
};

export const ChatInterface: React.FC<IChatInterfaceProps> = () => {
  const [messages, setMessages] = useState<IMessage[]>([]);
  const [currentChatId, setCurrentChatId] = useState<string | null>(null);
  // const [toolUses, setToolUses] = useState<IToolUse[]>([]);
  // const [currentTool, setCurrentTool] = useState<IToolUse | null>(null);
  const [isStreaming, setIsStreaming] = useState<boolean>(false);
  const [isThinking, setIsThinking] = useState<boolean>(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatContextController = useChatContext();
  const [chatTitle, setChatTitle] = useState<string>('');
  // Function to handle creating a new chat
  const handleNewChat = () => {
    setMessages([]); // Reset the messages state
    setCurrentChatId(null);
    setIsStreaming(false);
    setIsThinking(false);
    setChatTitle('New Chat');
    // only create new chat on the first message sent
  };

  const handleCancel = async () => {
    console.debug('Cancel requested');
    // TODO: Implement actual cancellation logic with the JovyanClient
    setIsStreaming(false);
    setIsThinking(false);
    // Optionally remove the streaming placeholder message
    setMessages(prev =>
      prev.filter(
        msg => !(msg.role === 'assistant' && msg.isStreaming === true)
      )
    );
  };

  // at mount, get latest chat
  useEffect(() => {
    const loadLatestChat = async () => {
      const lastChat = await getLastChat();
      if (!lastChat) {
        console.debug('No last chat found, skipping loadLatestChat');
        setChatTitle('New Chat');
        return;
      }
      console.debug('Get latest chat', lastChat);

      if (lastChat) {
        // console.debug('Loading latest chat', lastChat);
        setCurrentChatId(lastChat.chat.id);
        const sortedMessages = lastChat.messages
          .sort(
            (a, b) =>
              new Date((a as any).created_at).getTime() -
              new Date((b as any).created_at).getTime()
          )
          .map(msg => ({
            role: (msg as any).sender,
            content: (msg as any).content
          }));
        setMessages(sortedMessages);
        // Handle potentially async title
        const titleToSet =
          lastChat.chat.title ||
          (await getChatTitle((lastChat.messages[0] as any).content));
        setChatTitle(titleToSet);
        //scroll to bottom
        const client = await getJovyanClient();
        client.setCurrentChatId(lastChat.chat.id);

        // Scrolling is now handled by the useEffect hook below
      }
    };
    loadLatestChat();
    padChatColumn('off');
    // Scrolling on initial load is handled within loadLatestChat
  }, []);

  const handleSendMessage = async (message: IMessage) => {
    // start streaming response
    setIsStreaming(true);
    // add user message to messages
    setMessages(prev => [...prev, message]);
    setIsThinking(true);
    setIsStreaming(false);
    padChatColumn('on'); // Add padding before scrolling

    const client = await getJovyanClient();
    await client.connect();

    if (!currentChatId) {
      console.debug('Creating new chat');
      const title = await getChatTitle(message.content); // Await the title
      const newChat = await client.createChat(title); // Use the resolved title
      setChatTitle(title); // Use the resolved title
      setCurrentChatId(newChat.id);
      client.setCurrentChatId(newChat.id); // Ensure new chat ID is set
    }
    console.debug('Current chat ID', currentChatId);

    const contextData = chatContextController.getContextDataForApi();
    console.debug('Context data', contextData);
    // --- End Context Gathering Logic ---

    let accumulatedContent = '';
    let firstChunkReceived = false;

    client
      .sendChatUserMessageStream(message.content, contextData, chunk => {
        if (!firstChunkReceived) {
          setIsThinking(false);
          setIsStreaming(true);
          firstChunkReceived = true;

          const initialNewMessage: IMessage = {
            role: 'assistant',
            content: chunk,
            isStreaming: true
          };
          setMessages(prev => [...prev, initialNewMessage]);
          accumulatedContent = chunk;
        } else {
          accumulatedContent += chunk;
          setMessages(prev => {
            const updatedMessages = [...prev];
            const streamingMessageIndex = updatedMessages.findIndex(
              msg => msg.role === 'assistant' && msg.isStreaming === true
            );

            if (streamingMessageIndex !== -1) {
              updatedMessages[streamingMessageIndex].content =
                accumulatedContent;
            }
            return updatedMessages;
          });
        }
      })
      .then(async () => {
        setMessages(prev => {
          return prev.map(msg =>
            msg.role === 'assistant' && msg.isStreaming === true
              ? { ...msg, content: accumulatedContent, isStreaming: false }
              : msg
          );
        });
        setIsStreaming(false);
      })
      .catch(error => {
        console.error('Error streaming chat message:', error);
        setIsThinking(false);
        setIsStreaming(false);
        setMessages(prev =>
          prev.filter(
            msg => !(msg.role === 'assistant' && msg.isStreaming === true)
          )
        );
      })
      .finally(() => {
        setIsThinking(false);
        setIsStreaming(false);
        padChatColumn('off');
      });
  };

  const padChatColumn = (status: string): void => {
    const chatColumn = messagesEndRef.current?.parentElement;
    if (!chatColumn) {
      return;
    }
    if (status === 'on') {
      // Use a large padding value to ensure enough scroll space
      chatColumn.style.paddingBottom = '100vh';
    } else {
      // Reset padding, calculating dynamically based on the last user message if possible
      const defaultPadding = '80px';
      chatColumn.style.paddingBottom = defaultPadding; // Set default first

      // Try to calculate padding based on the last user message height
      // -1: messagesEndRef, -2: last assistant message, -3: last user message
      const lastUserMessageBox = chatColumn.children[
        chatColumn.children.length - 3
      ] as HTMLElement;

      if (lastUserMessageBox && lastUserMessageBox.clientHeight) {
        // Calculate required padding to keep the user message visible, with some buffer
        // Aim to have roughly (viewport height - message height - buffer) space below the message
        const calculatedPadding = `calc(100vh - ${lastUserMessageBox.offsetTop}px - ${lastUserMessageBox.clientHeight}px - 100px)`; // Adjust 100px buffer as needed
        // Use the larger of the default or calculated padding
        chatColumn.style.paddingBottom = `max(${defaultPadding}, ${calculatedPadding})`;
        console.debug(
          'Calculated paddingBottom:',
          chatColumn.style.paddingBottom
        );
      } else {
        console.debug(
          'Could not find last user message box or its height for padding calculation.'
        );
      }
    }
  };

  // Auto-scroll user message to top when they send one
  useEffect(() => {
    // Only scroll if there are messages and the last one is from user
    if (messages.length > 0 && messages[messages.length - 1].role === 'user') {
      scrollMessages();
    } else {
      // For other cases (initial load, history load, assistant message finished), scroll to bottom
      // Ensure messages exist before trying to scroll
      if (messages.length > 0 && isStreaming === false) {
        padChatColumn('off');
        requestAnimationFrame(() => {
          messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
        });
      }
    }
  }, [messages.length]); // Dependency ensures this runs when messages array updates

  // Function to scroll the latest message (usually user's) towards the top
  const scrollMessages = () => {
    // Use requestAnimationFrame to ensure DOM updates are painted
    requestAnimationFrame(() => {
      if (messagesEndRef.current) {
        const parentElement = messagesEndRef.current.parentElement;
        console.debug('Scroll messages', parentElement);
        if (!parentElement) {
          return;
        }
        // Target the second to last element, which should be the user's latest message
        const lastMessageBox = messagesEndRef.current.previousElementSibling;
        console.debug('Scroll messages', lastMessageBox);
        if (!lastMessageBox) {
          // If no message yet, scroll to top
          parentElement.scrollTo({ top: 0, behavior: 'smooth' });
          return;
        }
        // Calculate the desired scroll position to bring the message near the top
        const messageTop = (lastMessageBox as HTMLElement).offsetTop;
        const desiredScrollTop = messageTop - 100; // Adjust the offset (100px) as needed
        console.debug('Scroll messages', desiredScrollTop);
        parentElement.scrollTo({
          top: desiredScrollTop,
          behavior: 'smooth'
        });
      }
    });
  };

  // Render messages and tool uses in chronological order
  const renderChatItems = () => {
    // Combine messages and tool uses and sort by timestamp
    const allItems = [
      ...messages.map(msg => ({
        type: 'message',
        data: msg
      }))
    ];

    return allItems.map((item, index) => {
      if (item.type === 'message') {
        return <ChatMessage key={index} message={item.data as IMessage} />;
      }
      // Handle other item types if necessary
      return null;
    });
  };

  const handleLoadChat = async (chatId: string) => {
    console.debug('Loading chat', chatId);
    const client = await getJovyanClient();
    client.setCurrentChatId(chatId);
    const fetchedMessages = await client.getMessages(chatId);
    const sortedMessages = fetchedMessages
      .sort(
        (a, b) =>
          new Date((a as any).created_at).getTime() -
          new Date((b as any).created_at).getTime()
      )
      .map(msg => ({
        role: (msg as any).sender,
        content: (msg as any).content
      }));
    setMessages(sortedMessages);
    setCurrentChatId(chatId);
    // Scroll to bottom after messages are set and rendered
    // Scrolling is now handled by the useEffect hook below
  };

  return (
    <div className="chat-container">
      <ChatHeader
        title={chatTitle}
        onNewChat={handleNewChat}
        onLoadChat={handleLoadChat}
      />

      <div className="chat-content">
        <div className="messages-container">
          {renderChatItems()}
          {isThinking && (
            <ChatMessage
              message={{ role: 'assistant', content: '' }}
              isThinking
            />
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      <ChatInput
        onSendMessage={handleSendMessage}
        onCancel={handleCancel}
        disabled={isStreaming || isThinking}
      />
    </div>
  );
};
