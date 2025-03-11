import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import tenorGif from "../assets/tenor.gif"; // Adjust path accordingly
import axios from "axios";

interface ChatbarProps {
    company?: string | null;
}

interface Message {
    sender: "user" | "bot";
    text: string;
}

const Chatbar: React.FC<ChatbarProps> = ({ company }) => {
    const [currentSession, setCurrentSession] = useState<string>("General");
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState<string>("");
    const chatContainerRef = useRef<HTMLDivElement>(null);
    const [phase , setPhase] = useState<string>('phase1');
    const navigate = useNavigate();

    useEffect(() => {   
        if (company) {
            setCurrentSession(company);
        } else {
            setCurrentSession("General");
        }
        setMessages([]); // Clear chat on session switch
    }, [company]);

    useEffect(() => {
        // Auto-scroll to the latest message
        if (chatContainerRef.current) {
            chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
        }
    }, [messages]);

    const handleGeneralButton = () => {
        setCurrentSession("General");
        setMessages([]);
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === "Enter") {
            handleSendMessage();
        }
    };

    const getresponse = async (currentSession:string, userMessage:string) => {   
        console.log(userMessage)
        try {
            console.log(`http://127.0.0.1:8000/`)
            const response = await axios.get(`http://127.0.0.1:8000/response/${phase}/${currentSession}/${userMessage}`)
            console.log(response)
            return response
        } catch(error) {
            console.error("API error:", error)
            return error // Return the actual error object instead of a string
        }
    }

    const handleSendMessage = () => {
        if (input.trim() === "") return;

        // User message
        const userMessage: Message = { sender: "user", text: input };
        setMessages((prev) => [...prev, userMessage]);
        setInput("");

        // actual bot response 
        const bot_response = getresponse(currentSession, input);
        bot_response.then(response => {
            if (response && response.data) {
                const botMessage: Message = {
                    sender: "bot",
                    text: response.data,
                    raw_json: JSON.stringify(response),
                };
                setMessages((prev) => [...prev, botMessage]);
            } else {
                const botMessage: Message = {
                    sender: "bot",
                    text: "Error Fetching chat",
                    raw_json: JSON.stringify(response),
                };
                setMessages((prev) => [...prev, botMessage]);
            }
        });
    };

    const handleViewRawJson = (rawJson: string) => {
        // Store the JSON in localStorage to access it from the new tab
        localStorage.setItem('rawJsonData', rawJson);
        
        // Open the view-json route in a new tab
        window.open('/view-json', '_blank');
    };

    useEffect(() => {
        const firstMessage = `Quack! how can i help u with  ${currentSession}.`;
        const botMessage: Message = { sender: "bot", text: firstMessage };
        setMessages([botMessage]);
    }, [currentSession]);

    return (
        <div className="flex flex-col h-screen w-full border-l sticky top-0 ">
            {/* Background GIF */}
            <div className="absolute inset-0 z-0 overflow-hidden flex justify-center items-center">
                <img src={tenorGif} alt="Chat Background GIF" className="w-full h-full object-cover opacity-30" />

            </div>
            {/* Chat Content (Overlay on GIF) */}
            <div className="relative z-10 flex flex-col h-full">
                {/* Chat Header (Fixed) */}
                <div className="p-4  flex justify-between items-center ">
                    <h1 className="text-xl font-bold bg-gray-400 text-white border-2 rounded-full px-4 py-2">{currentSession}</h1>

                    <div className="flex gap-4 border-black">
                        <button 
                        className={`p-2 text-xl font-bold ${phase === 'phase1' ? '  text-black  bg-inherit border-2 rounded-2xl' : ''} `} 
                        onClick = {() => setPhase('phase1')}>PyElastic</button>
                        <button 
                        className={`p-2 text-xl font-bold ${phase === 'phase2' ? '  text-black bg-inherit border-2 rounded-2xl' : ''} `} 
                        onClick = {() => setPhase('phase2')}>BERT </button>
                    </div>

                    <button
                        className="text-xl font-bold bg-gray-400 bg-opacity-50 text-white border-2 border-white rounded-full px-4 py-2 backdrop-filter backdrop-blur-lg"
                        onClick={handleGeneralButton}
                    >
                        Reset
                    </button>
                </div>

                {/* Chat Messages (Scrollable) */}
                <div
                    ref={chatContainerRef}
                    className="flex-1 overflow-y-auto p-4 space-y-4"
                >
                    {messages.map((msg, index) => (
                        <div
                            key={index}
                            className={`p-2 rounded-lg w-fit max-w-[70%] transition-all duration-500 ${msg.sender === "user"? "bg-gradient-to-r from-cyan-500 to-blue-500 text-black ml-auto": "bg-gradient-to-r from-cyan-500 to-blue-500 text-black"}`}>
                            {msg.text}
                            <br />
                            {msg.raw_json && (
                                <button 
                                    onClick={() => handleViewRawJson(msg.raw_json)}
                                    className="text-yellow-800 underline ml-2"
                                >
                                    View Raw JSON
                                </button>
                            )}
                        </div>
                    ))}
                </div>

                {/* Chat Input (Fixed at Bottom) */}
                <div className=" p-4 sticky bottom-0">
                    <div className="flex gap-2">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Type your message..."
                            className="flex-1 p-2 border rounded-lg focus:outline-none"
                            onKeyDown={handleKeyDown}
                        />

                        <button
                            onClick={handleSendMessage}
                            className="bg-inherit text-black px-4 py-2 rounded-lg hover:bg-black hover:text-white transition"
                        >
                            Send
                        </button>
                    </div>
                </div>

            </div>
        </div>
    );
};

export default Chatbar;
