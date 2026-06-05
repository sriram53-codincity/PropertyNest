import { useState } from 'react';
import { Link } from 'react-router-dom';
import { bookAppointment } from '../services/api';

function LandingPage() {
  const [activeTab, setActiveTab] = useState('Tenants');
  const [showModal, setShowModal] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);
  
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    phone: '',
    preferred_date: '',
    preferred_time: '10:00 AM'
  });

  const handleBookingSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await bookAppointment({
        ...formData,
        purpose: 'GENERAL_INQUIRY',
        additional_notes: `Requested from Landing Page - Role: ${activeTab}`
      });
      setSuccess(true);
      setTimeout(() => {
        setShowModal(false);
        setSuccess(false);
        setFormData({ full_name: '', email: '', phone: '', preferred_date: '', preferred_time: '10:00 AM' });
      }, 3000);
    } catch (err) {
      alert("Failed to book appointment. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-white font-sans flex flex-col text-gray-900 overflow-x-hidden">
      
      {/* Navbar */}
      <header className="flex justify-between items-center p-6 border-b border-gray-100 max-w-7xl mx-auto w-full">
        <div className="flex items-center text-brandRed text-2xl font-bold gap-2">
          <span className="text-3xl text-red-500">❖</span>
          PropertyNest
        </div>
        
        <div className="hidden md:flex items-center gap-6 text-sm font-medium">
          <button 
            onClick={() => setShowModal(true)} 
            className="text-gray-500 hover:text-gray-900 transition flex items-center gap-1 cursor-pointer"
          >
            Call for reference <span className="bg-gray-100 text-gray-500 px-1.5 rounded text-xs">C</span>
          </button>
          
          <Link to="/login" className="bg-black text-white px-5 py-2.5 rounded-lg hover:bg-gray-800 transition shadow-md">
            Log in
          </Link>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex flex-col items-center text-center px-4 pt-16 pb-24 max-w-4xl mx-auto w-full">
        
        {/* Toggle (Tenants / Sellers) */}
        <div className="bg-gray-50 rounded-full p-1 inline-flex mb-16 shadow-inner border border-gray-100">
          <button 
            onClick={() => setActiveTab('Tenants')}
            className={`rounded-full px-6 py-2 shadow-sm font-medium text-sm transition ${activeTab === 'Tenants' ? 'bg-white text-gray-900' : 'text-gray-500 hover:text-gray-900'}`}
          >
            Tenants
          </button>
          <button 
            onClick={() => setActiveTab('Sellers')}
            className={`rounded-full px-6 py-2 shadow-sm font-medium text-sm transition ${activeTab === 'Sellers' ? 'bg-white text-gray-900' : 'text-gray-500 hover:text-gray-900'}`}
          >
            Sellers
          </button>
        </div>

        {/* Hero Text */}
        <p className="text-brandRed font-bold tracking-wide uppercase text-sm mb-6">
          Property Rentals That Actually Work
        </p>
        
        {activeTab === 'Tenants' ? (
          <>
            <h1 className="text-6xl md:text-7xl font-extrabold tracking-tight mb-4 leading-tight">
              Find the perfect home.<br />
              <span className="text-brandRed">Skip the busywork.</span>
            </h1>
            <p className="text-xl text-gray-600 mb-12 max-w-2xl leading-relaxed">
              Describe what you need in plain English and get matched with properties in seconds. 
              Pick a location, set your budget, and let the perfect home come to you.
            </p>
          </>
        ) : (
          <>
            <h1 className="text-6xl md:text-7xl font-extrabold tracking-tight mb-4 leading-tight">
              Find the right tenants.<br />
              <span className="text-brandRed">Skip the busywork.</span>
            </h1>
            <p className="text-xl text-gray-600 mb-12 max-w-2xl leading-relaxed">
              List your property and get matched with verified tenants instantly. Manage applications, 
              maintenance, and leases all in one place.
            </p>
          </>
        )}
        
        {/* Call to Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 mb-20">
          <Link to="/login" className="bg-black text-white px-8 py-3.5 rounded-lg font-medium hover:bg-gray-800 transition shadow-lg flex items-center justify-center gap-2 text-lg">
            Get started <span>→</span>
          </Link>
        </div>

        {/* Features List */}
        <div className="flex flex-wrap justify-center gap-8 text-gray-600 text-sm border-t border-gray-100 pt-10 w-full">
          <div className="flex items-center gap-2">
            <span className="text-brandRed font-bold">✓</span> Search by exact requirements
          </div>
          <div className="flex items-center gap-2">
            <span className="text-brandRed font-bold">✓</span> Simple digital applications
          </div>
          <div className="flex items-center gap-2">
            <span className="text-brandRed font-bold">✓</span> Verified owners and properties
          </div>
        </div>
      </main>

      {/* Side Decorative Borders matching the image */}
      <div className="hidden lg:block fixed left-10 top-0 bottom-0 w-px border-l-2 border-dashed border-gray-200 -z-10"></div>
      <div className="hidden lg:block fixed right-10 top-0 bottom-0 w-px border-l-2 border-dashed border-gray-200 -z-10"></div>

      {/* Appointment Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-2xl p-8 max-w-md w-full relative">
            <button onClick={() => setShowModal(false)} className="absolute top-4 right-4 text-gray-400 hover:text-gray-800 text-xl font-bold">&times;</button>
            <h2 className="text-2xl font-bold mb-6 text-gray-900">Request a Reference Call</h2>
            
            {success ? (
              <div className="bg-green-50 text-green-700 p-4 rounded-lg border border-green-200 text-center font-medium">
                Request submitted successfully! Our team will contact you shortly.
              </div>
            ) : (
              <form onSubmit={handleBookingSubmit} className="flex flex-col gap-4 text-left">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
                  <input type="text" required value={formData.full_name} onChange={e => setFormData({...formData, full_name: e.target.value})} className="w-full border border-gray-300 rounded-lg p-2.5 focus:ring-black focus:border-black" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                  <input type="email" required value={formData.email} onChange={e => setFormData({...formData, email: e.target.value})} className="w-full border border-gray-300 rounded-lg p-2.5 focus:ring-black focus:border-black" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Phone</label>
                  <input type="text" required value={formData.phone} onChange={e => setFormData({...formData, phone: e.target.value})} className="w-full border border-gray-300 rounded-lg p-2.5 focus:ring-black focus:border-black" />
                </div>
                <div className="flex gap-4">
                  <div className="flex-1">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Date</label>
                    <input type="date" required value={formData.preferred_date} onChange={e => setFormData({...formData, preferred_date: e.target.value})} className="w-full border border-gray-300 rounded-lg p-2.5 focus:ring-black focus:border-black" />
                  </div>
                  <div className="flex-1">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Time</label>
                    <select required value={formData.preferred_time} onChange={e => setFormData({...formData, preferred_time: e.target.value})} className="w-full border border-gray-300 rounded-lg p-2.5 focus:ring-black focus:border-black">
                      <option>10:00 AM</option>
                      <option>12:00 PM</option>
                      <option>02:00 PM</option>
                      <option>04:00 PM</option>
                    </select>
                  </div>
                </div>
                
                <button type="submit" disabled={submitting} className="mt-4 w-full bg-black text-white rounded-lg py-3 font-semibold hover:bg-gray-800 transition disabled:bg-gray-400">
                  {submitting ? "Submitting..." : "Schedule Call"}
                </button>
              </form>
            )}
          </div>
        </div>
      )}

    </div>
  );
}

export default LandingPage;
