import React from 'react';

function TenantMaintenanceTab({ maintenance, leases, handleMaintenanceSubmit }) {
  return (
    <div className="flex flex-col md:flex-row gap-8">
      <div className="flex-1">
        <h2 className="text-xl font-semibold mb-4">Maintenance Requests</h2>
        {maintenance.length === 0 ? <p className="text-gray-500">No requests found.</p> : (
          <ul className="space-y-4">
            {maintenance.map(req => (
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
              </li>
            ))}
          </ul>
        )}
      </div>
      
      {leases.length > 0 && (
        <div className="w-full md:w-1/3 bg-white p-6 border rounded shadow-sm h-fit">
          <h3 className="font-bold text-lg mb-4">New Request</h3>
          <form onSubmit={handleMaintenanceSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Lease</label>
              <select name="lease_id" required className="w-full border p-2 rounded focus:ring-2 focus:ring-brandRed outline-none">
                {leases.map(l => <option key={l.id} value={l.id}>Property {l.property_id}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Title</label>
              <input name="title" required className="w-full border p-2 rounded focus:ring-2 focus:ring-brandRed outline-none" placeholder="E.g. Leaking Faucet" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
              <select name="category" required className="w-full border p-2 rounded focus:ring-2 focus:ring-brandRed outline-none">
                <option value="PLUMBING">Plumbing</option>
                <option value="ELECTRICAL">Electrical</option>
                <option value="APPLIANCE">Appliance</option>
                <option value="OTHER">Other</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
              <textarea name="description" required className="w-full border p-2 rounded focus:ring-2 focus:ring-brandRed outline-none h-24" placeholder="Describe the issue..."></textarea>
            </div>
            <button type="submit" className="w-full bg-brandRed text-white py-2 rounded font-medium hover:bg-red-700 transition">Submit Request</button>
          </form>
        </div>
      )}
    </div>
  );
}

export default TenantMaintenanceTab;
