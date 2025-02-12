import Navbar from "./components/navbar";
import React, { useState , useEffect } from "react";
import CompanyItem from "./components/CompanyItem";
import Chatbar from "./components/chatbar";
import anya2 from "./assets/anya2.png";
import fullface from "./assets/full_face.png";
import company from './assets/companies.json';

interface Company {
  company_id: number | null;
  company_name: string ;
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

const App: React.FC = () => {
  const [openIndex, setOpenIndex] = useState<number | null>(null);  
  const [selectedCompany , setSelectedCompany] = useState<string | null>(null);
  const [currentmeme , setCurrentmeme] = useState<string>(fullface);
  const [companies, setCompanies] = useState<Company[]>([]);

  const [currentPage, setCurrentPage] = useState(1);
  const companiesPerPage = 20; // Adjust as needed

  const tags = ['3d-printed-foods',
    '3d-printing',
    'advanced-materials',
    'advertising',
    'aerospace',
    'agriculture',
    'ai',
    'ai-assistant',
    'ai-enhanced-learning',
    'ai-powered-drug-discovery',
    'aiops',
    'air-taxis',
    'airlines',
    'airplanes',
    'alternative-battery-tech',
    'analytics',
    'anti-aging',
    'api',
    'apis',
    'ar',
    'art-trading-platforms',
    'artificial-intelligence',
    'assistive-tech',
    'augmented-reality',
    'vr-health',
    'warehouse-management-tech',
    'weather',
    "women's-health",
    'workflow-automation']

  const [searchQuery, setSearchQuery] = useState("");
  const [selectedStatus, setSelectedStatus] = useState<string | null>(null);
  const [selectedLocation, setSelectedLocation] = useState<string | null>(null);
  const [selectedBatch, setSelectedBatch] = useState<string | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  const filteredCompanies = companies.filter((company) => {
    const matchesSearch = company.company_name.toLowerCase().includes(searchQuery);
    const matchesStatus = selectedStatus ? company.status === selectedStatus : true;
    const matchesLocation = selectedLocation ? company.location?.toLowerCase().includes(selectedLocation.toLowerCase()) : true;
    const matchesBatch = selectedBatch ? company.batch === selectedBatch : true;
    const matchesCategory = selectedCategory ? company.tags.includes(selectedCategory) : true;
    return matchesSearch && matchesStatus && matchesLocation && matchesBatch && matchesCategory;
  });

  const indexOfLastCompany = currentPage * companiesPerPage;
  const indexOfFirstCompany = indexOfLastCompany - companiesPerPage;
  const currentCompanies = filteredCompanies.slice(indexOfFirstCompany, indexOfLastCompany);

  const handleSelectedMeem = () => {
    setCurrentmeme(anya2);
  }

  const handleSelectedCompany = (companyName: string) => {
    setSelectedCompany(companyName);
  }

  const handleToggle = (index: number) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(event.target.value.toLowerCase());
  };
  
