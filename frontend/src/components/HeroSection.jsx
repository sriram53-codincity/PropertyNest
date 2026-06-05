function HeroSection() {
  return (
    <div className="text-center pt-16 pb-8 bg-gray-50 flex flex-col items-center">
      <h1 className="text-3xl md:text-4xl text-gray-600 mb-6">
        World's Largest NoBrokerage Property Site
      </h1>
      
      <div className="bg-orange-50 border border-orange-200 rounded px-6 py-3 flex items-center justify-center gap-4 shadow-sm inline-block">
        <span className="flex items-center gap-2 text-gray-700 font-medium">
          🚚 Packers And Movers
        </span>
        <span className="text-gray-300">|</span>
        <span className="flex items-center gap-2 text-brandRed font-medium">
          % Lowest Prices
        </span>
      </div>
    </div>
  );
}

export default HeroSection;
