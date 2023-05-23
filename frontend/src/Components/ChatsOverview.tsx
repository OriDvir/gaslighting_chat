import React, { useContext, useState } from "react";
import Button from "@mui/material/Button";
import { TableContainer, TableHead, TableRow, TableCell, TableBody, Table, styled } from "@mui/material";
import "./ChatsOverview.css"
import { ChatsContext } from "../Contexts/ChatsContext";
import { useNavigate } from "react-router-dom";
import DateRangePicker from '@wojtekmaj/react-daterange-picker';
import 'react-calendar/dist/Calendar.css';

const StyledTableRow = styled(TableRow)(({ theme }) => ({
    '&:nth-of-type(odd)': {
      backgroundColor: theme.palette.action.hover,
    },
    // hide last border
    '&:last-child td, &:last-child th': {
      border: 0,
    },
  }));

export const ChatsOverview : React.FC = () => {
    const navigate = useNavigate();
    const chats = useContext(ChatsContext);
    const [dateRange, onDateRangeChange] = useState<[Date, Date]>([new Date(), new Date()]);

    function onChange(value: any) {
        onDateRangeChange(value);
    }

    return <div>
        <header className="page-title">
            Chats Score
        </header>
        <div className="date-container">
            <DateRangePicker onChange={onChange} value={dateRange} clearIcon={null} maxDate={new Date()} closeCalendar={true}
            shouldCloseCalendar={() => true}/>
        </div>
        <TableContainer>
            <Table>
                <TableHead>
                    <TableRow>
                        <TableCell> Chat </TableCell>
                        <TableCell> Score </TableCell>
                        <TableCell size="small" align="left"/>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {chats.map((chat, index) =>
                        <StyledTableRow key={chat.chatName}> 
                            <TableCell>
                                {`${chat.chatName}-${chat.owner}`}
                            </TableCell>
                            <TableCell>
                                {chat.score}
                            </TableCell>
                            <TableCell size="small" align="left">
                                <Button variant="contained" onClick={() => navigate(`/chat/${index}`)}>
                                    details
                                </Button>
                            </TableCell>
                        </StyledTableRow>
                    )}
                </TableBody>
            </Table>
        </TableContainer>
    </div>;
}