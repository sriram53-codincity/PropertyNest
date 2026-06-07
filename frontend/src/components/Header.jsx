import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/AuthContext';

function Header() {
  const { user, logoutUser } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logoutUser();
    navigate('/');
  };

  return (
    <header className="flex justify-between items-center p-6 border-b border-gray-100 max-w-7xl mx-auto w-full bg-white relative z-10">
      <Link to="/" className="flex items-center text-brandRed text-2xl font-bold gap-2">
        <span className="text-3xl text-red-500">❖</span>
        PropertyNest
      </Link>
      
      <div className="hidden md:flex items-center gap-6 text-sm font-medium">
        <Link to="/properties" className="text-gray-600 hover:text-black transition">
          Browse Properties
        </Link>
        
        {user ? (
          <>
            {user.roles?.includes('SELLER') && (
              <Link to="/dashboard?mode=seller&tab=add-property" className="bg-brandRed text-white px-4 py-1.5 rounded-full text-sm hover:bg-red-700 transition shadow-sm font-semibold flex items-center gap-1">
                <span className="text-lg leading-none">+</span> Add Property
              </Link>
            )}
            <Link to="/dashboard" className="text-gray-600 hover:text-black transition font-medium">
              Dashboard
            </Link>
            
            <div className="flex items-center gap-4 border-l border-gray-200 pl-6">
              <span className="text-gray-500">Hi, {user.full_name || user.username}</span>
              <button onClick={handleLogout} className="text-red-500 hover:text-red-700 transition">
                Logout
              </button>
            </div>
          </>
        ) : (
          <div className="flex items-center gap-4 border-l border-gray-200 pl-6">
            <Link to="/login" className="text-gray-500 hover:text-black text-sm font-medium transition">
              Sign In
            </Link>
          </div>
        )}
      </div>
    </header>
  );
}

export default Header;
