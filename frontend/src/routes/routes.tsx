import React from 'react';
import { Route, Routes } from 'react-router-dom';
import Home from '../components/pages/Home';
import ComparePages from '../components/pages/ComparePages';
import CompareProducts from '../components/pages/CompareProducts';
import MassParsing from '../components/pages/MassParsing';
import Auth from '@/components/pages/Auth';
import Profile from '@/pages/profile/index';

const routes = [
  { path: '/', element: <Home /> },
  { path: '/compare-pages', element: <ComparePages /> },
  { path: '/compare-products', element: <CompareProducts /> },
  { path: '/mass-parsing', element: <MassParsing /> },
  { path: '/auth', element: <Auth /> },
  { path: '/profile', element: <Profile /> },
];

export const renderRoutes = (): React.ReactNode => {
  return (
    <Routes>
      {routes.map((route, index) => (
        <Route
          key={index}
          path={route.path}
          element={route.element}
        />
      ))}
    </Routes>
  );
};

export default routes;
