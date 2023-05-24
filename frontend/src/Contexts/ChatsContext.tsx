import React, { createContext } from "react";

interface IOccurance {
    datetime: Date,
    score: number,
    phrase: string,
    content: string,
    sender: string
}

interface IChatContext {
    chatName: string,
    owner: string,
    score: number,
    occurrences: IOccurance[],
}

export const ChatsContext = createContext<IChatContext[]>([]); 