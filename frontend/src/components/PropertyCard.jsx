import { Link } from 'react-router-dom';

function PropertyCard({ property }) {
  return (
    <Link to={`/properties/${property.id}`} className="block">
      <div className="bg-white rounded-lg shadow-md overflow-hidden border border-gray-200 hover:shadow-lg transition-shadow p-6">
        <div className="flex justify-between items-start mb-2">
          <h3 className="text-xl font-bold text-gray-800 line-clamp-1" title={property.title}>
            {property.title}
          </h3>
          <span className="bg-teal-100 text-teal-800 text-xs px-2 py-1 rounded font-medium">
            {property.property_type}
          </span>
        </div>
        
        <p className="text-sm text-gray-600 flex items-center gap-1 mb-4">
          📍 {property.city}
        </p>

        <div className="flex justify-between items-end border-t border-gray-100 pt-4 mt-2">
          <div>
            <p className="text-xs text-gray-500 uppercase font-semibold">Rent</p>
            <p className="text-xl font-bold text-gray-800">₹{property.monthly_rent}</p>
          </div>
        </div>
      </div>
    </Link>
  );
}

export default PropertyCard;
