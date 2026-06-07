import { useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../hooks/AuthContext";

function SearchContainer({ onSearch }) {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState("Rent");
  const [city, setCity] = useState("Chennai");
  const [propertyType, setPropertyType] = useState("Apartment");
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
      {/* Search Bar */}
      <div className="flex flex-col md:flex-row mt-6 shadow-md rounded overflow-hidden border border-gray-200">
        <select 
          value={city}
          onChange={(e) => setCity(e.target.value)}
          className="flex-1 px-4 py-3 outline-none text-gray-700 bg-white"
        >
          <option value="">All Cities</option>
          <option value="Chennai">Chennai</option>
          <option value="Bangalore">Bangalore</option>
          <option value="Mumbai">Mumbai</option>
          <option value="Delhi">Delhi</option>
          <option value="Hyderabad">Hyderabad</option>
          <option value="Pune">Pune</option>
        </select>
        
        <button 
          onClick={handleSearch}
          className="bg-brandRed text-white px-8 py-3 font-medium hover:bg-red-600 transition flex items-center gap-2 cursor-pointer"
        >
          🔍 Search
        </button>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap items-center gap-6 mt-6 p-4 border border-gray-200 rounded shadow-sm bg-white">
        {["Apartment", "House", "Villa"].map((type) => (
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
      
    </div>
  );
}

export default SearchContainer;
