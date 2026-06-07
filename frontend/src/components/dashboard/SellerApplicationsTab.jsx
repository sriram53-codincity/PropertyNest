import React from 'react';

function SellerApplicationsTab({ receivedApplications, handleStatusUpdate, handleCreateLease }) {
  return (
    <div className="bg-white rounded-lg shadow border border-gray-200 overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-200 bg-gray-50">
        <h2 className="text-xl font-semibold text-gray-800">Received Applications</h2>
      </div>
      <div className="divide-y divide-gray-200">
        {receivedApplications.length === 0 ? (
          <p className="p-6 text-gray-500">No applications received yet.</p>
        ) : (
          receivedApplications.map((app) => (
            <div key={app.id} className="p-6">
              <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-lg font-bold text-gray-900">{app.full_name || 'Applicant'}</h3>
                    <span className={`px-2 py-1 text-xs font-bold rounded-full ${app.status === 'APPROVED' ? 'bg-green-100 text-green-800' : app.status === 'REJECTED' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'}`}>
                      {app.status}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mb-4"><strong>Property:</strong> {app.property_title || `ID: ${app.property_id}`} | <strong>Applied on:</strong> {new Date(app.created_at || Date.now()).toLocaleDateString()}</p>
                  
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-4">
                    <div>
                      <p className="text-xs text-gray-500 uppercase font-semibold">Contact Info</p>
                      <p className="text-sm text-gray-800">{app.email}</p>
                      <p className="text-sm text-gray-800">{app.phone}</p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500 uppercase font-semibold">Employment</p>
                      <p className="text-sm text-gray-800">{app.employment_type} {app.company_name ? `at ${app.company_name}` : app.college_name ? `at ${app.college_name}` : ''}</p>
                      {app.monthly_income && <p className="text-sm text-gray-800 text-green-700 font-medium">Income: ₹{Number(app.monthly_income).toFixed(0)}</p>}
                    </div>
                    <div>
                      <p className="text-xs text-gray-500 uppercase font-semibold">Lease Request</p>
                      <p className="text-sm text-gray-800">Move-in: {new Date(app.move_in_date).toLocaleDateString()}</p>
                      <p className="text-sm text-gray-800">{app.lease_duration} Months | {app.num_occupants} Occupant(s)</p>
                    </div>
                  </div>

                  {app.additional_notes && (
                    <div className="bg-gray-50 p-3 rounded-lg border border-gray-100 mb-4">
                      <p className="text-xs text-gray-500 uppercase font-semibold mb-1">Notes</p>
                      <p className="text-sm text-gray-700 italic">"{app.additional_notes}"</p>
                    </div>
                  )}
                  
                  {app.status === 'REJECTED' && app.reason && (
                    <div className="bg-red-50 p-3 rounded-lg border border-red-100 mb-4">
                      <p className="text-xs text-red-800 uppercase font-semibold mb-1">Rejection Reason</p>
                      <p className="text-sm text-red-700">"{app.reason}"</p>
                    </div>
                  )}

                  {app.gov_id_url && (
                    <div className="mb-4">
                      <a href={`http://localhost:8000${app.gov_id_url}`} target="_blank" rel="noopener noreferrer" className="inline-flex items-center text-sm font-medium text-blue-600 hover:text-blue-800 hover:underline bg-blue-50 px-3 py-1.5 rounded">
                        📄 View Attached Document (ID / Payslip)
                      </a>
                    </div>
                  )}
                </div>
                
                <div className="flex flex-col gap-2 min-w-[120px]">
                  {app.status === 'PENDING' && (
                    <>
                      <button onClick={() => handleStatusUpdate(app.id, 'APPROVED')} className="w-full bg-green-600 text-white px-4 py-2 rounded text-sm font-medium hover:bg-green-700 transition shadow-sm">Approve</button>
                      <button onClick={() => handleStatusUpdate(app.id, 'REJECTED')} className="w-full bg-red-50 text-red-700 border border-red-200 px-4 py-2 rounded text-sm font-medium hover:bg-red-100 transition shadow-sm">Reject</button>
                    </>
                  )}
                  {app.status === 'APPROVED' && (
                    <button 
                      onClick={() => handleCreateLease(app.id)}
                      className="w-full bg-brandRed text-white px-4 py-2 rounded text-sm font-medium hover:bg-red-700 transition shadow-sm"
                    >
                      Generate Lease
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default SellerApplicationsTab;
