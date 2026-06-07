import React from 'react';

function TenantSellerRequestsTab({ sellerRequests }) {
  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">My Seller Requests</h2>
      {sellerRequests.length === 0 ? <p className="text-gray-500">No seller requests found.</p> : (
        <ul className="space-y-4">
          {sellerRequests.map(req => (
            <li key={req.id} className="p-4 border rounded shadow-sm bg-white">
              <div className="flex justify-between items-start mb-2">
                <p className="font-bold text-lg">{req.property_title}</p>
                <span className={`text-xs px-2 py-1 rounded font-medium ${req.status === 'APPROVED' ? 'bg-green-100 text-green-800' : req.status === 'REJECTED' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'}`}>{req.status}</span>
              </div>
              <p className="text-sm text-gray-600 mb-3">{req.property_address}</p>
              <div className="flex gap-4 text-xs text-gray-500">
                <p><span className="font-semibold text-gray-700">Type:</span> {req.property_type}</p>
                <p><span className="font-semibold text-gray-700">Rent:</span> ${req.monthly_rent}</p>
              </div>
              {req.reason && <p className="text-sm text-red-600 mt-2 italic">Reason: {req.reason}</p>}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default TenantSellerRequestsTab;
