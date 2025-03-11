import React from "react";

interface RawJsonModalProps {
    content: string;
    onClose: () => void;
}

const RawJsonModal: React.FC<RawJsonModalProps> = ({ content, onClose }) => {
    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
            <div className="bg-white p-4 rounded-lg max-w-lg w-full">
                <h2 className="text-xl font-bold mb-4">Raw JSON</h2>
                <pre className="bg-gray-100 p-2 rounded-lg overflow-auto max-h-96">
                    {content}
                </pre>
                <button
                    onClick={onClose}
                    className="mt-4 bg-blue-500 text-white px-4 py-2 rounded-lg"
                >
                    Close
                </button>
            </div>
        </div>
    );
};

export default RawJsonModal;
