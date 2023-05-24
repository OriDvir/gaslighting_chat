import React, { useContext, useMemo } from "react";
import { LineChart, XAxis, YAxis, Line, Tooltip, Legend, BarChart, Bar, Cell, ResponsiveContainer } from 'recharts';
import { ChatsContext } from "../Contexts/ChatsContext";
import moment from "moment";
import {chunk, groupBy, map, partition} from "lodash";
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
    let minData = chat.occurrences[0] ? chat.occurrences[0].datetime.toLocaleString() : (new Date()).toLocaleDateString();
    let maxDate = chat.occurrences[chat.occurrences.length - 1] ? chat.occurrences[chat.occurrences.length - 1].datetime.toLocaleString() : (new Date()).toLocaleDateString();
    const parsedLineData = useMemo(() => {
        //const [ownerOccurrences, sideBOccurrences] = partition(chat.occurrences, (occurance) => occurance.sender === chat.owner);
        //const compactedOwnerOccurrences = chunk(ownerOccurrences, 200).map(chunked => {
        //    return {...chunked[0] ,score: chunked.reduce((sum, occurance: any) => sum + occurance.score, 0)}
        //});
        //const compactedSideBOccurrences = chunk(sideBOccurrences, 200).map(chunked => {
        //    return {...chunked[0] ,score: chunked.reduce((sum, occurance: any) => sum + occurance.score, 0)}
        //});
        const compactedOccurrences = chat.occurrences;//compactedOwnerOccurrences.concat(compactedSideBOccurrences);
        return compactedOccurrences.map((occurance) => ({
            datetime: occurance.datetime.valueOf(),
            ...(occurance.sender === chat.chatName ? {[sideB]: occurance.score, [chat.owner]: 0} : {[chat.owner]: occurance.score, [sideB]: 0})
        }))}, [chat]);
    const parsedBarData = useMemo(() => {
        const groupedBySender = groupBy(chat.occurrences, (occurance) => occurance.sender);
        return map(groupedBySender, (group, sender) => ({sender, score: group.reduce((scoreSum, occurance) => scoreSum + occurance.score, 0)}));
    }, [chat]);
    const commonOccurences = groupBy(chat.occurrences, "phrase");
    const commonOccurencesParsed = map(commonOccurences, (occurances, phrase) => ({phrase,  occurances}));
    return <>
        <header className="page-title-drill">
            {`${chat.chatName}-${chat.owner}`}
        </header>
        <div>
            {minData} - {maxDate}
        </div>
        <div className="chat-drill-grid">
            <ResponsiveContainer width="100%" height={240} className="chat-drill-line-chart">
                <LineChart data={parsedLineData} width={560} height={190}>
                    <XAxis dataKey="datetime" type = 'number' tickFormatter = {(unixTime) => moment(unixTime).format("DD/MM/YYYY hh:mm")}
                        domain = {['auto', 'auto']}
                        scale="time" hide padding={{ left: 30, right: 30 }}/>
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey={chat.owner} stroke="#56a3a6" connectNulls strokeWidth={3}/>
                    <Line type="monotone" dataKey={sideB} stroke="#e3b505" connectNulls strokeWidth={3}/>
                </LineChart>
            </ResponsiveContainer>
            <ResponsiveContainer width="100%" height={240} className="bar-drill-line-chart">
                <BarChart data={parsedBarData} width={560} height={190}>
                    <YAxis />
                    <XAxis dataKey="sender" />
                    <Bar dataKey={"score"} fill="#e3b505">
                        <Cell key={chat.owner} fill={"#e3b505"} />
                        <Cell key={sideB} fill={"#56a3a6"} />
                    </Bar>
                </BarChart>
            </ResponsiveContainer>
            <div className="commonOccurences">
                <List>
                    {commonOccurencesParsed.map((occuranceGroup) => {
                        return <ListItemButton>{occuranceGroup.phrase}</ListItemButton>
                    })}
                </List>
            </div>
        </div>
    </>
}