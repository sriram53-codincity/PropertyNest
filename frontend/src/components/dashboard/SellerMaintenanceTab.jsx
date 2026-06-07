import React from 'react';

function SellerMaintenanceTab({ sellerMaintenance, handleMaintenanceStatusUpdate }) {
  return (
    <div className="flex flex-col md:flex-row gap-8">
      <div className="flex-1">
        <h2 className="text-xl font-semibold mb-4">Maintenance Requests</h2>
        {sellerMaintenance.length === 0 ? <p className="text-gray-500">No requests found.</p> : (
          <ul className="space-y-4">
            {sellerMaintenance.map(req => (
              <li key={req.id} className="p-4 border rounded shadow-sm bg-white">
                <div className="flex justify-between items-start mb-2">
                  <p className="font-bold text-lg">{req.title}</p>
                  <span className={`text-xs px-2 py-1 rounded font-medium ${req.status === 'OPEN' ? 'bg-yellow-100 text-yellow-800' : req.status === 'IN_PROGRESS' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'}`}>{req.status}</span>
                </div>
                <p className="text-sm text-gray-600 mb-3">{req.description}</p>
                <div className="flex gap-4 text-xs text-gray-500 mb-2">
                  <p><span className="font-semibold text-gray-700">Category:</span> {req.category}</p>
                  <p><span className="font-semibold text-gray-700">Priority:</span> {req.priority}</p>
                </div>
                {req.comment && (
                  <div className="bg-gray-50 p-3 rounded border border-gray-200 mt-2">
                    <p className="text-xs text-gray-500 font-semibold uppercase mb-1">Owner Comment</p>
                    <p className="text-sm text-gray-700">{req.comment}</p>
                  </div>
                )}
                {(req.status === 'OPEN' || req.status === 'IN_PROGRESS') && (
                  <div className="flex gap-2 mt-4 pt-4 border-t border-gray-100">
                    {req.status === 'OPEN' && (
                      <button onClick={() => handleMaintenanceStatusUpdate(req.id, 'IN_PROGRESS')} className="bg-blue-600 text-white px-3 py-1.5 rounded text-sm font-medium hover:bg-blue-700 transition">Mark In Progress</button>
                    )}
                    <button onClick={() => handleMaintenanceStatusUpdate(req.id, 'RESOLVED')} className="bg-green-600 text-white px-3 py-1.5 rounded text-sm font-medium hover:bg-green-700 transition">Resolve</button>
                    <button onClick={() => handleMaintenanceStatusUpdate(req.id, 'CLOSED')} className="bg-gray-600 text-white px-3 py-1.5 rounded text-sm font-medium hover:bg-gray-700 transition">Close</button>
                  </div>
                )}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default SellerMaintenanceTab;
