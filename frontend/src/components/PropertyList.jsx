import PropertyCard from './PropertyCard';

function PropertyList({ properties, loading, error }) {
  if (loading) {
    return (
      <div className="max-w-6xl mx-auto px-4 py-12 text-center">
        <p className="text-gray-500 text-lg animate-pulse">Loading properties...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-6xl mx-auto px-4 py-12 text-center">
        <p className="text-red-500 bg-red-50 p-4 rounded border border-red-200">{error}</p>
      </div>
    );
  }

  if (!properties || properties.length === 0) {
    return (
      <div className="max-w-6xl mx-auto px-4 py-12 text-center">
        <div className="bg-white p-8 rounded shadow-sm border border-gray-200">
          <p className="text-gray-600 text-lg">No properties found matching your criteria.</p>
          <p className="text-gray-400 text-sm mt-2">Try adjusting your search filters.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-12">
      <h2 className="text-2xl font-semibold text-gray-800 mb-6">
        Recommended Properties ({properties.length})
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {properties.map((prop) => (
          <PropertyCard key={prop.id} property={prop} />
        ))}
      </div>
    </div>
  );
}

export default PropertyList;
