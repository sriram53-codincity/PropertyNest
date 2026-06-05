import { useState, useEffect } from "react";
import Header from "../components/Header";
import HeroSection from "../components/HeroSection";
import SearchContainer from "../components/SearchContainer";
import PropertyList from "../components/PropertyList";
import { getProperties } from "../services/api";

function HomePage() {
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchProperties = async (params = {}) => {
    setLoading(true);
    setError(null);
    try {
      // For testing based on typical FastAPI pagination/response format:
      // if it returns a list directly or a paginated object
      const data = await getProperties(params);
      
      // If your API returns data inside an 'items' or 'data' field, adjust this
      const items = Array.isArray(data) ? data : data.items || [];
      setProperties(items);
    } catch (err) {
      setError("Failed to load properties. Ensure backend is running.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Initial fetch
    fetchProperties();
  }, []);

  const handleSearch = (searchParams) => {
    fetchProperties(searchParams);
  };

  return (
    <div className="min-h-screen bg-gray-50 font-sans">
      <Header />
      <main>
        <HeroSection />
        <SearchContainer onSearch={handleSearch} />
        <div className="bg-gray-50 py-8">
          <PropertyList properties={properties} loading={loading} error={error} />
        </div>
      </main>
      
      {/* Bottom Floating Chat Button */}
      <div className="fixed bottom-6 right-6">
        <button className="bg-brandRed text-white p-4 rounded-full shadow-lg hover:bg-red-600 transition">
          💬
        </button>
      </div>
    </div>
  );
}

export default HomePage;
