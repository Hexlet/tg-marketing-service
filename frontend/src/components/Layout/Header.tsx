import React, { useState, useEffect } from 'react';
import { Bars3Icon } from '@heroicons/react/24/outline';
import Tooltip from '@/components/ui/Tooltip';
import AppLink from '../ui/AppLink';

const Header: React.FC = () => {
  const [isProfileOpen, setProfileOpen] = useState(false);
  const [isMenuOpen, setMenuOpen] = useState(false);

  const menuItems = [
    { to: '/compare-pages', label: 'Сравнить две страницы' },
    { to: '/compare-products', label: 'Сравнить несколько товаров' },
    { to: '/mass-parsing', label: 'Массовый парсинг каталога' },
    { to: '/channels', label: 'Каталог каналов' },
    { to: '/auth', label: 'Войти' },
  ];
  const profileMenuItems = [
    { to: '/profile', label: 'Профиль' },
    { to: '/settings', label: 'Настройки' },
    { to: '/logout', label: 'Выход' },
  ];

  const toggleProfileMenu = () => setProfileOpen(!isProfileOpen);
  const closeProfileMenu = () => setProfileOpen(false);
  const toggleMenu = () => setMenuOpen(!isMenuOpen);
  const closeMenu = () => setMenuOpen(false);

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
    <header className="w-full bg-white border-1">
      <div className="w-full mx-auto max-w-7xl flex">
        <div className="w-full px-4 flex items-center justify-between">
          <AppLink
            to="/"
            className="text-xl font-bold"
            variant="text"
            scheme="default"
          >
            PriceAggregator — B2B Сравнение
          </AppLink>
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
            {menuItems.map(({ to, label }) => (
              <AppLink
                key={to}
                to={to}
                className="block"
                onClick={closeMenu}
                variant="text"
                scheme="default"
              >
                {label}
              </AppLink>
            ))}
          </nav>
        </div>
        {isProfileOpen && (
          <div
            id="profile-menu"
            className="absolute right-0 mt-2 bg-white border rounded shadow-lg"
          >
            <ul>
              {profileMenuItems.map(({ to, label }) => (
                <li>
                  <AppLink key={to} to={to}>
                    {label}
                  </AppLink>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;
