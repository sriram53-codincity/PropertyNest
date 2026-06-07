import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import { createSellerRequest } from '../services/api';

function BecomeSellerPage() {
  const [formData, setFormData] = useState({
    full_name: '',
    phone: '',
    address: '',
    property_title: '',
    property_address: '',
    district: 'CHENNAI',
    property_type: 'APARTMENT',
    bedrooms: 1,
    monthly_rent: '',
    description: '',
    doc_type: 'DEED',
    declaration_accepted: false
  });
  
  const [files, setFiles] = useState({
    ownership_doc: null,
    property_image: null
  });
  
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(null);
  
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleFileChange = (e) => {
    const { name, files: selectedFiles } = e.target;
    setFiles(prev => ({
      ...prev,
      [name]: selectedFiles[0]
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    if (!files.ownership_doc || !files.property_image) {
      setError("Please upload both required documents.");
      setLoading(false);
      return;
    }

    try {
      const data = new FormData();
      Object.keys(formData).forEach(key => {
        data.append(key, formData[key]);
      });
      data.append('ownership_doc', files.ownership_doc);
      data.append('property_image', files.property_image);

      await createSellerRequest(data);
      setSuccess(true);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to submit request.");
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <div className="max-w-3xl mx-auto py-16 px-4 sm:px-6 lg:px-8 text-center">
          <div className="bg-white p-10 rounded-lg shadow border border-gray-100">
            <div className="text-5xl mb-6">🎉</div>
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Request Submitted Successfully!</h2>
            <p className="text-gray-600 mb-8 text-lg">
              Thank you for applying to become a property owner on PropertyNest. 
              Our admin team will review your application and documents shortly.
            </p>
            <button 
              onClick={() => navigate('/properties')}
              className="bg-black text-white px-8 py-3 rounded-md hover:bg-gray-800 transition font-medium"
            >
              Back to Browse
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <div className="max-w-3xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Become a Seller</h1>
          <p className="mt-2 text-gray-600">Upgrade your account to list properties on PropertyNest.</p>
        </div>

        <div className="bg-white shadow sm:rounded-lg border border-gray-200">
          <form className="space-y-8 divide-y divide-gray-200 p-8" onSubmit={handleSubmit}>
            
            {/* Personal Info */}
            <div className="space-y-6">
              <div>
                <h3 className="text-lg leading-6 font-medium text-gray-900">Personal Information</h3>
                <p className="mt-1 text-sm text-gray-500">How we can contact you regarding your properties.</p>
              </div>
              <div className="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-2">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Full Name</label>
                  <input required type="text" name="full_name" value={formData.full_name} onChange={handleChange} className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-black focus:border-black sm:text-sm" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Phone</label>
                  <input required type="text" name="phone" value={formData.phone} onChange={handleChange} className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-black focus:border-black sm:text-sm" />
                </div>
                <div className="sm:col-span-2">
                  <label className="block text-sm font-medium text-gray-700">Current Address</label>
                  <input required type="text" name="address" value={formData.address} onChange={handleChange} className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-black focus:border-black sm:text-sm" />
                </div>
              </div>
            </div>

            {/* Property Info */}
            <div className="pt-8 space-y-6">
              <div>
                <h3 className="text-lg leading-6 font-medium text-gray-900">First Property Details</h3>
                <p className="mt-1 text-sm text-gray-500">Provide details for the first property you wish to list.</p>
              </div>
              <div className="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-2">
                <div className="sm:col-span-2">
                  <label className="block text-sm font-medium text-gray-700">Property Title</label>
                  <input required type="text" name="property_title" value={formData.property_title} onChange={handleChange} className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-black focus:border-black sm:text-sm" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Property Address</label>
                  <input required type="text" name="property_address" value={formData.property_address} onChange={handleChange} className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-black focus:border-black sm:text-sm" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Place</label>
                  <select name="district" value={formData.district} onChange={handleChange} className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-black focus:border-black sm:text-sm rounded-md border">
                    <option value="CHENNAI">Chennai</option>
                    <option value="BANGALORE">Bangalore</option>
                    <option value="HYDERABAD">Hyderabad</option>
                    <option value="MUMBAI">Mumbai</option>
                    <option value="PUNE">Pune</option>
                    <option value="DELHI">Delhi</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Property Type</label>
                  <select name="property_type" value={formData.property_type} onChange={handleChange} className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-black focus:border-black sm:text-sm rounded-md border">
                    <option value="APARTMENT">Apartment</option>
                    <option value="HOUSE">House</option>
                    <option value="VILLA">Villa</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">BHK / Bedrooms</label>
                  <input required type="number" min="1" name="bedrooms" value={formData.bedrooms} onChange={handleChange} className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-black focus:border-black sm:text-sm" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Expected Monthly Rent (₹)</label>
                  <input required type="number" name="monthly_rent" value={formData.monthly_rent} onChange={handleChange} className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-black focus:border-black sm:text-sm" />
                </div>
                <div className="sm:col-span-2">
                  <label className="block text-sm font-medium text-gray-700">Property Description</label>
                  <textarea
                    name="description"
                    value={formData.description}
                    onChange={handleChange}
                    required
                    rows="4"
                    className="w-full border p-2 rounded focus:outline-none focus:ring-1 focus:ring-black"
                    placeholder="Describe your property (amenities, location highlights, etc.)..."
                  />
                </div>
              </div>
            </div>

            {/* Documents */}
            <div className="pt-8 space-y-6">
              <div>
                <h3 className="text-lg leading-6 font-medium text-gray-900">Document Uploads</h3>
                <p className="mt-1 text-sm text-gray-500">We need proof of ownership to approve your account.</p>
              </div>
              <div className="grid grid-cols-1 gap-y-6 sm:grid-cols-2">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Document Type</label>
                  <select name="doc_type" value={formData.doc_type} onChange={handleChange} className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-black focus:border-black sm:text-sm rounded-md border">
                    <option value="DEED">Title Deed</option>
                    <option value="TAX_RECEIPT">Tax Receipt</option>
                    <option value="UTILITY_BILL">Utility Bill</option>
                  </select>
                </div>
                <div></div>
                
                <div className="sm:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-2">Proof of Ownership (PDF/Image)</label>
                  <input type="file" required name="ownership_doc" accept=".pdf,image/*" onChange={handleFileChange} className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-gray-50 file:text-black hover:file:bg-gray-100 border border-gray-300 rounded-md p-2" />
                </div>

                <div className="sm:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-2">Property Photo</label>
                  <input type="file" required name="property_image" accept="image/*" onChange={handleFileChange} className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-gray-50 file:text-black hover:file:bg-gray-100 border border-gray-300 rounded-md p-2" />
                </div>
              </div>
            </div>

            {/* Submission */}
            <div className="pt-8">
              <div className="flex items-start">
                <div className="flex items-center h-5">
                  <input required id="declaration" name="declaration_accepted" type="checkbox" checked={formData.declaration_accepted} onChange={handleChange} className="focus:ring-black h-4 w-4 text-black border-gray-300 rounded" />
                </div>
                <div className="ml-3 text-sm">
                  <label htmlFor="declaration" className="font-medium text-gray-700">I declare that the information provided is accurate and I own the property.</label>
                </div>
              </div>
              
              {error && (
                <div className="mt-4 text-sm text-red-600 bg-red-50 p-3 rounded">
                  {error}
                </div>
              )}

              <div className="mt-6 flex justify-end">
                <button type="submit" disabled={loading} className="ml-3 inline-flex justify-center py-2 px-6 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-black hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-black disabled:bg-gray-400">
                  {loading ? 'Submitting...' : 'Submit Application'}
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default BecomeSellerPage;
