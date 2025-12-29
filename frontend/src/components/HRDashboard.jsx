import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { useAuth } from '../context/AuthContext'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import './HRDashboard.css'

const HRDashboard = () => {
  const [candidates, setCandidates] = useState([])
  const [statistics, setStatistics] = useState(null)
  const [selectedCandidate, setSelectedCandidate] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  useEffect(() => {
    fetchCandidates()
    fetchStatistics()
  }, [])

  const fetchCandidates = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/dashboard/candidates`)
      setCandidates(response.data)
    } catch (error) {
      console.error('Error fetching candidates:', error)
      setError('Failed to load candidates')
    } finally {
      setLoading(false)
    }
  }

  const fetchStatistics = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/dashboard/statistics`)
      setStatistics(response.data)
    } catch (error) {
      console.error('Error fetching statistics:', error)
    }
  }

  const viewCandidateDetails = async (candidateId, interviewId) => {
    try {
      const response = await axios.get(
        `${API_BASE_URL}/api/dashboard/candidates/${candidateId}/interview/${interviewId}`
      )
      setSelectedCandidate(response.data)
    } catch (error) {
      setError('Failed to load candidate details')
    }
  }

  const closeDetails = () => {
    setSelectedCandidate(null)
  }

  // Prepare chart data
  const chartData = candidates.slice(0, 10).map(candidate => ({
    name: candidate.candidate_username,
    score: candidate.final_score
  }))

  if (loading) {
    return <div className="loading">Loading dashboard...</div>
  }

  return (
    <div className="App">
      <nav className="navbar">
        <h1>Botboss - HR Dashboard</h1>
        <div className="user-info">
          <span>Welcome, {user?.username}</span>
          <button onClick={logout}>Logout</button>
        </div>
      </nav>

      <div className="container">
        {error && <div className="error">{error}</div>}

        {/* Statistics Cards */}
        {statistics && (
          <div className="stats-grid">
            <div className="stat-card">
              <h3>Total Interviews</h3>
              <p className="stat-value">{statistics.total_interviews}</p>
            </div>
            <div className="stat-card">
              <h3>Completed</h3>
              <p className="stat-value">{statistics.completed_interviews}</p>
            </div>
            <div className="stat-card">
              <h3>In Progress</h3>
              <p className="stat-value">{statistics.in_progress_interviews}</p>
            </div>
            <div className="stat-card">
              <h3>Total Candidates</h3>
              <p className="stat-value">{statistics.total_candidates}</p>
            </div>
            <div className="stat-card">
              <h3>Average Score</h3>
              <p className="stat-value">{statistics.average_final_score}/10</p>
            </div>
          </div>
        )}

        {/* Chart */}
        {chartData.length > 0 && (
          <div className="card">
            <h2>Top Candidates Performance</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis domain={[0, 10]} />
                <Tooltip />
                <Legend />
                <Bar dataKey="score" fill="#007bff" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Candidates Table */}
        <div className="card">
          <h2>Candidates List</h2>
          {candidates.length === 0 ? (
            <p>No candidates have completed interviews yet.</p>
          ) : (
            <div className="table-container">
              <table className="candidates-table">
                <thead>
                  <tr>
                    <th>Candidate</th>
                    <th>Email</th>
                    <th>Job Role</th>
                    <th>Final Score</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {candidates.map((candidate) => (
                    <tr key={candidate.interview_id}>
                      <td>{candidate.candidate_username}</td>
                      <td>{candidate.candidate_email}</td>
                      <td>{candidate.job_role}</td>
                      <td>
                        <span className={`score-badge ${candidate.final_score >= 7 ? 'high' : candidate.final_score >= 5 ? 'medium' : 'low'}`}>
                          {candidate.final_score}/10
                        </span>
                      </td>
                      <td>
                        <span className={`status-badge ${candidate.status}`}>
                          {candidate.status}
                        </span>
                      </td>
                      <td>
                        <button
                          className="btn btn-primary btn-sm"
                          onClick={() => viewCandidateDetails(candidate.candidate_id, candidate.interview_id)}
                        >
                          View Details
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Candidate Details Modal */}
        {selectedCandidate && (
          <div className="modal-overlay" onClick={closeDetails}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <div className="modal-header">
                <h2>Interview Details - {selectedCandidate.candidate.username}</h2>
                <button className="close-btn" onClick={closeDetails}>×</button>
              </div>
              <div className="modal-body">
                <div className="candidate-info">
                  <p><strong>Email:</strong> {selectedCandidate.candidate.email}</p>
                  <p><strong>Job Role:</strong> {selectedCandidate.job_role}</p>
                  <p><strong>Status:</strong> {selectedCandidate.interview.status}</p>
                  <p><strong>Completed:</strong> {new Date(selectedCandidate.interview.completed_at).toLocaleString()}</p>
                </div>

                <div className="scores-section">
                  <h3>Overall Scores</h3>
                  <div className="scores-grid">
                    <div className="score-item">
                      <label>Technical</label>
                      <div className="score-value">{selectedCandidate.interview.technical_score}/10</div>
                    </div>
                    <div className="score-item">
                      <label>Clarity</label>
                      <div className="score-value">{selectedCandidate.interview.clarity_score}/10</div>
                    </div>
                    <div className="score-item">
                      <label>Relevance</label>
                      <div className="score-value">{selectedCandidate.interview.relevance_score}/10</div>
                    </div>
                    <div className="score-item">
                      <label>Sentiment</label>
                      <div className="score-value">{selectedCandidate.interview.sentiment_score}/10</div>
                    </div>
                    <div className="score-item final">
                      <label>Final Score</label>
                      <div className="score-value">{selectedCandidate.interview.final_score}/10</div>
                    </div>
                  </div>
                </div>

                <div className="questions-section">
                  <h3>Questions & Responses</h3>
                  {selectedCandidate.questions_and_responses.map((item, index) => (
                    <div key={item.question_id} className="question-response-item">
                      <div className="question">
                        <strong>Q{item.question_number}:</strong> {item.question_text}
                      </div>
                      {item.response ? (
                        <div className="response">
                          <strong>Answer:</strong>
                          <p>{item.response.response_text}</p>
                          <div className="response-scores">
                            <span>Technical: {item.response.technical_score}/10</span>
                            <span>Clarity: {item.response.clarity_score}/10</span>
                            <span>Relevance: {item.response.relevance_score}/10</span>
                            <span>Sentiment: {item.response.sentiment_score}/10</span>
                          </div>
                        </div>
                      ) : (
                        <div className="response">No response submitted</div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default HRDashboard

