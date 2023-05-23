import React, { useContext, useMemo } from "react";
import { LineChart, XAxis, YAxis, Line, Tooltip, Legend, BarChart, Bar, Cell, ResponsiveContainer } from 'recharts';
import { ChatsContext } from "../Contexts/ChatsContext";
import moment from "moment";
import {groupBy, map} from "lodash";
import "./ChatDrill.css";
import List from "@mui/material/List";
import ListItemButton from "@mui/material/ListItemButton";
import { useParams } from "react-router-dom";

interface ChatDrillProps {
}

export const ChatDrill: React.FC<ChatDrillProps> = () => {
    let params = useParams();
    let chatIndex: number = -1;
    if (params.chatIndex) {
        chatIndex = Number.parseInt(params.chatIndex);
    }
    const chats = useContext(ChatsContext);
    const chat = chats[chatIndex];
    const sideB = chat.chatName;
    let minData = chat.messages[0] ? chat.messages[0].datetime.toLocaleString() : (new Date()).toLocaleDateString();
    let maxDate = chat.messages[chat.messages.length - 1] ? chat.messages[chat.messages.length - 1].datetime.toLocaleString() : (new Date()).toLocaleDateString();
    const parsedLineData = useMemo(() =>  chat.occurrences.map((occurance) => ({
            datetime: occurance.datetime.valueOf(),
            ...(chat.messages[occurance.messageIndex].sender === chat.chatName ? {[sideB]: occurance.score, "Yael": 0} : {"Yael": occurance.score, [sideB]: 0})
        })), [chat]);
    const parsedBarData = useMemo(() => {
        const groupedBySender = groupBy(chat.occurrences, (occurance) => chat.messages[occurance.messageIndex].sender);
        return map(groupedBySender, (group, sender) => ({sender, score: group.reduce((scoreSum, occurance) => scoreSum + occurance.score, 0)}));
    }, [chat]);
    const commonOccurences = groupBy(chat.occurrences, "phrase");
    const commonOccurencesParsed = map(commonOccurences, (occurances, phrase) => ({phrase,  occurances}));
    return <>
        <header>
            {`${chat.chatName}-${chat.owner}`}
        </header>
        <div>
            {minData} - {maxDate}
        </div>
        <div className="chat-drill-grid">
            <ResponsiveContainer width="50%" height={240} className="chat-drill-line-chart">
                <LineChart data={parsedLineData} width={560} height={190}>
                    <XAxis dataKey="datetime" type = 'number' tickFormatter = {(unixTime) => moment(unixTime).format("DD/MM/YYYY hh:mm")}
                        domain = {['auto', 'auto']}
                        scale="time" hide padding={{ left: 30, right: 30 }}/>
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="Yael" stroke="#56a3a6" connectNulls strokeWidth={3}/>
                    <Line type="monotone" dataKey={sideB} stroke="#e3b505" connectNulls strokeWidth={3}/>
                </LineChart>
            </ResponsiveContainer>
            <ResponsiveContainer width="50%" height={240} className="bar-drill-line-chart">
                <BarChart data={parsedBarData} width={560} height={190}>
                    <YAxis />
                    <XAxis dataKey="sender" />
                    <Bar dataKey={"score"} fill="#e3b505">
                        <Cell key={`Yael`} fill={"#e3b505"} />
                        <Cell key={sideB} fill={"#56a3a6"} />
                    </Bar>
                </BarChart>
            </ResponsiveContainer>
            <div className="commonOccurences">
                <List>
                    {commonOccurencesParsed.map((occuranceGroup) => {
                        return <ListItemButton></ListItemButton>
                    })}
                </List>
            </div>
        </div>
    </>
}