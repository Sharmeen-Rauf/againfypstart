import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Login from './components/Login'
import CandidateDashboard from './components/CandidateDashboard'
import Interview from './components/Interview'
import HRDashboard from './components/HRDashboard'
import { AuthProvider, useAuth } from './context/AuthContext'
import './App.css'

const PrivateRoute = ({ children, requiredRole }) => {
  const { user, loading } = useAuth()

  if (loading) {
    return <div className="loading">Loading...</div>
  }

  if (!user) {
    return <Navigate to="/login" />
  }

  if (requiredRole && user.role !== requiredRole) {
    return <Navigate to={user.role === 'hr' ? '/hr/dashboard' : '/candidate/dashboard'} />
  }

  return children
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route 
            path="/candidate/dashboard" 
            element={
              <PrivateRoute requiredRole="candidate">
                <CandidateDashboard />
              </PrivateRoute>
            } 
          />
          <Route 
            path="/candidate/interview/:interviewId" 
            element={
              <PrivateRoute requiredRole="candidate">
                <Interview />
              </PrivateRoute>
            } 
          />
          <Route 
            path="/hr/dashboard" 
            element={
              <PrivateRoute requiredRole="hr">
                <HRDashboard />
              </PrivateRoute>
            } 
          />
          <Route path="/" element={<Navigate to="/login" />} />
        </Routes>
      </Router>
    </AuthProvider>
  )
}

export default App

