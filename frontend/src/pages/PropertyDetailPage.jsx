import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import Header from "../components/Header";
import { getPropertyById, applyForProperty, uploadApplicationDocument } from "../services/api";
import { useAuth } from "../hooks/AuthContext";
import BookAppointmentModal from "../components/BookAppointmentModal";

function PropertyDetailPage() {
  const { id } = useParams();
  const { user } = useAuth();
  const [property, setProperty] = useState(null);
  const [loading, setLoading] = useState(true);
  const [applying, setApplying] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);
  const [applicationStatus, setApplicationStatus] = useState(null);
  const [isBookingModalOpen, setIsBookingModalOpen] = useState(false);
  const [actionType, setActionType] = useState('rent'); // 'rent' or 'buy'
  const [documentFile, setDocumentFile] = useState(null);
  const [appData, setAppData] = useState({
    full_name: '',
    email: '',
    phone: '',
    date_of_birth: '',
    marital_status: 'SINGLE',
    employment_type: 'EMPLOYED',
    company_name: '',
    college_name: '',
    monthly_income: '',
    current_address: '',
    move_in_date: '',
    lease_duration: 12,
    num_occupants: 1,
    additional_notes: ''
  });

  const handleAppChange = (e) => {
    const { name, value } = e.target;
    setAppData(prev => ({ ...prev, [name]: value }));
  };

  const handleApply = async (e) => {
    e.preventDefault();
    if (!user) {
      alert("Please log in to apply");
      return;
    }
    if (!documentFile) {
      alert("Please upload an ID document or payslip to proceed.");
      return;
    }
    setApplying(true);
    try {
      const payload = {
        ...appData,
        property_id: id,
        lease_duration: parseInt(appData.lease_duration),
        num_occupants: parseInt(appData.num_occupants),
        monthly_income: appData.monthly_income ? parseFloat(appData.monthly_income) : null
      };
      const result = await applyForProperty(payload);
      
      if (result && result.application && result.application.id) {
        const formData = new FormData();
        formData.append('document', documentFile);
        await uploadApplicationDocument(result.application.id, formData);
      }
      
      setApplicationStatus('success');
    } catch (err) {
      console.error(err);
      setErrorMsg("Failed to submit application");
      setApplicationStatus('error');
    } finally {
      setApplying(false);
    }
  };

  useEffect(() => {
    const fetchProp = async () => {
      try {
        const data = await getPropertyById(id);
        setProperty(data);
      } catch (err) {
        console.error("Error fetching property:", err);
        setErrorMsg(err.message || "Failed to fetch property details");
      } finally {
        setLoading(false);
      }
    };
    fetchProp();
  }, [id]);

  if (errorMsg) return <div className="p-12 text-center text-red-500 font-bold text-xl">Error: {errorMsg}</div>;
  if (loading) return <div className="p-12 text-center text-gray-500 font-bold text-xl">Loading Property Details...</div>;
  if (!property) return <div className="p-12 text-center text-red-500 font-bold text-xl">Property not found in database.</div>;

  try {
    return (
    <div className="min-h-screen bg-gray-50 font-sans">
      <Header />
      <main className="max-w-7xl mx-auto px-4 py-12">
        <Link to="/properties" className="text-brandRed hover:underline mb-6 inline-block">← Back to Search</Link>
        
        <div className="flex flex-col lg:flex-row gap-8">
          <div className="flex-1 bg-white rounded-xl shadow-md overflow-hidden border border-gray-200">
            {property.image_urls && property.image_urls.length > 0 && (
              <div className="h-64 bg-gray-200 flex items-center justify-center">
                 <img src={`http://localhost:8000${property.image_urls[0]}`} className="w-full h-full object-cover" alt="Property" />
              </div>
            )}
            
            <div className="p-8">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">{property.title}</h1>
              <p className="text-gray-600 mb-6 flex items-center gap-2">📍 {property.city} | {property.property_type}</p>
              
              <div className="bg-gray-50 p-4 rounded-lg mb-6 border border-gray-100 flex gap-8">
                <div>
                  <p className="text-sm text-gray-500 uppercase font-semibold">Rent</p>
                  <p className="text-2xl font-bold text-gray-900">₹{property.monthly_rent}</p>
                </div>
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

                <h3 className="font-semibold text-lg border-b pb-2 mb-4 mt-6">Seller Details</h3>
                <div className="bg-gray-50 p-4 rounded-lg border border-gray-100">
                  <p className="text-gray-800"><strong>Name:</strong> {property.owner_name}</p>
                </div>
              </div>
            </div>
          </div>

          <div className="w-full lg:w-1/3">
            <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm sticky top-6">
                <h3 className="text-xl font-bold text-gray-900 mb-4">Rental Application</h3>
              
              {applicationStatus === 'success' ? (
                <div className="bg-green-50 text-green-700 p-4 rounded border border-green-200">
                  Application created successfully! The owner will review it soon.
                </div>
              ) : (
                <form onSubmit={handleApply} className="flex flex-col gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
                    <input required type="text" name="full_name" value={appData.full_name} onChange={handleAppChange} className="w-full border p-2 rounded focus:outline-none focus:ring-1 focus:ring-black" />
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                      <input required type="email" name="email" value={appData.email} onChange={handleAppChange} className="w-full border p-2 rounded focus:outline-none focus:ring-1 focus:ring-black" />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Phone</label>
                      <input required type="text" name="phone" value={appData.phone} onChange={handleAppChange} className="w-full border p-2 rounded focus:outline-none focus:ring-1 focus:ring-black" />
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Date of Birth</label>
                      <input required type="date" name="date_of_birth" value={appData.date_of_birth} onChange={handleAppChange} className="w-full border p-2 rounded focus:outline-none focus:ring-1 focus:ring-black text-sm" />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Marital Status</label>
                      <select name="marital_status" value={appData.marital_status} onChange={handleAppChange} className="w-full border p-2 rounded focus:outline-none focus:ring-1 focus:ring-black text-sm">
                        <option value="SINGLE">Single</option>
                        <option value="MARRIED">Married</option>
                      </select>
                    </div>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Employment Type</label>
                    <select name="employment_type" value={appData.employment_type} onChange={handleAppChange} className="w-full border p-2 rounded focus:outline-none focus:ring-1 focus:ring-black">
                      <option value="EMPLOYED">Employed</option>
                      <option value="SELF_EMPLOYED">Self Employed</option>
                      <option value="STUDENT">Student</option>
                      <option value="UNEMPLOYED">Unemployed</option>
                    </select>
                  </div>

                  {appData.employment_type === 'STUDENT' ? (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">College Name</label>
                      <input type="text" name="college_name" value={appData.college_name} onChange={handleAppChange} className="w-full border p-2 rounded focus:outline-none focus:ring-1 focus:ring-black" />
                    </div>
                  ) : appData.employment_type !== 'UNEMPLOYED' ? (
                    <div className="grid grid-cols-2 gap-2">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Company</label>
                        <input type="text" name="company_name" value={appData.company_name} onChange={handleAppChange} className="w-full border p-2 rounded focus:outline-none focus:ring-1 focus:ring-black text-sm" />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Income (₹)</label>
                        <input type="number" name="monthly_income" value={appData.monthly_income} onChange={handleAppChange} className="w-full border p-2 rounded focus:outline-none focus:ring-1 focus:ring-black text-sm" />
                      </div>
                    </div>
                  ) : null}

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Current Address</label>
                    <input required type="text" name="current_address" value={appData.current_address} onChange={handleAppChange} className="w-full border p-2 rounded focus:outline-none focus:ring-1 focus:ring-black" />
                  </div>

                  <div className="grid grid-cols-3 gap-2">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Move-in</label>
                      <input required type="date" name="move_in_date" value={appData.move_in_date} onChange={handleAppChange} className="w-full border p-2 rounded focus:outline-none focus:ring-1 focus:ring-black text-xs" />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1 text-xs">Lease (Months)</label>
                      <input required type="number" min="1" name="lease_duration" value={appData.lease_duration} onChange={handleAppChange} className="w-full border p-2 rounded focus:outline-none focus:ring-1 focus:ring-black text-sm" />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1 text-xs">Occupants</label>
                      <input required type="number" min="1" name="num_occupants" value={appData.num_occupants} onChange={handleAppChange} className="w-full border p-2 rounded focus:outline-none focus:ring-1 focus:ring-black text-sm" />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Additional Notes</label>
                    <textarea 
                      name="additional_notes"
                      placeholder="Any pets, special requirements..." 
                      className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-black min-h-[60px] text-sm"
                      value={appData.additional_notes}
                      onChange={handleAppChange}
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">ID Document / Payslip (PDF/Image)</label>
                    <input 
                      required 
                      type="file" 
                      accept=".pdf,image/*" 
                      onChange={(e) => setDocumentFile(e.target.files[0])} 
                      className="w-full border p-2 rounded focus:outline-none focus:ring-1 focus:ring-black text-sm" 
                    />
                  </div>
                  
                  <button 
                    type="submit" 
                    disabled={applying || !property.is_available}
                    className="bg-black text-white px-4 py-3 rounded font-medium hover:bg-gray-800 transition disabled:bg-gray-400 mt-2"
                  >
                    {applying ? "Submitting..." : property.is_available ? "Create Application" : "Currently Unavailable"}
                  </button>
                  {!user && <p className="text-xs text-center text-red-500">You must be logged in to apply.</p>}
                </form>
              )}
            </div>
          </div>
        </div>
      </main>
      
      {isBookingModalOpen && (
        <BookAppointmentModal 
          propertyId={id} 
          onClose={() => setIsBookingModalOpen(false)} 
        />
      )}
    </div>
  );
  } catch (renderError) {
    return <div className="p-12 text-center text-red-500 font-bold text-xl">Render Error: {renderError.message}</div>;
  }
}

export default PropertyDetailPage;
