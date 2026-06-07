import React from 'react';

function SellerAppointmentsTab({ propertyAppointments, handleAppointmentStatusUpdate }) {
  return (
    <div className="bg-white rounded-lg shadow border border-gray-200 overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-200 bg-gray-50">
        <h2 className="text-xl font-semibold text-gray-800">Property Appointments</h2>
      </div>
      <div className="divide-y divide-gray-200">
        {propertyAppointments.length === 0 ? (
          <p className="p-6 text-gray-500">No appointments scheduled.</p>
        ) : (
          propertyAppointments.map((apt) => (
            <div key={apt.id} className="p-6 flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-brandRed">{apt.preferred_date} at {apt.preferred_time}</h3>
                <p className="text-sm text-gray-600 mt-1">Property ID: {apt.property_id || 'N/A'}</p>
                <p className="text-sm text-gray-600 mt-1">{apt.full_name} | {apt.email} | {apt.phone}</p>
                <p className="text-sm text-gray-600 mt-1">Status: <span className={`font-bold ${apt.status === 'CONFIRMED' ? 'text-green-600' : apt.status === 'REJECTED' ? 'text-red-600' : 'text-yellow-600'}`}>{apt.status}</span></p>
                {apt.additional_notes && <p className="text-sm text-gray-600 mt-2 bg-gray-50 p-2 rounded border whitespace-pre-wrap">{apt.additional_notes}</p>}
              </div>
              <div className="flex gap-2">
                {apt.status === 'PENDING' && (
                  <>
                    <button onClick={() => handleAppointmentStatusUpdate(apt.id, 'CONFIRMED')} className="bg-green-600 text-white px-4 py-2 rounded text-sm font-medium hover:bg-green-700 transition">Confirm</button>
                    <button onClick={() => handleAppointmentStatusUpdate(apt.id, 'REJECTED')} className="bg-red-100 text-red-700 px-4 py-2 rounded text-sm font-medium hover:bg-red-200 transition">Reject</button>
                  </>
                )}
                {(apt.status === 'CONFIRMED' || apt.status === 'APPROVED') && (
                  <a href={`https://meet.jit.si/PropertyNest_${apt.id}`} target="_blank" rel="noopener noreferrer" className="bg-blue-600 text-white px-4 py-2 rounded text-sm font-medium hover:bg-blue-700 transition shadow-sm">
                    📹 Join Meeting
                  </a>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default SellerAppointmentsTab;
