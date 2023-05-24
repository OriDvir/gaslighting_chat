import React, { useContext } from "react"
import { ChatsContext } from "../Contexts/ChatsContext";
import { Chip, styled } from "@mui/material";
import "./ChatContent.css";
import { useParams } from "react-router-dom";

interface ChatContentProps {
}

const StyledChip = styled(Chip)(({ theme }) => ({
    fontSize: "large"
  }));

export const ChatContent: React.FC<ChatContentProps> = () => {
    let params = useParams();
    let chatIndex: number = -1;
    if (params.chatIndex) {
        chatIndex = Number.parseInt(params.chatIndex);
    }
    const chats = useContext(ChatsContext);
    const chat = chats[chatIndex];

    return <div className="chat-grid">
        {/*chat.messages.map(message => 
            <StyledChip label={message.content} className={message.sender === chat.owner ? "owner-message" : "side-b-message"}
            color={message.sender === chat.owner ? "primary" : "default"}/>
        )*/}
    </div>
}