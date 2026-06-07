import React from 'react';

function TenantApplicationsTab({ myApplications }) {
  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">My Applications</h2>
      {myApplications.length === 0 ? <p className="text-gray-500">No applications found.</p> : (
        <ul className="space-y-4">
          {myApplications.map((app) => (
            <li key={app.id} className="p-6 border rounded shadow-sm bg-white">
              <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-lg font-bold text-gray-900">Application for Property ID: {app.property_id}</h3>
                    <span className={`px-2 py-1 text-xs font-bold rounded-full ${app.status === 'APPROVED' ? 'bg-green-100 text-green-800' : app.status === 'REJECTED' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'}`}>
                      {app.status}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mb-4"><strong>Property:</strong> {app.property_title || `ID: ${app.property_id}`} | <strong>Owner:</strong> {app.owner_name || 'N/A'} | <strong>Applied on:</strong> {new Date(app.created_at || Date.now()).toLocaleDateString()}</p>
                  
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-4">
                    <div>
                      <p className="text-xs text-gray-500 uppercase font-semibold">Lease Request</p>
                      <p className="text-sm text-gray-800">Move-in: {new Date(app.move_in_date).toLocaleDateString()}</p>
                      <p className="text-sm text-gray-800">{app.lease_duration} Months | {app.num_occupants} Occupant(s)</p>
                    </div>
                  </div>

                  {app.reason && app.status === 'REJECTED' && (
                    <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded">
                      <p className="text-sm font-bold text-red-800">Rejection Reason:</p>
                      <p className="text-sm text-red-700">{app.reason}</p>
                    </div>
                  )}
                </div>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default TenantApplicationsTab;
