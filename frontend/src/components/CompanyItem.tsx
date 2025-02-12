import React, { useState } from "react";
import LazyLoad from "react-lazy-load";
import linksvg from '../assets/link.svg'

interface CompanyItemProps {
    company: {
        company_id: number | null;
        company_name: string;
        short_description: string | null;
        long_description: string | null;
        batch: string | null;
        status: string | null;
        tags: string[];
        location: string | null;
        country: string | null;
        year_founded: number | null;
        num_founders: number | null;
        founders_names: string[];
        team_size: number;
        website: string | null;
        cb_url: string | null;
        linkedin_url: string | null;
        image_urls?: string[];
    };

    isOpen: boolean;
    onToggle: () => void;
    onClick: () => void;
}

const CompanyItem: React.FC<CompanyItemProps> = ({ company, isOpen, onToggle, onClick }) => {
    const [hovered, setHovered] = useState(false);

    return (
        <>
            <li
                className={`border-b w-full hover:bg-black ${hovered ? "text-white" : "text-black"} transition-all duration-500 ${isOpen ? "bg-black text-white" : ""}`}
                onMouseEnter={() => setHovered(true)}
                onMouseLeave={() => setHovered(false)}
                onClick={() => {
                    onToggle();
                    onClick();
                }}
            >
                <button className={`w-full h-full text-left px-4 py-3 text-2xl sm:text-3xl lg:text-4xl ${hovered ? "scale-95" : "scale-90"} transform transition-transform duration-300`}>
                    <div className="flex justify-between items-center">
                        <span className="truncate">{company.company_name}</span>
                        <span className={`transform transition-all duration-500 ${isOpen ? "rotate-180" : "rotate-0"}`}>
                            {isOpen ? "×" : "→"}
                        </span>
                    </div>
                </button>
            </li>

            {isOpen && (
                <div
                    className={`w-full max-w-3xl mx-auto p-5 bg-white rounded-lg shadow-md transition-transform transform border-2 overflow-hidden 
                    ${company.status?.toLowerCase() === "active" ? "border-green-500" : "border-red-500"}`}
                >
                    <div className="flex items-center mb-4">
                        <LazyLoad height={60} offset={100}>
                            <img
                                className="w-16 h-16 object-cover rounded-full"
                                src={company.image_urls?.[1] || ""}
                                alt="Company Logo"
                            />
                        </LazyLoad>
                        <div className="ml-4">
                            <h2 className="text-xl font-bold text-gray-800">{company.company_name}</h2>
                            <span className="text-sm uppercase tracking-wide text-gray-500">{company.status}</span>
                        </div>
                        <div className="ml-auto text-right">
                            {company.founders_names.length > 0 && (
                                <>
                                    <h3 className="text-sm font-semibold text-gray-700">Founders:</h3>
                                    <ul className="text-sm text-gray-600">
                                        {company.founders_names.map((founder, index) => (
                                            <li key={index}>{founder}</li>
                                        ))}
                                    </ul>
                                </>
                            )}
                        </div>
                    </div>

                    <p className="text-gray-700 text-sm sm:text-base break-words">{company.short_description || "No short description available."}</p>
                    <p className="text-gray-600 text-sm sm:text-base break-words">{company.long_description || "No long description available."}</p>

                    <div className="flex flex-wrap mt-3">
                        {company.website && (
                            <a href={company.website} target="_blank" rel="noopener noreferrer" className="mr-4 mb-2 text-blue-600 hover:underline">
                                Official Website <img src={linksvg} alt="link" className="inline-block w-4 h-4 ml-1" />
                            </a>
                        )}
                        {company.linkedin_url && (
                            <a href={company.linkedin_url} target="_blank" rel="noopener noreferrer" className="mr-4 mb-2 text-blue-600 hover:underline">
                                LinkedIn
                            </a>
                        )}
                        {company.tags.slice(0, 3).map((tag, index) => (
                            <span key={index} className="mr-2 mb-2 px-2 py-1 bg-gray-200 text-gray-700 text-xs font-semibold rounded">
                                {tag}
                            </span>
                        ))}
                    </div>

                    {company.location && (
                        <div className="mt-2 text-sm text-gray-500">
                            Location: {company.location}
                            {company.country ? `, ${company.country}` : ""}
                        </div>
                    )}
                </div>
            )}
        </>
    );
};

export default CompanyItem;
