import React, { useState } from "react";
import XOsX from "../assets/XOsX.gif"; // Adjust path accordingly
import yand from '../assets/Yand.png';

interface NavbarProps {
    className ?: string;
    handleSelectedMeem: () => void;
}


const Navbar: React.FC<NavbarProps> = ({className ,handleSelectedMeem}) => {
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    const toggleMenu = () => {
        setIsMenuOpen(!isMenuOpen);
    };

    return (
        <header className={`flex  py-6 px-4 sm:px-10 bg-white font-[sans-serif] min-h-[65px] tracking-wide relative z-50 ${className}`}>
            <div className="flex flex-wrap items-center gap-4 max-w-screen-xl mx-auto w-full">
                <a className="max-sm:hidden">
                    <img src={XOsX} alt="XOsX" className="w-8"  onClick={handleSelectedMeem}/>
                </a>

                <div className="flex items-center">
                    <header className="text-2xl font-bold text-gray-800 hover:text-blue-600 transition-colors duration-300">
                       <a href="/">QuackBot</a> : <span className="text-yellow-500">The YC Duck</span>
                    </header>
                </div>
                

                </div>
                <div className="flex gap-4 ml-auto">
                    <div className="flex max-w-xs w-full bg-gray-100 px-4 py-2 rounded outline outline-transparent focus-within:border-blue-600 focus-within:bg-transparent transition-all">
                        <img src={yand} alt="tcombat logo" className="w-12 h-10" />
                    </div>
                    <button onClick={toggleMenu} className="lg:hidden">
                        <svg className="w-7 h-7" fill="#000" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                            <path fillRule="evenodd" d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
                        </svg>
                    </button>
                </div>

        </header>
    );
};
export default Navbar;
