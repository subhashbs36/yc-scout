import React, { useState } from 'react';
import { Card } from "@/components/ui/card";

const companies = ["[24]7.AI", "100 Thieves", "23andMe", "Sequoia", "Netflix"];

const App: React.FC = () => {
  const [selectedCompany, setSelectedCompany] = useState<string>("What can I help with?");
  const [searchTerm, setSearchTerm] = useState<string>("");
  const [chatMessage, setChatMessage] = useState<string>("");
  const [chatMode, setChatMode] = useState<string>("General");

  const filteredCompanies = companies.filter((company) =>
    company.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleSendMessage = () => {
    if (chatMessage.trim()) {
      console.log(Message sent: ${chatMessage});
      setChatMessage("");
    }
  };

  const handleCompanySelect = (company: string) => {
    setSelectedCompany(company);
    setChatMode("Specific");
  };

  const switchToGeneral = () => {
    setSelectedCompany("What can I help with?");
    setChatMode("General");
  };

  return (
    <div className="flex h-screen">
      {/* Left Sidebar */}
      <aside className="w-3/4 bg-[#f8f5f0] p-8 border-r border-gray-300 overflow-y-auto">
        <div className="mb-10">
          <h1 className="text-5xl font-bold tracking-widest text-black mb-4">OUR COMPANIES</h1>
          <button className="text-sm text-gray-600 mb-4">FILTERS &gt;</button>
          <p className="text-sm text-gray-500 uppercase tracking-widest mb-6">Spotlights</p>
          <input
            type="text"
            placeholder="Search Companies..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:ring-green-300"
          />
        </div>
        <table className="w-full text-left">
          <thead>
            <tr>
              <th className="text-sm text-gray-600 font-medium uppercase border-b border-gray-300 pb-2">Company Name</th>
            </tr>
          </thead>
          <tbody>
            {filteredCompanies.map((company) => (
              <tr key={company}>
                <td
                  className="text-lg text-black font-medium py-4 cursor-pointer hover:text-green-700"
                  onClick={() => handleCompanySelect(company)}
                >
                  {company}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </aside>

      {/* Main Chat Interface */}
      <main className="w-1/4 bg-black text-white flex flex-col p-6 relative">
        <div className="flex justify-between items-center mb-4">
          <select
            value={chatMode}
            onChange={(e) => {
              if (e.target.value === "General") {
                switchToGeneral();
              } else {
                setChatMode("Specific");
              }
            }}
            className="bg-gray-800 text-white py-2 px-4 rounded-md focus:outline-none focus:ring focus:ring-green-500"
          >
            <option value="General">General</option>
            <option value="Specific">Specific</option>
          </select>
          <div className="absolute top-6 right-6 bg-green-600 text-white px-2 py-1 rounded-md text-sm">
            {chatMode} Chat
          </div>
        </div>
        <div className="flex-grow flex items-center justify-center">
          <h2 className="text-gray-400 text-4xl font-semibold opacity-50">{selectedCompany}</h2>
        </div>
        <div className="flex items-center border-t border-gray-700 pt-4">
          <input
            type="text"
            placeholder="Ask anything..."
            value={chatMessage}
            onChange={(e) => setChatMessage(e.target.value)}
            className="flex-grow bg-gray-800 text-white p-2 rounded-md focus:outline-none focus:ring focus:ring-green-500"
          />
          <button
            onClick={handleSendMessage}
            className="ml-2 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
          >
            Send
          </button>
        </div>
      </main>
    </div>
  );
};

export default App;