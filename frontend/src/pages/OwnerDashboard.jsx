import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import Header from "../components/Header";
import { getApplications, updateApplicationStatus } from "../services/api";
import { useAuth } from "../hooks/AuthContext";

function OwnerDashboard() {
  const { user, loading: authLoading } = useAuth();
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user && user.roles.includes("SELLER")) {
      fetchApplications();
    } else {
      setLoading(false);
    }
  }, [user]);

  const fetchApplications = async () => {
    try {
      const data = await getApplications();
      setApplications(Array.isArray(data) ? data : data.items || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleStatusUpdate = async (id, status) => {
    try {
      await updateApplicationStatus(id, status);
      fetchApplications(); // refresh
    } catch (err) {
      alert("Failed to update status.");
    }
  };

  if (authLoading || loading) return <div className="p-12 text-center text-gray-500">Loading Dashboard...</div>;
  if (!user || !user.roles.includes("SELLER")) {
    return <div className="p-12 text-center text-red-500">Access Denied. You must be an owner.</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50 font-sans">
      <Header />
      <main className="max-w-7xl mx-auto px-4 py-12">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Owner Dashboard</h1>
        
        <div className="bg-white rounded-lg shadow border border-gray-200 overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200 bg-gray-50">
            <h2 className="text-xl font-semibold text-gray-800">Rental Applications</h2>
          </div>
          <div className="divide-y divide-gray-200">
            {applications.length === 0 ? (
              <p className="p-6 text-gray-500">No applications received yet.</p>
            ) : (
              applications.map((app) => (
                <div key={app.id} className="p-6 flex items-center justify-between">
                  <div>
                    <h3 className="font-semibold text-gray-800">Property: {app.property_id}</h3>
                    <p className="text-sm text-gray-500 mt-1">Tenant: {app.tenant_id} | Status: <span className="font-bold">{app.status}</span></p>
                    {app.message && <p className="text-sm text-gray-600 mt-2 bg-gray-50 p-2 rounded">"{app.message}"</p>}
                  </div>
                  <div className="flex gap-2">
                    {app.status === 'PENDING' && (
                      <>
                        <button onClick={() => handleStatusUpdate(app.id, 'APPROVED')} className="bg-green-600 text-white px-4 py-2 rounded text-sm hover:bg-green-700">Approve</button>
                        <button onClick={() => handleStatusUpdate(app.id, 'REJECTED')} className="bg-red-100 text-red-700 px-4 py-2 rounded text-sm hover:bg-red-200">Reject</button>
                      </>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default OwnerDashboard;
