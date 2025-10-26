import React from 'react';
import Header from './Header';

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div>
      <Header />
      <main className='w-full'>{children}</main>
    </div>
  );
};

export default Layout;
