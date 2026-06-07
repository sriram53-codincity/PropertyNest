import { useState } from 'react';
import { bookAppointment } from '../services/api';

function BookAppointmentModal({ propertyId, onClose }) {
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    phone: '',
    preferred_date: '',
    preferred_time: '',
    additional_notes: ''
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await bookAppointment({
        full_name: formData.full_name,
        email: formData.email,
        phone: formData.phone,
        purpose: 'PROPERTY_TOUR',
        preferred_date: formData.preferred_date,
        preferred_time: formData.preferred_time,
        additional_notes: `Property ID: ${propertyId}\n\n${formData.additional_notes}`
      });
      alert('Appointment booked successfully!');
      onClose();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to book appointment.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50 p-4 overflow-y-auto">
      <div className="bg-white p-6 rounded-lg w-full max-w-md shadow-xl my-8">
        <h2 className="text-xl font-bold mb-4 text-gray-900">Book a Viewing</h2>
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <div>
            <label className="block text-sm font-medium mb-1 text-gray-700">Full Name</label>
            <input type="text" required name="full_name" value={formData.full_name} onChange={handleChange} className="w-full border border-gray-300 p-2 rounded focus:ring-2 focus:ring-brandRed focus:outline-none" />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1 text-gray-700">Email</label>
            <input type="email" required name="email" value={formData.email} onChange={handleChange} className="w-full border border-gray-300 p-2 rounded focus:ring-2 focus:ring-brandRed focus:outline-none" />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1 text-gray-700">Phone</label>
            <input type="text" required name="phone" value={formData.phone} onChange={handleChange} className="w-full border border-gray-300 p-2 rounded focus:ring-2 focus:ring-brandRed focus:outline-none" />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1 text-gray-700">Preferred Date</label>
              <input type="date" required name="preferred_date" value={formData.preferred_date} onChange={handleChange} className="w-full border border-gray-300 p-2 rounded focus:ring-2 focus:ring-brandRed focus:outline-none" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1 text-gray-700">Preferred Time</label>
              <input type="time" required name="preferred_time" value={formData.preferred_time} onChange={handleChange} className="w-full border border-gray-300 p-2 rounded focus:ring-2 focus:ring-brandRed focus:outline-none" />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1 text-gray-700">Message (Optional)</label>
            <textarea 
              name="additional_notes"
              className="w-full border border-gray-300 p-2 rounded focus:ring-2 focus:ring-brandRed focus:outline-none h-20"
              placeholder="Any specific questions before you view the property?"
              value={formData.additional_notes}
              onChange={handleChange}
            />
          </div>
          <div className="flex gap-2 justify-end mt-4">
            <button type="button" onClick={onClose} className="px-4 py-2 text-gray-500 hover:text-black transition">Cancel</button>
            <button type="submit" disabled={loading} className="bg-brandRed text-white px-4 py-2 rounded font-medium hover:bg-red-700 transition disabled:bg-red-300">
              {loading ? 'Booking...' : 'Book Appointment'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default BookAppointmentModal;
