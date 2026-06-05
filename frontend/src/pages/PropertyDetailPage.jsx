import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import Header from "../components/Header";
import { getPropertyById, applyForProperty } from "../services/api";
import { useAuth } from "../hooks/AuthContext";

function PropertyDetailPage() {
  const { id } = useParams();
  const { user } = useAuth();
  const [property, setProperty] = useState(null);
  const [loading, setLoading] = useState(true);
  const [applying, setApplying] = useState(false);
  const [applyMessage, setApplyMessage] = useState("");
  const [applicationStatus, setApplicationStatus] = useState(null); // 'success' or 'error'

  useEffect(() => {
    const fetchProp = async () => {
      try {
        const data = await getPropertyById(id);
        setProperty(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchProp();
  }, [id]);

  const handleApply = async (e) => {
    e.preventDefault();
    if (!user) {
      alert("Please log in to apply");
      return;
    }
    setApplying(true);
    try {
      await applyForProperty({ property_id: id, message: applyMessage });
      setApplicationStatus('success');
    } catch (err) {
      setApplicationStatus('error');
    } finally {
      setApplying(false);
    }
  };

  if (loading) return <div className="p-12 text-center text-gray-500">Loading Property...</div>;
  if (!property) return <div className="p-12 text-center text-red-500">Property not found.</div>;

  return (
    <div className="min-h-screen bg-gray-50 font-sans">
      <Header />
      <main className="max-w-5xl mx-auto px-4 py-12">
        <Link to="/properties" className="text-brandRed hover:underline mb-6 inline-block">← Back to Search</Link>
        
        <div className="bg-white rounded-xl shadow-md overflow-hidden border border-gray-200">
          <div className="h-64 bg-gray-200 flex items-center justify-center">
            {property.images && property.images.length > 0 ? (
               <img src={`http://localhost:8000${property.images[0]}`} className="w-full h-full object-cover" alt="Property" />
            ) : (
               <span className="text-gray-400">No Image Provided</span>
            )}
          </div>
          
          <div className="p-8 flex flex-col md:flex-row gap-8">
            <div className="flex-1">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">{property.title}</h1>
              <p className="text-gray-600 mb-6 flex items-center gap-2">📍 {property.city} | {property.property_type}</p>
              
              <div className="bg-gray-50 p-4 rounded-lg mb-6 border border-gray-100 flex gap-8">
                <div>
                  <p className="text-sm text-gray-500 uppercase font-semibold">Rent</p>
                  <p className="text-2xl font-bold text-gray-900">₹{property.rent}</p>
                </div>
                {property.deposit && (
                  <div>
                    <p className="text-sm text-gray-500 uppercase font-semibold">Deposit</p>
                    <p className="text-2xl font-bold text-gray-900">₹{property.deposit}</p>
                  </div>
                )}
              </div>

              <div className="prose text-gray-700">
                <h3 className="font-semibold text-lg border-b pb-2 mb-4">Description</h3>
                <p>{property.description || "No detailed description provided for this property."}</p>
                
                {property.amenities && property.amenities.length > 0 && (
                  <>
                    <h3 className="font-semibold text-lg border-b pb-2 mb-4 mt-6">Amenities</h3>
                    <ul className="list-disc pl-5">
                      {property.amenities.map((amenity, i) => <li key={i}>{amenity}</li>)}
                    </ul>
                  </>
                )}
              </div>
            </div>

            <div className="w-full md:w-1/3">
              <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm sticky top-6">
                <h3 className="text-xl font-bold text-gray-900 mb-4">Interested?</h3>
                
                {applicationStatus === 'success' ? (
                  <div className="bg-green-50 text-green-700 p-4 rounded border border-green-200">
                    Application submitted successfully! The owner will review it soon.
                  </div>
                ) : (
                  <form onSubmit={handleApply} className="flex flex-col gap-4">
                    <textarea 
                      required
                      placeholder="Why are you a good fit? (Employment, references...)" 
                      className="w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-black min-h-[120px]"
                      value={applyMessage}
                      onChange={(e) => setApplyMessage(e.target.value)}
                    />
                    <button 
                      type="submit" 
                      disabled={applying || !property.available}
                      className="bg-black text-white px-4 py-3 rounded font-medium hover:bg-gray-800 transition disabled:bg-gray-400"
                    >
                      {applying ? "Submitting..." : property.available ? "Submit Application" : "Currently Unavailable"}
                    </button>
                    {!user && <p className="text-xs text-center text-red-500">You must be logged in to apply.</p>}
                  </form>
                )}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default PropertyDetailPage;
