import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Bars3Icon } from '@heroicons/react/24/outline';
import Tooltip from '@/components/ui/Tooltip';

const Header: React.FC = () => {
  const [isProfileOpen, setProfileOpen] = useState(false);
  const [isMenuOpen, setMenuOpen] = useState(false);

  const toggleProfileMenu = () => setProfileOpen(!isProfileOpen);
  const closeProfileMenu = () => setProfileOpen(false);
  const toggleMenu = () => setMenuOpen(!isMenuOpen);
  const closeMenu = () => setMenuOpen(false);

  // Закрытие профиля по клику вне меню или по Escape
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      const profileMenu = document.getElementById('profile-menu');
      if (profileMenu && !profileMenu.contains(event.target as Node)) {
        closeProfileMenu();
      }
    };

    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        closeProfileMenu();
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    document.addEventListener('keydown', handleEscape);

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleEscape);
    };
  }, []);

  return (
    <header className="flex flex-col md:flex-row justify-between items-center p-4 bg-white shadow-md">
      <div className="flex items-center justify-between w-full md:w-auto">
        <Link to="/" className="text-xl font-bold">
          PriceAggregator — B2B Сравнение
        </Link>
        <Tooltip text="Меню">
          <button onClick={toggleMenu} className="md:hidden">
            <Bars3Icon className="h-6 w-6" />
          </button>
        </Tooltip>
        <Tooltip text="Профиль">
          <button
            onClick={toggleProfileMenu}
            className="flex items-center md:hidden"
          >
            Профиль ▾
          </button>
        </Tooltip>
      </div>
      <div className={`relative ${isMenuOpen ? 'block' : 'hidden'} md:block`}>
        <nav className="flex flex-col md:flex-row md:justify-center space-y-2 md:space-y-0 md:space-x-4 p-4 bg-gray-100 md:bg-transparent">
          <Link to="/compare-pages" className="block" onClick={closeMenu}>
            Сравнить две страницы
          </Link>
          <Link to="/compare-products" className="block" onClick={closeMenu}>
            Сравнить несколько товаров
          </Link>
          <Link to="/mass-parsing" className="block" onClick={closeMenu}>
            Массовый парсинг каталога
          </Link>
          <Tooltip text="Профиль">
            <button
              onClick={toggleProfileMenu}
              className="hidden md:flex items-center"
            >
              Профиль ▾
            </button>
          </Tooltip>
        </nav>
      </div>
      {isProfileOpen && (
        <div
          id="profile-menu"
          className="absolute right-0 mt-2 w-48 bg-white border rounded shadow-lg"
        >
          <ul>
            <li onClick={closeProfileMenu}>
              <Link to="/profile">Профиль</Link>
            </li>
            <li onClick={closeProfileMenu}>
              <Link to="/settings">Настройки</Link>
            </li>
            <li onClick={closeProfileMenu}>
              <Link to="/logout">Выход</Link>
            </li>
          </ul>
        </div>
      )}
    </header>
  );
};

export default Header;
