import { useState, useEffect } from 'react';

// This is a placeholder for actual authentication logic
// In a real app, you would implement proper JWT handling and API calls

interface User {
  id: string;
  email: string;
  name: string;
}

interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  loading: boolean;
}

export const useAuth = () => {
  const [authState, setAuthState] = useState<AuthState>({
    isAuthenticated: false,
    user: null,
    loading: true,
  });

  useEffect(() => {
    // Check if user is logged in (e.g., by verifying JWT in localStorage)
    const checkAuth = async () => {
      try {
        const token = localStorage.getItem('auth_token');
        
        if (token) {
          // In a real app, you would verify the token with your backend
          // For now, we'll just assume it's valid if it exists
          
          // Mock user data
          const user = {
            id: '1',
            email: 'user@example.com',
            name: 'Test User',
          };
          
          setAuthState({
            isAuthenticated: true,
            user,
            loading: false,
          });
        } else {
          setAuthState({
            isAuthenticated: false,
            user: null,
            loading: false,
          });
        }
      } catch (error) {
        console.error('Authentication error:', error);
        setAuthState({
          isAuthenticated: false,
          user: null,
          loading: false,
        });
      }
    };
    
    checkAuth();
  }, []);

  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      // In a real app, you would make an API call to your backend
      // For now, we'll just simulate a successful login with any credentials
      
      // Mock successful login
      const user = {
        id: '1',
        email,
        name: 'Test User',
      };
      
      // Store token in localStorage
      localStorage.setItem('auth_token', 'mock_jwt_token');
      
      setAuthState({
        isAuthenticated: true,
        user,
        loading: false,
      });
      
      return true;
    } catch (error) {
      console.error('Login error:', error);
      return false;
    }
  };

  const register = async (name: string, email: string, password: string): Promise<boolean> => {
    try {
      // In a real app, you would make an API call to your backend
      // For now, we'll just simulate a successful registration
      
      // Mock successful registration
      const user = {
        id: '1',
        email,
        name,
      };
      
      // Store token in localStorage
      localStorage.setItem('auth_token', 'mock_jwt_token');
      
      setAuthState({
        isAuthenticated: true,
        user,
        loading: false,
      });
      
      return true;
    } catch (error) {
      console.error('Registration error:', error);
      return false;
    }
  };

  const logout = () => {
    // Remove token from localStorage
    localStorage.removeItem('auth_token');
    
    setAuthState({
      isAuthenticated: false,
      user: null,
      loading: false,
    });
  };

  return {
    ...authState,
    login,
    register,
    logout,
  };
};