import React from 'react';

function TenantLeasesTab({ leases }) {
  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">My Leases</h2>
      {leases.length === 0 ? <p className="text-gray-500">No active leases.</p> : (
        <ul className="space-y-4">
          {leases.map(lease => (
            <li key={lease.id} className="p-4 border rounded shadow-sm bg-white">
              <p className="font-bold text-lg mb-2">Property ID: {lease.property_id}</p>
              <div className="grid grid-cols-2 gap-4 text-sm text-gray-700">
                <p><span className="font-semibold">Start:</span> {lease.start_date}</p>
                <p><span className="font-semibold">End:</span> {lease.end_date}</p>
                <p><span className="font-semibold">Rent:</span> ${lease.monthly_rent}</p>
                <p><span className="font-semibold">Status:</span> <span className={`px-2 py-1 rounded text-xs ${lease.status === 'ACTIVE' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>{lease.status}</span></p>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default TenantLeasesTab;
