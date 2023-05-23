import React from 'react';
import { ChatsOverview } from './Components/ChatsOverview';
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import './App.css';
import { ChatsContext, chatsMock } from './Contexts/ChatsContext';
import { ChatDrill } from './Components/ChatDrill';
import { RouterProvider, createBrowserRouter, useLocation } from 'react-router-dom';
import { ChatContent } from './Components/ChatContent';

function App() {
  const router = createBrowserRouter([
    {
      path: "/",
      element: <ChatsOverview/>
    },
    {
      path: "/chat/:chatIndex",
      element: <ChatDrill/>
    },
    {
      path: "/chat-content/:chatIndex",
      element: <ChatContent/>
    }
  ]);

  return (
    <ChatsContext.Provider value={chatsMock}>
      <div className="App">
        <RouterProvider router={router} />
      </div>
    </ChatsContext.Provider>
  );
}

export default App;
