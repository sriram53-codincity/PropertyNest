import { useState } from "react";

function SearchContainer({ onSearch }) {
  const [activeTab, setActiveTab] = useState("Rent");
  const [city, setCity] = useState("Chennai");
  const [propertyType, setPropertyType] = useState("Full House");
  const [bhk, setBhk] = useState("");

  const handleSearch = () => {
    if (onSearch) {
      const params = { city, property_type: propertyType };
      if (bhk) params.bhk = bhk;
      onSearch(params);
    }
  };
  
  return (
    <div className="max-w-4xl mx-auto px-4 mt-8">
      {/* Tabs */}
      <div className="flex justify-center border-b border-gray-200">
        {["Buy", "Rent", "Commercial"].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-8 py-3 text-lg transition-colors ${
              activeTab === tab
                ? "text-brandRed border-b-2 border-brandRed font-medium"
                : "text-gray-500 hover:text-gray-700"
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Search Bar */}
      <div className="flex flex-col md:flex-row mt-6 shadow-md rounded overflow-hidden border border-gray-200">
        <div className="bg-gray-100 px-4 py-3 flex items-center justify-between min-w-[150px] border-r border-gray-200 cursor-pointer">
          <select 
            value={city} 
            onChange={(e) => setCity(e.target.value)}
            className="bg-transparent outline-none text-gray-700 w-full appearance-none cursor-pointer"
          >
            <option value="Chennai">Chennai</option>
            <option value="Bangalore">Bangalore</option>
            <option value="Mumbai">Mumbai</option>
            <option value="Delhi">Delhi</option>
          </select>
          <span className="text-gray-400 text-xs pointer-events-none">▼</span>
        </div>
        
        <input 
          type="text" 
          placeholder="Search upto 3 localities, societies or landmarks"
          className="flex-1 px-4 py-3 outline-none text-gray-700"
        />
        
        <button 
          onClick={handleSearch}
          className="bg-brandRed text-white px-8 py-3 font-medium hover:bg-red-600 transition flex items-center gap-2 cursor-pointer"
        >
          🔍 Search
        </button>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap items-center gap-6 mt-6 p-4 border border-gray-200 rounded shadow-sm bg-white">
        {["Full House", "PG/Hostel", "Flatmates"].map((type) => (
          <label key={type} className="flex items-center gap-2 cursor-pointer">
            <input 
              type="radio" 
              name="property_type" 
              className="accent-teal-600 w-4 h-4" 
              checked={propertyType === type}
              onChange={() => setPropertyType(type)}
            />
            <span className="text-gray-600 text-sm">{type}</span>
          </label>
        ))}
        
        <div className="ml-auto flex items-center gap-2">
          <input 
            type="number" 
            placeholder="BHK (e.g. 2)" 
            value={bhk}
            onChange={(e) => setBhk(e.target.value)}
            className="border border-gray-200 rounded px-3 py-1.5 text-sm outline-none w-32 focus:border-brandRed focus:ring-1 focus:ring-brandRed"
          />
        </div>
      </div>
      
      {/* Owner CTA */}
      <div className="mt-16 text-center">
        <div className="flex items-center justify-center gap-4 mb-6">
          <div className="h-px bg-gray-300 flex-1 max-w-[100px]"></div>
          <span className="text-gray-600">Are you a Property Owner?</span>
          <div className="h-px bg-gray-300 flex-1 max-w-[100px]"></div>
        </div>
        <button className="bg-brandTeal text-white px-6 py-2.5 rounded font-medium hover:bg-teal-600 transition shadow">
          Post Free Property Ad
        </button>
      </div>
    </div>
  );
}

export default SearchContainer;
