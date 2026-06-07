import React from 'react';

function SellerPropertiesTab({ myListedProperties, handleMarkAsSold, handleMarkAsAvailable, handleDeleteProperty }) {
  return (
    <div className="bg-white rounded-lg shadow border border-gray-200 overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-200 bg-gray-50">
        <h2 className="text-xl font-semibold text-gray-800">My Listed Properties</h2>
      </div>
      <div className="divide-y divide-gray-200">
        {myListedProperties.length === 0 ? (
          <p className="p-6 text-gray-500">You haven't listed any properties yet.</p>
        ) : (
          myListedProperties.map((prop) => (
            <div key={prop.id} className="p-6 flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-brandRed">{prop.title}</h3>
                <p className="text-sm text-gray-600 mt-1">{prop.city} | {prop.property_type} | {prop.bedrooms} BHK | {prop.bathrooms} Bath</p>
                <p className="text-sm font-medium text-gray-800 mt-1">Rent: ₹{prop.monthly_rent}</p>
                <p className="text-sm text-gray-600 mt-1">
                  Status: <span className={`font-bold ${prop.is_available ? 'text-green-600' : 'text-red-600'}`}>{prop.is_available ? "Available" : "Sold/Unavailable"}</span>
                </p>
              </div>
              <div className="flex gap-2">
                {prop.is_available ? (
                  <button onClick={() => handleMarkAsSold(prop.id)} className="bg-yellow-500 text-white px-4 py-2 rounded text-sm font-medium hover:bg-yellow-600 transition shadow-sm">Mark as Sold</button>
                ) : (
                  <button onClick={() => handleMarkAsAvailable(prop.id)} className="bg-green-600 text-white px-4 py-2 rounded text-sm font-medium hover:bg-green-700 transition shadow-sm">Mark as Available</button>
                )}
                <button onClick={() => handleDeleteProperty(prop.id)} className="bg-red-600 text-white px-4 py-2 rounded text-sm font-medium hover:bg-red-700 transition shadow-sm">Delete</button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default SellerPropertiesTab;
