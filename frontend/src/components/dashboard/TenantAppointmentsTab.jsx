import React from 'react';

function TenantAppointmentsTab({ myAppointments }) {
  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">My Appointments</h2>
      {myAppointments.length === 0 ? <p className="text-gray-500">No appointments found.</p> : (
        <ul className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {myAppointments.map(app => (
          <li key={app.id} className="p-4 border rounded shadow-sm bg-white">
            <p className="font-medium text-brandRed mb-2">{app.preferred_date} at {app.preferred_time}</p>
            <p className="text-sm mb-1"><span className="font-semibold">Purpose:</span> {app.purpose.replace('_', ' ')}</p>
            <p className="text-sm mb-1"><span className="font-semibold">Status:</span> {app.status}</p>
            {(app.status === 'CONFIRMED' || app.status === 'APPROVED') && (
              <div className="mt-3">
                <a href={`https://meet.jit.si/PropertyNest_${app.id}`} target="_blank" rel="noopener noreferrer" className="bg-blue-600 text-white px-3 py-1.5 rounded text-sm font-medium hover:bg-blue-700 transition shadow-sm inline-block">
                  📹 Join Meeting
                </a>
              </div>
            )}
            {app.additional_notes && <p className="text-sm text-gray-600 mt-2 italic whitespace-pre-wrap">{app.additional_notes}</p>}
          </li>
        ))}
      </ul>
      )}
    </div>
  );
}

export default TenantAppointmentsTab;
