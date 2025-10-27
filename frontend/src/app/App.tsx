import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import Layout from '@/components/Layout/Layout';
import { renderRoutes } from './routes';

const App: React.FC = () => {
  return (
    <Router>
      <Layout>
          {renderRoutes()}
      </Layout>
    </Router>
  );
};

export default App;
