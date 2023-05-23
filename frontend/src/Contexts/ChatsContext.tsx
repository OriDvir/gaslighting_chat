import React, { createContext } from "react";

interface IMessage {
    datetime: Date,
    content: string,
    sender: string
}

interface IOccurance {
    datetime: Date,
    messageIndex: number,
    score: number,
    phrase: string
}

interface IChatContext {
    chatName: string,
    owner: string,
    score: number,
    occurrences: IOccurance[],
    messages: IMessage[]
}

export const chatsMock = [
    {
      chatName: "Dor",
      owner: "Yael",
      score: 120,
      occurrences: [{datetime: new Date("Mar 22 2018 16:00"), messageIndex: 0, score: 10, phrase: "את/אתה"}, 
        {datetime: new Date("Mar 22 2019 18:00"), messageIndex: 0, score: 40, phrase: "גרמת/ה"}, 
        {datetime: new Date("Sep 23 2019 13:00"), messageIndex: 2, score: 10, phrase: "את/אתה"},
        {datetime: new Date("Feb 18 2020 13:00"), messageIndex: 3, score: 20, phrase: "כסף"},
        {datetime: new Date("Feb 18 2021 13:00"), messageIndex: 4, score: 20, phrase: "כסף"},
        {datetime: new Date("Feb 18 2022 13:00"), messageIndex: 5, score: 20, phrase: "כסף"}],
      messages: [{content: "את גרמת לכל זה לקרות", datetime: new Date("Mar 22 2018 16:00"), sender: "Dor"}, 
        {content: "על מה אתה מדבר?", datetime: new Date("Mar 22 2018 18:00"), sender: "Yael"}, 
        {content: "אתה הולך לפרט על זה?", datetime: new Date("Mar 23 2018 13:00"), sender: "Yael"},
        {content: "הולך", datetime: new Date("Feb 18 2022 13:00"), sender: "Dor"},
        {content: "הולך", datetime: new Date("Feb 18 2022 13:00"), sender: "Dor"},
        {content: "הולך", datetime: new Date("Feb 18 2022 13:00"), sender: "Dor"}]
    }, 
    {
      chatName: "Liza",
      owner: "Yael",
      score: 0,
      occurrences: [],
      messages: []
    }, 
    {
      chatName: "Michael",
      owner: "Yael",
      score: 2,
      occurrences: [],
      messages: []
    }
  ] 

export const ChatsContext = createContext<IChatContext[]>(chatsMock); 