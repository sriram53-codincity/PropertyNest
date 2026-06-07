import React from 'react';

function AddPropertyTab({ handleCreateProperty }) {
  return (
    <div className="bg-white rounded-lg shadow border border-gray-200 p-6">
      <h2 className="text-xl font-semibold text-gray-800 mb-6">List a New Property</h2>
      <form onSubmit={handleCreateProperty} className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Title</label>
          <input required name="title" placeholder="Beautiful 2BHK Apartment" className="w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-brandRed" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">City</label>
          <select required name="city" className="w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-brandRed bg-white">
            <option value="">Select City</option>
            <option value="CHENNAI">Chennai</option>
            <option value="BANGALORE">Bangalore</option>
            <option value="MUMBAI">Mumbai</option>
            <option value="DELHI">Delhi</option>
            <option value="HYDERABAD">Hyderabad</option>
            <option value="PUNE">Pune</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Property Type</label>
          <select required name="property_type" className="w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-brandRed bg-white">
            <option value="Apartment">Apartment</option>
            <option value="House">House</option>
            <option value="Villa">Villa</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">BHK / Bedrooms</label>
          <input required type="number" min="1" name="bedrooms" defaultValue={1} className="w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-brandRed" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Address</label>
          <input required name="address" placeholder="123 Main St" className="w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-brandRed" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Monthly Rent ($)</label>
          <input required type="number" name="rent" placeholder="1500" className="w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-brandRed" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Deposit ($)</label>
          <input required type="number" name="deposit" placeholder="1500" className="w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-brandRed" />
        </div>
        <div className="md:col-span-2">
          <label className="block text-sm font-medium text-gray-700 mb-1">Amenities (comma separated)</label>
          <input name="amenities" placeholder="Pool, Gym, Parking" className="w-full border p-2 rounded focus:outline-none focus:ring-2 focus:ring-brandRed" />
        </div>
        <div className="md:col-span-2">
          <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
          <textarea required name="description" placeholder="Describe the property..." className="w-full border p-2 rounded h-24 focus:outline-none focus:ring-2 focus:ring-brandRed" />
        </div>
        <div className="md:col-span-2">
          <label className="block text-sm font-medium text-gray-700 mb-1">Images</label>
          <input type="file" name="images" multiple accept="image/*" className="w-full border p-2 rounded" />
        </div>
        <div className="md:col-span-2 mt-4">
          <button type="submit" className="bg-brandRed text-white px-6 py-3 rounded font-medium hover:bg-red-700 transition w-full md:w-auto">
            List Property
          </button>
        </div>
      </form>
    </div>
  );
}

export default AddPropertyTab;
