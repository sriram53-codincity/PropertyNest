import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/AuthContext';
import { 
  getAllSellerRequests, updateSellerRequestStatus,
  getApplications, updateApplicationStatus,
  getAppointments, updateAppointmentStatus,
  getAdminProperties, updateProperty,
  getAdminUsers, deleteAdminUser
} from '../services/api';

export default function AdminDashboard() {
  const [activeTab, setActiveTab] = useState('requests');
  const [requests, setRequests] = useState([]);
  const [applications, setApplications] = useState([]);
  const [appointments, setAppointments] = useState([]);
  const [properties, setProperties] = useState([]);
  const [usersList, setUsersList] = useState([]);
  
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (user && !user.roles?.includes('ADMIN')) {
      navigate('/properties');
      return;
    }
    if (user) {
      fetchData();
    }
  }, [user, navigate, activeTab]);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      if (activeTab === 'requests') {
        const data = await getAllSellerRequests();
        setRequests(data);
      } else if (activeTab === 'applications') {
        const data = await getApplications();
        setApplications(Array.isArray(data) ? data : data.items || []);
      } else if (activeTab === 'appointments') {
        const data = await getAppointments();
        setAppointments(Array.isArray(data) ? data : data.items || []);
      } else if (activeTab === 'properties') {
        const data = await getAdminProperties();
        setProperties(Array.isArray(data) ? data : []);
      } else if (activeTab === 'buyers' || activeTab === 'sellers') {
        const data = await getAdminUsers();
        setUsersList(Array.isArray(data) ? data : []);
      }
    } catch (err) {
      setError(`Failed to load data: ${err.response?.data?.detail || err.message}`);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateSellerRequest = async (id, status) => {
    try {
      await updateSellerRequestStatus(id, status);
      fetchData();
    } catch (err) {
      alert(err.response?.data?.detail || "Failed to update status.");
    }
  };

  const handleUpdateApplication = async (id, status) => {
    try {
      await updateApplicationStatus(id, status);
      fetchData();
    } catch (err) {
      alert(`Failed to update application: ${err.message}`);
    }
  };

  const handleDeleteUser = async (userId, fullName) => {
    if (!window.confirm(`Are you sure you want to completely delete the user "${fullName}"? This action cannot be undone.`)) {
      return;
    }
    try {
      await deleteAdminUser(userId);
      setUsersList(usersList.filter(u => u.id !== userId));
    } catch (err) {
      alert(`Failed to delete user: ${err.response?.data?.detail || err.message}`);
    }
  };

  const handleUpdateAppointment = async (id, status) => {
    try {
      await updateAppointmentStatus(id, status);
      fetchData();
    } catch (err) {
      alert("Failed to update appointment status.");
    }
  };

  const handleUpdatePropertyStatus = async (id, status) => {
    try {
      const reason = status === 'REJECTED' ? prompt("Reason for rejection:") : null;
      if (status === 'REJECTED' && !reason) return;
      await updateProperty(id, { status, reason });
      fetchData();
    } catch (err) {
      alert(err.response?.data?.detail || "Failed to update property status.");
    }
  };

  return (
    <div className="w-full">
        <p className="text-gray-500 mb-6">Manage platform seller requests, properties, users, and appointments.</p>

        <div className="flex gap-4 mb-8 border-b border-gray-200 pb-1 overflow-x-auto">
          {['requests', 'properties', 'buyers', 'sellers', 'appointments'].map(tab => (
            <button 
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 py-2.5 capitalize font-medium whitespace-nowrap transition-colors relative ${activeTab === tab ? 'text-brandRed' : 'text-gray-500 hover:text-gray-800'}`}
            >
              {tab.replace('-', ' ')}
              {activeTab === tab && (
                <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-brandRed rounded-t-md"></div>
              )}
            </button>
          ))}
        </div>

        {error && (
          <div className="mb-6 bg-red-50 p-4 rounded-md text-red-700 text-sm">
            {error}
          </div>
        )}

        {loading ? (
          <div className="text-center py-10 text-gray-500">Loading data...</div>
        ) : (
          <div className="bg-white shadow overflow-hidden sm:rounded-lg border border-gray-200">
            
            {activeTab === 'requests' && (
              <>
                <div className="px-4 py-5 border-b border-gray-200 sm:px-6 flex justify-between items-center bg-gray-50">
                  <h3 className="text-lg leading-6 font-medium text-gray-900">Pending Seller Requests</h3>
                  <span className="bg-black text-white text-xs px-2 py-1 rounded-full">
                    {requests.filter(r => r.status === 'PENDING').length} Pending
                  </span>
                </div>
                <ul className="divide-y divide-gray-200">
                  {requests.length === 0 ? (
                    <li className="px-4 py-8 text-center text-gray-500">No seller requests found.</li>
                  ) : (
                    [...requests].sort((a, b) => {
                      if (a.status === 'PENDING' && b.status !== 'PENDING') return -1;
                      if (a.status !== 'PENDING' && b.status === 'PENDING') return 1;
                      return 0;
                    }).map((req) => (
                      <li key={req.id} className="p-6">
                        <div className="flex items-center justify-between">
                          <div className="flex-1">
                            <div className="flex items-center justify-between">
                              <p className="text-sm font-medium text-brandRed truncate">
                                User #{req.user_id} — {req.full_name}
                              </p>
                              <div className="ml-2 flex-shrink-0 flex">
                                <p className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                                  ${req.status === 'APPROVED' ? 'bg-green-100 text-green-800' : 
                                    req.status === 'REJECTED' ? 'bg-red-100 text-red-800' : 
                                    'bg-yellow-100 text-yellow-800'}`}>
                                  {req.status}
                                </p>
                              </div>
                            </div>
                            <div className="mt-2 sm:flex sm:justify-between">
                              <div className="sm:flex flex-col gap-1 text-sm text-gray-500">
                                <p><span className="font-semibold">Property:</span> {req.property_title} ({req.property_type})</p>
                                <p><span className="font-semibold">Address:</span> {req.property_address}</p>
                                <p><span className="font-semibold">Rent:</span> ₹{req.monthly_rent}/month</p>
                                {req.description && (
                                  <div className="mt-2 p-3 bg-white border rounded shadow-sm text-gray-700">
                                    <span className="font-semibold block mb-1">Description:</span>
                                    <p className="italic whitespace-pre-wrap">{req.description}</p>
                                  </div>
                                )}
                              </div>
                              <div className="mt-2 flex items-center text-sm text-gray-500 sm:mt-0 gap-4">
                                <a href={`http://localhost:8000${req.doc_url}`} target="_blank" rel="noreferrer" className="text-blue-600 hover:underline">
                                  📄 View Document ({req.doc_type})
                                </a>
                                {req.image_urls && JSON.parse(req.image_urls).length > 0 && (
                                  <a href={`http://localhost:8000${JSON.parse(req.image_urls)[0]}`} target="_blank" rel="noreferrer" className="text-blue-600 hover:underline">
                                    🖼️ View Image
                                  </a>
                                )}
                              </div>
                            </div>
                          </div>
                        </div>
                        {req.status === 'PENDING' && (
                          <div className="mt-6 flex gap-3 border-t border-gray-100 pt-4">
                            <button onClick={() => handleUpdateSellerRequest(req.id, 'APPROVED')} className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md text-sm font-medium transition shadow-sm">
                              Approve & Grant Seller Role
                            </button>
                            <button onClick={() => handleUpdateSellerRequest(req.id, 'REJECTED')} className="bg-red-50 hover:bg-red-100 text-red-700 px-4 py-2 rounded-md text-sm font-medium transition border border-red-200">
                              Reject
                            </button>
                          </div>
                        )}
                      </li>
                    ))
                  )}
                </ul>
              </>
            )}

            {activeTab === 'appointments' && (
              <>
                <div className="px-4 py-5 border-b border-gray-200 sm:px-6 bg-gray-50">
                  <h3 className="text-lg leading-6 font-medium text-gray-900">Global Appointments Overview</h3>
                </div>
                <ul className="divide-y divide-gray-200">
                  {appointments.length === 0 ? (
                    <li className="px-4 py-8 text-center text-gray-500">No appointments found.</li>
                  ) : (
                    [...appointments].sort((a, b) => {
                      if (a.status === 'PENDING' && b.status !== 'PENDING') return -1;
                      if (a.status !== 'PENDING' && b.status === 'PENDING') return 1;
                      return 0;
                    }).map((apt) => (
                      <li key={apt.id} className="p-6">
                        <div className="flex justify-between items-start">
                          <div>
                            <p className="font-semibold text-brandRed">{apt.preferred_date} at {apt.preferred_time}</p>
                            <p className="text-sm text-gray-600 mt-1">{apt.full_name} | {apt.email} | {apt.phone}</p>
                            <p className="text-sm text-gray-600 mt-1">Purpose: {apt.purpose.replace('_', ' ')}</p>
                            {apt.additional_notes && <p className="text-sm text-gray-500 mt-2 italic whitespace-pre-wrap">{apt.additional_notes}</p>}
                          </div>
                          <div className="flex flex-col items-end gap-2">
                            <span className={`px-2 py-1 text-xs font-semibold rounded-full ${apt.status === 'CONFIRMED' || apt.status === 'APPROVED' ? 'bg-green-100 text-green-800' : apt.status === 'CANCELLED' || apt.status === 'REJECTED' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'}`}>
                              {apt.status}
                            </span>
                            {(apt.status === 'CONFIRMED' || apt.status === 'APPROVED') && (
                              <a href={`https://meet.jit.si/PropertyNest_${apt.id}`} target="_blank" rel="noopener noreferrer" className="bg-blue-600 text-white px-3 py-1.5 rounded text-sm font-medium hover:bg-blue-700 transition shadow-sm">
                                📹 Join Meeting
                              </a>
                            )}
                          </div>
                        </div>
                        {apt.status === 'PENDING' && (
                          <div className="mt-4 flex gap-2">
                            <button onClick={() => handleUpdateAppointment(apt.id, 'CONFIRMED')} className="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700">Approve</button>
                            <button onClick={() => handleUpdateAppointment(apt.id, 'REJECTED')} className="bg-red-100 text-red-700 px-3 py-1 rounded text-sm hover:bg-red-200">Reject</button>
                          </div>
                        )}
                      </li>
                    ))
                  )}
                </ul>
              </>
            )}

            {activeTab === 'properties' && (
              <>
                <div className="px-4 py-5 border-b border-gray-200 sm:px-6 flex justify-between items-center bg-gray-50">
                  <h3 className="text-lg leading-6 font-medium text-gray-900">Property Listings</h3>
                  <span className="bg-black text-white text-xs px-2 py-1 rounded-full">
                    {properties.filter(p => p.status === 'PENDING').length} Pending Approval
                  </span>
                </div>
                <ul className="divide-y divide-gray-200">
                  {properties.length === 0 ? (
                    <li className="px-4 py-8 text-center text-gray-500">No properties found.</li>
                  ) : (
                    [...properties].sort((a, b) => {
                      if (a.status === 'PENDING' && b.status !== 'PENDING') return -1;
                      if (a.status !== 'PENDING' && b.status === 'PENDING') return 1;
                      return 0;
                    }).map((prop) => (
                      <li key={prop.id} className="p-6">
                        <div className="flex justify-between items-start">
                          <div>
                            <p className="text-lg font-bold text-gray-900">{prop.title}</p>
                            <p className="text-sm text-gray-600 mt-1">{prop.city} | {prop.property_type}</p>
                            <p className="text-sm text-gray-800 mt-1 font-semibold">Rent: ₹{prop.monthly_rent}/mo</p>
                            <p className="text-sm text-gray-500 mt-2">Owner: {prop.owner_name} ({prop.owner_email})</p>
                          </div>
                          <span className={`px-2 py-1 text-xs font-semibold rounded-full ${prop.status === 'PUBLISHED' ? 'bg-green-100 text-green-800' : prop.status === 'REJECTED' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'}`}>
                            {prop.status}
                          </span>
                        </div>
                        {prop.status === 'PENDING' && (
                          <div className="mt-4 flex gap-2">
                            <button onClick={() => handleUpdatePropertyStatus(prop.id, 'PUBLISHED')} className="bg-green-600 text-white px-4 py-2 rounded text-sm font-medium hover:bg-green-700">Approve & Publish</button>
                            <button onClick={() => handleUpdatePropertyStatus(prop.id, 'REJECTED')} className="bg-red-50 border border-red-200 text-red-700 px-4 py-2 rounded text-sm font-medium hover:bg-red-100">Reject</button>
                          </div>
                        )}
                      </li>
                    ))
                  )}
                </ul>
              </>
            )}

            {(activeTab === 'buyers' || activeTab === 'sellers') && (() => {
              const nonAdminUsers = usersList.filter(u => !u.roles.includes('ADMIN'));
              const listToRender = activeTab === 'buyers'
                ? nonAdminUsers.filter(u => u.roles.includes('BUYER') && !u.roles.includes('SELLER'))
                : nonAdminUsers.filter(u => u.roles.includes('SELLER'));
              
              const title = activeTab === 'buyers' ? 'Buyer Directory' : 'Seller Directory';
              const emptyMsg = activeTab === 'buyers' ? 'No buyers found.' : 'No sellers found.';

              return (
                <>
                  <div className="px-4 py-5 border-b border-gray-200 sm:px-6 flex justify-between items-center bg-gray-50">
                    <h3 className="text-lg leading-6 font-medium text-gray-900">{title}</h3>
                    <span className="bg-black text-white text-xs px-2 py-1 rounded-full">
                      {listToRender.length} {activeTab === 'buyers' ? 'Buyers' : 'Sellers'}
                    </span>
                  </div>
                  
                  <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-gray-50">
                        <tr>
                          <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                          <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                          <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Roles</th>
                          <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                          <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {listToRender.length === 0 ? (
                          <tr>
                            <td colSpan="4" className="px-6 py-4 text-center text-sm text-gray-500">{emptyMsg}</td>
                          </tr>
                        ) : (
                          listToRender.map((usr) => (
                            <tr key={usr.id}>
                              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{usr.full_name}</td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{usr.email}</td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                {usr.roles.map(role => (
                                  <span key={role} className={`inline-block mr-1 px-2 py-0.5 rounded text-xs font-medium 
                                    ${role === 'SELLER' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'}`}>
                                    {role}
                                  </span>
                                ))}
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                {usr.is_active ? <span className="text-green-600 font-semibold">Active</span> : <span className="text-red-600 font-semibold">Inactive</span>}
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                <button 
                                  onClick={() => handleDeleteUser(usr.id, usr.full_name)}
                                  className="text-red-600 hover:text-red-900 bg-red-50 hover:bg-red-100 px-3 py-1 rounded transition"
                                >
                                  Delete
                                </button>
                              </td>
                            </tr>
                          ))
                        )}
                      </tbody>
                    </table>
                  </div>
                </>
              );
            })()}

          </div>
        )}
    </div>
  );
}


