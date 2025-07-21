import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import Register from './pages/Register';
import JobSearch from './pages/JobSearch';
import ApplicationManager from './pages/ApplicationManager';
import DocumentGenerator from './pages/DocumentGenerator';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import './styles/App.css';

// Create a theme instance
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 500,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 500,
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 500,
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/" element={<Layout />}>
            <Route index element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } />
            <Route path="job-search" element={
              <ProtectedRoute>
                <JobSearch />
              </ProtectedRoute>
            } />
            <Route path="applications" element={
              <ProtectedRoute>
                <ApplicationManager />
              </ProtectedRoute>
            } />
            <Route path="documents" element={
              <ProtectedRoute>
                <DocumentGenerator />
              </ProtectedRoute>
            } />
          </Route>
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;