import { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import Header from "../components/Header";
import AdminDashboard from "./AdminDashboard";
import api from "../services/api";
import { useAuth } from "../hooks/AuthContext";
import TenantApplicationsTab from "../components/dashboard/TenantApplicationsTab";
import TenantAppointmentsTab from "../components/dashboard/TenantAppointmentsTab";
import TenantLeasesTab from "../components/dashboard/TenantLeasesTab";
import TenantMaintenanceTab from "../components/dashboard/TenantMaintenanceTab";
import TenantSellerRequestsTab from "../components/dashboard/TenantSellerRequestsTab";
import SellerApplicationsTab from "../components/dashboard/SellerApplicationsTab";
import SellerAppointmentsTab from "../components/dashboard/SellerAppointmentsTab";
import SellerLeasesTab from "../components/dashboard/SellerLeasesTab";
import SellerMaintenanceTab from "../components/dashboard/SellerMaintenanceTab";
import SellerPropertiesTab from "../components/dashboard/SellerPropertiesTab";
import AddPropertyTab from "../components/dashboard/AddPropertyTab";

function Dashboard() {
  const { user, loading: authLoading } = useAuth();
  
  // Tenant/Buyer States
  const [myApplications, setMyApplications] = useState([]);
  const [myAppointments, setMyAppointments] = useState([]);
  const [leases, setLeases] = useState([]);
  const [maintenance, setMaintenance] = useState([]);
  const [sellerLeases, setSellerLeases] = useState([]);
  const [sellerMaintenance, setSellerMaintenance] = useState([]);
  const [sellerRequests, setSellerRequests] = useState([]);
  
  // Seller States
  const [receivedApplications, setReceivedApplications] = useState([]);
  const [propertyAppointments, setPropertyAppointments] = useState([]);
  const [myListedProperties, setMyListedProperties] = useState([]);

  const [loading, setLoading] = useState(true);
  
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const initialMode = queryParams.get('mode') || 'tenant';
  const initialTab = queryParams.get('tab') || (initialMode === 'seller' ? 'received-applications' : 'applications');

  const [activeTab, setActiveTab] = useState(initialTab);
  const [viewMode, setViewMode] = useState(initialMode); // 'tenant' or 'owner' or 'admin'

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const mode = params.get('mode');
    const tab = params.get('tab');
    if (mode) setViewMode(mode);
    if (tab) setActiveTab(tab);
  }, [location.search]);

  useEffect(() => {
    if (user) {
      fetchTenantData();
      if (user.roles?.includes('SELLER')) {
        fetchSellerData();
      }
    } else {
      setLoading(false);
    }
  }, [user]);

  const fetchTenantData = () => {
    setLoading(true);
    
    api.get('/applications/')
      .then(res => {
        const appData = res.data;
        setMyApplications(Array.isArray(appData) ? appData.filter(app => String(app.applicant_id) === String(user.id)) : []);
      }).catch(console.error);

    api.get('/appointments/mine')
      .then(res => {
        const aptData = res.data;
        setMyAppointments(Array.isArray(aptData) ? aptData : []);
      }).catch(console.error);

    api.get('/leases/me')
      .then(res => {
        const leaseData = res.data;
        setLeases(Array.isArray(leaseData) ? leaseData.filter(l => String(l.tenant_id) === String(user.id)) : []);
      }).catch(console.error);

    api.get('/maintenance/')
      .then(res => {
        const maintData = res.data;
        setMaintenance(Array.isArray(maintData) ? maintData.filter(m => String(m.tenant_id) === String(user.id)) : []);
      }).catch(console.error);

    api.get('/seller-requests/mine')
      .then(res => {
        const reqData = res.data;
        setSellerRequests(Array.isArray(reqData) ? reqData : []);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  const fetchSellerData = () => {
    api.get('/applications/')
      .then(res => {
        const appData = res.data;
        setReceivedApplications(Array.isArray(appData) ? appData.filter(app => String(app.applicant_id) !== String(user.id)) : []);
      }).catch(console.error);

    api.get('/appointments/for-owner')
      .then(res => {
        const aptData = res.data;
        setPropertyAppointments(Array.isArray(aptData) ? aptData : aptData.items || []);
      }).catch(console.error);

    api.get('/leases/me')
      .then(res => {
        const leaseData = res.data;
        setSellerLeases(Array.isArray(leaseData) ? leaseData.filter(l => String(l.tenant_id) !== String(user.id)) : []);
      }).catch(console.error);

    api.get('/maintenance/')
      .then(res => {
        const maintData = res.data;
        setSellerMaintenance(Array.isArray(maintData) ? maintData.filter(m => String(m.tenant_id) !== String(user.id)) : []);
      }).catch(console.error);

    api.get('/properties/mine')
      .then(res => {
        const propData = res.data;
        setMyListedProperties(Array.isArray(propData) ? propData : propData.items || []);
      }).catch(console.error);
  };

  // --- Seller Actions ---
  const handleStatusUpdate = async (id, status) => {
    let reason = null;
    if (status === 'REJECTED') {
      reason = window.prompt("Please provide a reason for rejection:");
      if (!reason) return; // User cancelled
    }
    try {
      await updateApplicationStatus(id, status, reason);
      fetchTenantData();
      if (user.roles?.includes('SELLER')) fetchSellerData();
    } catch (err) {
      alert("Failed to update status.");
    }
  };

  const handleAppointmentStatusUpdate = async (id, status) => {
    try {
      await updateAppointmentStatus(id, status);
      fetchSellerData();
    } catch (err) {
      alert("Failed to update appointment status.");
    }
  };

  const handleMaintenanceStatusUpdate = async (id, status) => {
    let comment = null;
    if (status === 'RESOLVED' || status === 'CLOSED' || status === 'IN_PROGRESS') {
      comment = window.prompt(`Please provide a comment for marking as ${status}:`);
      if (comment === null) return; // User cancelled
    }
    try {
      await updateMaintenanceRequestStatus(id, status, comment);
      fetchTenantData();
      if (user.roles?.includes('SELLER')) fetchSellerData();
    } catch (err) {
      alert("Failed to update maintenance request status.");
    }
  };

  const handleMarkAsSold = async (id) => {
    try {
      await updateProperty(id, { is_available: false });
      fetchSellerData();
    } catch (err) {
      alert("Failed to mark as sold.");
    }
  };

  const handleMarkAsAvailable = async (id) => {
    try {
      await updateProperty(id, { is_available: true });
      fetchSellerData();
    } catch (err) {
      alert("Failed to mark as available.");
    }
  };

  const handleDeleteProperty = async (id) => {
    if (window.confirm("Are you sure you want to delete this property?")) {
      try {
        await deleteProperty(id);
        fetchSellerData();
      } catch (err) {
        alert("Failed to delete property.");
      }
    }
  };

  const handleCreateProperty = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const images = formData.getAll('images');
    formData.delete('images');
    
    const propertyData = {
      title: formData.get('title'),
      description: formData.get('description'),
      city: formData.get('city'),
      property_type: formData.get('property_type').toUpperCase(),
      bedrooms: parseInt(formData.get('bedrooms')),
      monthly_rent: parseFloat(formData.get('rent')),
      deposit: parseFloat(formData.get('deposit')) || 0,
      address: formData.get('address'),
      amenities: formData.get('amenities').split(',').map(a => a.trim()),
    };

    try {
      const newProp = await createProperty(propertyData);
      
      if (images && images.length > 0 && images[0].name) {
        const imageForm = new FormData();
        images.forEach(img => imageForm.append('images', img));
        await uploadPropertyImages(newProp.id, imageForm);
      }
      
      alert('Property created successfully!');
      e.target.reset();
      fetchSellerData();
    } catch (err) {
      console.error(err);
      alert('Failed to create property.');
    }
  };

  // --- Tenant Actions ---
  const handleMaintenanceSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    try {
      await createMaintenanceRequest(data);
      fetchTenantData();
      e.target.reset();
      alert('Maintenance request submitted successfully.');
    } catch (err) {
      alert('Error submitting maintenance request.');
    }
  };

  const handleCreateLease = async (applicationId) => {
    try {
      await createLease({ application_id: String(applicationId) });
      alert('Lease created successfully!');
      fetchTenantData();
      if (user.roles?.includes('SELLER')) fetchSellerData();
      setActiveTab('leases');
    } catch (err) {
      const detail = err.response?.data?.detail;
      const msg = typeof detail === 'object' ? JSON.stringify(detail) : detail;
      alert(msg || 'Failed to create lease.');
    }
  };

  if (authLoading || loading) return <div className="p-12 text-center text-gray-500">Loading Dashboard...</div>;
  if (!user) {
    return <div className="p-12 text-center text-red-500">Access Denied. Please log in.</div>;
  }

  const isSeller = user.roles?.includes('SELLER');

  const tenantTabs = [
    { id: 'applications', label: 'My Applications' },
    { id: 'leases', label: 'Leases' },
    { id: 'maintenance', label: 'Maintenance' }
  ];

  const sellerTabs = [
    { id: 'received-applications', label: 'Received Applications' },
    { id: 'seller-leases', label: 'Leases' },
    { id: 'seller-maintenance', label: 'Maintenance' },
    { id: 'my-listed-properties', label: 'My Listed Properties' },
    { id: 'add-property', label: 'Add Property' }
  ];

  const currentTabs = viewMode === 'tenant' ? tenantTabs : sellerTabs;
  
  const displayLeases = viewMode === 'tenant' ? leases : sellerLeases;
  const displayMaintenance = viewMode === 'tenant' ? maintenance : sellerMaintenance;

  return (
    <div className="min-h-screen bg-gray-50 font-sans">
      <Header />
      <div className="max-w-7xl mx-auto p-6 mt-4">
        
        <div className="flex flex-col md:flex-row md:items-center justify-between mb-8 gap-4">
          <h1 className="text-3xl font-bold text-gray-900">
            {viewMode === 'tenant' ? 'My Dashboard' : viewMode === 'seller' ? 'Owner Dashboard' : 'Admin Dashboard'}
          </h1>

          <div className="flex bg-white rounded-md shadow-sm border border-gray-200 p-1">
            <button 
              onClick={() => {
                setViewMode('tenant');
                setActiveTab('applications');
              }}
              className={`px-4 py-2 rounded text-sm font-medium transition ${viewMode === 'tenant' ? 'bg-brandRed text-white' : 'text-gray-600 hover:bg-gray-50'}`}
            >
              Renting Mode
            </button>
            {isSeller && (
              <button 
                onClick={() => {
                  setViewMode('seller');
                  setActiveTab('received-applications');
                }}
                className={`px-4 py-2 rounded text-sm font-medium transition ${viewMode === 'seller' ? 'bg-brandRed text-white' : 'text-gray-600 hover:bg-gray-50'}`}
              >
                Selling Mode
              </button>
            )}
            {user?.roles?.includes('ADMIN') && (
              <button 
                onClick={() => {
                  setViewMode('admin');
                  setActiveTab('requests');
                }}
                className={`px-4 py-2 rounded text-sm font-medium transition ${viewMode === 'admin' ? 'bg-brandRed text-white' : 'text-gray-600 hover:bg-gray-50'}`}
              >
                Admin Mode
              </button>
            )}
          </div>
        </div>

        {viewMode === 'admin' ? (
          <AdminDashboard />
        ) : (
          <>
            <div className="flex gap-4 mb-8 border-b border-gray-200 pb-1 overflow-x-auto">
              {currentTabs.map(tab => (
                <button 
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`px-4 py-2.5 font-medium whitespace-nowrap transition-colors relative ${
                    activeTab === tab.id 
                      ? 'text-brandRed' 
                      : 'text-gray-500 hover:text-gray-800'
                  }`}
                >
                  {tab.label}
                  {activeTab === tab.id && (
                    <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-brandRed rounded-t-md"></div>
                  )}
                </button>
              ))}
            </div>

            <div>
              {/* Tenant Tabs */}
              {activeTab === 'applications' && <TenantApplicationsTab myApplications={myApplications} />}
              {activeTab === 'my-appointments' && <TenantAppointmentsTab myAppointments={myAppointments} />}
              {activeTab === 'leases' && <TenantLeasesTab leases={leases} />}
              {activeTab === 'maintenance' && <TenantMaintenanceTab maintenance={maintenance} leases={leases} handleMaintenanceSubmit={handleMaintenanceSubmit} />}
              {activeTab === 'seller-requests' && <TenantSellerRequestsTab sellerRequests={sellerRequests} />}

              {/* Seller Tabs */}
              {activeTab === 'received-applications' && isSeller && (
                <SellerApplicationsTab 
                  receivedApplications={receivedApplications} 
                  handleStatusUpdate={handleStatusUpdate} 
                  handleCreateLease={handleCreateLease} 
                />
              )}
              {activeTab === 'property-appointments' && isSeller && (
                <SellerAppointmentsTab 
                  propertyAppointments={propertyAppointments} 
                  handleAppointmentStatusUpdate={handleAppointmentStatusUpdate} 
                />
              )}
              {activeTab === 'seller-leases' && isSeller && (
                <SellerLeasesTab sellerLeases={sellerLeases} />
              )}
              {activeTab === 'seller-maintenance' && isSeller && (
                <SellerMaintenanceTab 
                  sellerMaintenance={sellerMaintenance} 
                  handleMaintenanceStatusUpdate={handleMaintenanceStatusUpdate} 
                />
              )}
              {activeTab === 'my-listed-properties' && isSeller && (
                <SellerPropertiesTab 
                  myListedProperties={myListedProperties} 
                  handleMarkAsSold={handleMarkAsSold} 
                  handleMarkAsAvailable={handleMarkAsAvailable} 
                  handleDeleteProperty={handleDeleteProperty} 
                />
              )}
              {activeTab === 'add-property' && isSeller && (
                <AddPropertyTab handleCreateProperty={handleCreateProperty} />
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
