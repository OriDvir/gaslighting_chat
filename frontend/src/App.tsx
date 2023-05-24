import React, { useEffect, useState } from 'react';
import { ChatsOverview } from './Components/ChatsOverview';
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import './App.css';
import { ChatsContext } from './Contexts/ChatsContext';
import { ChatDrill } from './Components/ChatDrill';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';
import { ChatContent } from './Components/ChatContent';
import axios from "axios";
import { map, flattenDeep } from 'lodash';


const words = ["you"]

function App() {
  const [chatsState, setChatsState] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
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

  useEffect(() => {
    (async () => {
      await axios.get("http://10.81.1.45:8000/init/short_chat.translated?translate=False")
      const {data: scores} = await axios.get("http://10.81.1.45:8000/db/get_score") as any;
      let promises = words.map(word => axios.get("http://10.81.1.45:8000/db/get_lines/" + word));
      let lines = (await Promise.all(promises)).map((promise) => promise.data);
      let wordCountsPromises = words.map(word => axios.get("http://10.81.1.45:8000/db/get_word_count/" + word));
      let wordCounts = (await Promise.all(wordCountsPromises)).map((promise) => promise.data);
      const occurrences = flattenDeep(lines.map((line, wordIndex) => map(line, (messages, sender) => (messages.map((message: [string, string]) => ({
        content: message[1],
        datetime: new Date(message[0]),
        sender, 
        phrase: words[wordIndex],
        score: 1
      }))))));
      let participents = Object.keys(scores);
      const res = {
        owner: [participents[0]],
        chatName: [participents[1]],
        score: scores[participents[0]] + scores[participents[1]],
        occurrences
      };
      setChatsState([res as any]);
      setLoading(false);
    })();   
  }, []);

  return (
    <ChatsContext.Provider value={chatsState}>
      <div className="App">
        {!loading && <RouterProvider router={router} />}
      </div>
    </ChatsContext.Provider>
  );
}

export default App;