  const handleStatusChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedStatus(event.target.value || null);
  };
  
  const handleLocationChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedLocation(event.target.value || null);
  };

  const handleBatchChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    // Add your logic for handling batch change here
    setSelectedBatch(event.target.value || null);
  };

  const handleCategoryChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    // Add your logic for handling category change here
    setSelectedCategory(event.target.value || null);
  };

  useEffect(() => {
    setCompanies(company as Company[]);
  }, []);

  return (
    <>
      <div className="flex flex-row">
        <div className="border-2 border-r-1 w-full h-full relative">
          <div id="navbar" className="sticky top-0 z-50 bg-white">
            <Navbar className="sticky top-0" handleSelectedMeem={handleSelectedMeem} />
            <hr className="ml-8 mr-8" />
          </div>

          <div className="absolute inset-0 z-0 mt-10  h-1/3 w-full items-center pointer-events-none"> 
            <img src={currentmeme} alt="anya2" className="w-fit h-fit opacity-30" />
          </div>

          <div id="companySection" className="text-7xl ml-90 text-center mt-10 font-normal tracking-wide">
            OUR <br /> COMPANIES
          </div>

          <div>
            <div className="p-4 m-6  text-l justify-between items-center">
              {/* Search Bar */}
              <input
                type="text"
                placeholder="Search Company"
                className="w-full p-3 font-bold text-xl m-2 focus:outline-none bg-gradient-to-r from-slate-100 to-slate-200 boder-2" 
                onChange={handleSearchChange}
              />

              {/* Status Filter */}
                <select className="m-1 p-1 text-sm font-bold border-1 ml-0 rounded" onChange={handleStatusChange}>
                <option value="">All Statuses</option>
                <option value="Active">Active</option>
                <option value="Inactive">Inactive</option>
                </select>

                {/* Location Filter */}
                <select className="m-1 p-1 text-sm font-bold border-1 ml-0 rounded tracking-wide" onChange={handleLocationChange}>
                  <option value="">All Locations</option>
                  <option value="Seattle, WA">Seattle, WA</option>
                  <option value="San Francisco">San Francisco</option>
                  <option value="Toronto, Canada">Toronto, Canada</option>
                  <option value="Huntington Beach, CA">Huntington Beach, CA</option>
                  <option value="New York">New York</option>
                  <option value="Amsterdam, Netherlands">Amsterdam, Netherlands</option>
                  <option value="Dublin, Ireland">Dublin, Ireland</option>
                  <option value="London, United Kingdom">London, United Kingdom</option>
                  <option value="Austin, TX">Austin, TX</option>
                  <option value="Oakland, CA">Oakland, CA</option>
                  <option value="Berlin, Germany">Berlin, Germany</option>
                  <option value="Paris, France">Paris, France</option>
                  <option value="Redmond, WA">Redmond, WA</option>
                  <option value="Gurugram, India">Gurugram, India</option>
                  <option value="Los Angeles, CA">Los Angeles, CA</option>
                  <option value="Washington, DC">Washington, DC</option>
                  <option value="Atlanta, GA">Atlanta, GA</option>
                  <option value="Mexico City, Mexico">Mexico City, Mexico</option>
                  <option value="Copenhagen, Denmark">Copenhagen, Denmark</option>
                  <option value="Miami, FL">Miami, FL</option>
                  <option value="Santa Barbara, CA">Santa Barbara, CA</option>
                  <option value="Ikeja, Nigeria">Ikeja, Nigeria</option>
                  <option value="Vienna, Austria">Vienna, Austria</option>
                  <option value="Lake Oswego, OR">Lake Oswego, OR</option>
                  <option value="Long Beach, CA">Long Beach, CA</option>
                  <option value="Nairobi, Kenya">Nairobi, Kenya</option>
                  <option value="Lagos, Nigeria">Lagos, Nigeria</option>
                  <option value="Oxford, United Kingdom">Oxford, United Kingdom</option>
                  <option value="Zug, Switzerland">Zug, Switzerland</option>
                  <option value="Santa Clara, CA">Santa Clara, CA</option>
                  <option value="Philadelphia, PA">Philadelphia, PA</option>
                  <option value="San Jose, CA">San Jose, CA</option>
                  <option value="Boston">Boston</option>
                  <option value="Bengaluru, India">Bengaluru, India</option>
                  <option value="Jakarta, Indonesia">Jakarta, Indonesia</option>
                  <option value="Bogotá, Colombia">Bogotá, Colombia</option>
                  <option value="Singapore, Singapore">Singapore, Singapore</option>
                  <option value="São Paulo, Brazil">São Paulo, Brazil</option>
                  <option value="Buenos Aires, Argentina">Buenos Aires, Argentina</option>
                  <option value="Madrid, Spain">Madrid, Spain</option>
                  <option value="Mexico City, Mexico">Mexico City, Mexico</option>
                  <option value="Berlin, Germany">Berlin, Germany</option>
                  <option value="Paris, France">Paris, France</option>
                  <option value="New York">New York</option>
                  <option value="San Francisco">San Francisco</option>
                  <option value="Toronto, Canada">Toronto, Canada</option>
                  <option value="London, United Kingdom">London, United Kingdom</option>
                  <option value="Austin, TX">Austin, TX</option>
                  <option value="Los Angeles, CA">Los Angeles, CA</option>
                  <option value="Washington, DC">Washington, DC</option>
                  <option value="Atlanta, GA">Atlanta, GA</option>
                  <option value="Mexico City, Mexico">Mexico City, Mexico</option>
                  <option value="Copenhagen, Denmark">Copenhagen, Denmark</option>
                  <option value="Miami, FL">Miami, FL</option>
                  <option value="Santa Barbara, CA">Santa Barbara, CA</option>
                  <option value="Ikeja, Nigeria">Ikeja, Nigeria</option>
                  <option value="Vienna, Austria">Vienna, Austria</option>
                  <option value="Lake Oswego, OR">Lake Oswego, OR</option>
                  <option value="Long Beach, CA">Long Beach, CA</option>
                  <option value="Nairobi, Kenya">Nairobi, Kenya</option>
                  <option value="Lagos, Nigeria">Lagos, Nigeria</option>
                  <option value="Oxford, United Kingdom">Oxford, United Kingdom</option>
                  <option value="Zug, Switzerland">Zug, Switzerland</option>
                  <option value="Santa Clara, CA">Santa Clara, CA</option>
                  <option value="Philadelphia, PA">Philadelphia, PA</option>
                  <option value="San Jose, CA">San Jose, CA</option>
                  <option value="Boston">Boston</option>
                  <option value="Bengaluru, India">Bengaluru, India</option>
                  <option value="Jakarta, Indonesia">Jakarta, Indonesia</option>
                  <option value="Bogotá, Colombia">Bogotá, Colombia</option>
                  <option value="Singapore, Singapore">Singapore, Singapore</option>
                  <option value="São Paulo, Brazil">São Paulo, Brazil</option>
                  <option value="Buenos Aires, Argentina">Buenos Aires, Argentina</option>
                  <option value="Madrid, Spain">Madrid, Spain</option>
                  <option value="Mexico City, Mexico">Mexico City, Mexico</option>
                  <option value="Berlin, Germany">Berlin, Germany</option>
                  <option value="Paris, France">Paris, France</option>
                </select>
                
                <select className="m-1 p-1 text-sm font-bold border-1 ml-0 rounded tracking-wide" onChange={handleBatchChange}>
                    <option value="">All Batch</option>
                    <option value="F24">F24</option>
                    <option value="IK12">IK12</option>
                    <option value="S05">S05</option>
                    <option value="S06">S06</option>
                    <option value="S07">S07</option>
                    <option value="S08">S08</option>
                    <option value="S09">S09</option>
                    <option value="S10">S10</option>
                    <option value="S11">S11</option>
                    <option value="S12">S12</option>
                    <option value="S13">S13</option>
                    <option value="S14">S14</option>
                    <option value="S15">S15</option>
                    <option value="S16">S16</option>
                    <option value="S17">S17</option>
                    <option value="S18">S18</option>
                    <option value="S19">S19</option>
                    <option value="S20">S20</option>
                    <option value="S21">S21</option>
                    <option value="S22">S22</option>
                    <option value="S23">S23</option>
                    <option value="W06">W06</option>
                    <option value="W07">W07</option>
                    <option value="W08">W08</option>
                    <option value="W09">W09</option>
                    <option value="W10">W10</option>
                    <option value="W11">W11</option>
                    <option value="W12">W12</option>
                    <option value="W13">W13</option>
                    <option value="W14">W14</option>
                    <option value="W15">W15</option>
                    <option value="W16">W16</option>
                    <option value="W17">W17</option>
                    <option value="W18">W18</option>
                    <option value="W19">W19</option>
                    <option value="W20">W20</option>
                    <option value="W21">W21</option>
                    <option value="W22">W22</option>
                    <option value="W23">W23</option>
                    <option value="W24">W24</option>
                    <option value="W25">W25</option>
                </select>
                <select className="m-1 p-1 text-sm font-bold border-1 ml-0 rounded tracking-wide" onChange={handleCategoryChange}>
                  <option value="">All Categories</option>
                    {tags.map((tag, index) => (
                    <option key={index} value={tag}>{tag}</option>
                    ))}
                </select>

                  <button 
                  onClick={() => {
                    setSearchQuery("");
                    setSelectedLocation(null);
                    setSelectedStatus(null);
                    setSelectedBatch(null);
                    setSelectedCategory(null);
                    
                  }}
                  className="m-1 p-1 text-sm font-bold border-1 ml-0 rounded tracking-wide"
                  >
                  Reset
                  </button>
              </div>


            <ul
              className="font-normal tracking-widest"
              onClick={() => {
                const navbar = document.getElementById("navbar");
                if (navbar) {
                  navbar.scrollIntoView({ behavior: "smooth", block: "start" });
                }
              }}                
            >
              {currentCompanies.map((company, index) => (
                <CompanyItem
                  key={index}
                  company={{
                    company_id: company.company_id,
                    company_name: company.company_name,
                    short_description: company.short_description,
                    long_description: company.long_description,
                    batch: company.batch,
                    status: company.status,
                    tags: company.tags,
                    location: company.location,
                    country: company.country,
                    year_founded: company.year_founded,
                    num_founders: company.num_founders,
                    founders_names: company.founders_names,
                    team_size: company.team_size,
                    website: company.website,
                    linkedin_url: company.linkedin_url,
                    cb_url: company.cb_url,
                    image_urls: company.image_urls,
                  }}
                  isOpen={openIndex === index}
                  onToggle={() => handleToggle(index)}
                  onClick={() => handleSelectedCompany(company.company_name)}
                />
              ))}
            </ul>
            <div className="flex justify-center mt-5">
              <button 
                disabled={currentPage === 1} 
                onClick={() => {
                  setCurrentPage(prev => prev - 1);
                  setOpenIndex(null);
                  window.scrollTo({ top: 0, behavior: "smooth" });
                }}
                className="mx-2 p-2 border rounded"
              >
                Previous
              </button>

              <span className="p-2">
                Page {currentPage} of {Math.ceil(companies.length / companiesPerPage)}
              </span>

              <button 
                disabled={indexOfLastCompany >= companies.length} 
                onClick={() => {
                  setCurrentPage(prev => prev + 1);
                  setOpenIndex(null);
                  window.scrollTo({ top: 0, behavior: "smooth" });
                }}
                className="mx-2 p-2 border rounded"
              >
                Next
              </button> 
            </div>
          </div>
        </div>
        
        {/* CHAT SECTION */}
        <Chatbar company={selectedCompany} />
      </div>
    </>
  );
}

export default App;
