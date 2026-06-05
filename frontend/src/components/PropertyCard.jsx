import { Link } from 'react-router-dom';

function PropertyCard({ property }) {
  // Use a fallback image if no images exist
  const imageUrl = property.images && property.images.length > 0 
    ? `http://localhost:8000${property.images[0]}` 
    : 'https://via.placeholder.com/400x250?text=No+Image+Available';

  return (
    <Link to={`/properties/${property.id}`} className="block">
      <div className="bg-white rounded-lg shadow-md overflow-hidden border border-gray-200 hover:shadow-lg transition-shadow">
        <img src={imageUrl} alt={property.title} className="w-full h-48 object-cover" />
        <div className="p-4">
          <div className="flex justify-between items-start mb-2">
            <h3 className="text-lg font-bold text-gray-800 line-clamp-1" title={property.title}>
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
              <p className="text-xl font-bold text-gray-800">₹{property.rent}</p>
            </div>
            {property.deposit && (
              <div className="text-right">
                <p className="text-xs text-gray-500 uppercase font-semibold">Deposit</p>
                <p className="text-sm font-semibold text-gray-700">₹{property.deposit}</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </Link>
  );
}

export default PropertyCard;
