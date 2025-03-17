import React from "react";

interface Result {
    index: number;
    score: number;
    text: string;
    ycombinator: string;
}

interface IndexDataProps {
    results: Result[];
}

const IndexData: React.FC<IndexDataProps> = ({ results }) => {
    return (
        <div className="flex flex-col h-screen w-1/4 border-2 sticky top-0 bg-white">
            {/* Fixed Header */}
            <div className="font-bold text-xl text-black bg-gray-100 w-full text-center py-2 border-b border-gray-300 sticky top-0 z-10">
                🔍 Index Data
            </div>

            {/* Scrollable Content */}
            <div className="flex-1 overflow-y-auto">
                {results && results.length > 0 ? (
                    results.map((result) => (
                        <div 
                            key={result.index} 
                            className="p-4 border-b border-gray-200 w-full text-left transition-all duration-300 hover:bg-gray-100 rounded-md"
                        >
                            {/* Index & Score */}
                            <div className="text-gray-600 text-sm font-medium">
                                Index: <span className="text-black font-bold">{result.index}</span> |  
                                Score: <span className="text-green-600 font-bold">{result.score.toFixed(4)}</span>
                            </div>

                            {/* YCombinator Link as Heading (No Overlay) */}
                            <a 
                                href={result.ycombinator} 
                                target="_blank" 
                                rel="noopener noreferrer" 
                                className="block text-lg font-semibold text-blue-600 hover:underline mt-1 break-words"
                            >
                                {result.ycombinator} 
                            </a>

                            {/* Truncated Text */}
                            <p className="text-gray-700 text-sm mt-2 line-clamp-2">
                                {result.text.length > 100 ? result.text.substring(0, 100) + "..." : result.text}
                            </p>
                        </div>
                    ))
                ) : (
                    <p className="text-gray-500 text-center py-4">No data available</p>
                )}
            </div>
        </div>
    );
};

export default IndexData;
