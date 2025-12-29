import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { useAuth } from '../context/AuthContext'
import './CandidateDashboard.css'

const CandidateDashboard = () => {
  const [roles, setRoles] = useState([])
  const [selectedRole, setSelectedRole] = useState('')
  const [currentInterview, setCurrentInterview] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    fetchRoles()
    checkCurrentInterview()
  }, [])

  const fetchRoles = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/roles/')
      setRoles(response.data)
    } catch (error) {
      console.error('Error fetching roles:', error)
    } finally {
      setLoading(false)
    }
  }

  const checkCurrentInterview = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/interviews/current')
      setCurrentInterview(response.data)
    } catch (error) {
      // No interview in progress
      setCurrentInterview(null)
    }
  }

  const startInterview = async () => {
    if (!selectedRole) {
      setError('Please select a job role')
      return
    }

    try {
      setLoading(true)
      const response = await axios.post('http://localhost:8000/api/interviews/start', {
        job_role_id: parseInt(selectedRole)
      })
      
      navigate(`/candidate/interview/${response.data.id}`)
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to start interview')
      setLoading(false)
    }
  }

  const continueInterview = () => {
    if (currentInterview) {
      navigate(`/candidate/interview/${currentInterview.id}`)
    }
  }

  if (loading && !currentInterview) {
    return <div className="loading">Loading...</div>
  }

  return (
    <div className="App">
      <nav className="navbar">
        <h1>Botboss - Candidate Dashboard</h1>
        <div className="user-info">
          <span>Welcome, {user?.username}</span>
          <button onClick={logout}>Logout</button>
        </div>
      </nav>

      <div className="container">
        {currentInterview ? (
          <div className="card">
            <h2>Interview In Progress</h2>
            <p>You have an interview in progress. Continue to complete it.</p>
            <button className="btn btn-primary" onClick={continueInterview}>
              Continue Interview
            </button>
          </div>
        ) : (
          <div className="card">
            <h2>Start New Interview</h2>
            <p>Select a job role to begin your AI interview</p>
            
            <div className="form-group">
              <label>Select Job Role</label>
              <select
                value={selectedRole}
                onChange={(e) => setSelectedRole(e.target.value)}
              >
                <option value="">-- Select a role --</option>
                {roles.map((role) => (
                  <option key={role.id} value={role.id}>
                    {role.title}
                  </option>
                ))}
              </select>
            </div>

            {error && <div className="error">{error}</div>}

            <button
              className="btn btn-primary"
              onClick={startInterview}
              disabled={loading || !selectedRole}
            >
              {loading ? 'Starting...' : 'Start Interview'}
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default CandidateDashboard

