import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import axios from 'axios'
import { useAuth } from '../context/AuthContext'
import './Interview.css'

const Interview = () => {
  const { interviewId } = useParams()
  const [questions, setQuestions] = useState([])
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [responses, setResponses] = useState({})
  const [currentResponse, setCurrentResponse] = useState('')
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [interviewCompleted, setInterviewCompleted] = useState(false)
  const [finalScores, setFinalScores] = useState(null)
  const { logout } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    fetchQuestions()
    fetchResponses()
  }, [interviewId])

  const fetchQuestions = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/interviews/${interviewId}/questions`)
      setQuestions(response.data)
      
      // Check if interview is completed
      const interviewResponse = await axios.get(`http://localhost:8000/api/interviews/current`)
      if (interviewResponse.data.status === 'completed') {
        setInterviewCompleted(true)
        // Fetch final scores
        try {
          const completeResponse = await axios.post(`http://localhost:8000/api/interviews/${interviewId}/complete`)
          setFinalScores(completeResponse.data.final_scores)
        } catch (e) {
          // Interview already completed, fetch from interview data
          setFinalScores({
            technical_score: interviewResponse.data.technical_score,
            clarity_score: interviewResponse.data.clarity_score,
            relevance_score: interviewResponse.data.relevance_score,
            sentiment_score: interviewResponse.data.sentiment_score,
            final_score: interviewResponse.data.final_score
          })
        }
      }
    } catch (error) {
      console.error('Error fetching questions:', error)
      setError('Failed to load interview questions')
    } finally {
      setLoading(false)
    }
  }

  const fetchResponses = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/interviews/${interviewId}/responses`)
      const responseMap = {}
      response.data.forEach(r => {
        responseMap[r.question_id] = r.response_text
      })
      setResponses(responseMap)
    } catch (error) {
      // No responses yet
    }
  }

  const handleSubmitResponse = async () => {
    if (!currentResponse.trim()) {
      setError('Please provide a response')
      return
    }

    const currentQuestion = questions[currentQuestionIndex]
    setSubmitting(true)
    setError('')

    try {
      await axios.post(`http://localhost:8000/api/interviews/${interviewId}/respond`, {
        question_id: currentQuestion.id,
        response_text: currentResponse
      })

      setResponses({
        ...responses,
        [currentQuestion.id]: currentResponse
      })

      if (currentQuestionIndex < questions.length - 1) {
        setCurrentQuestionIndex(currentQuestionIndex + 1)
        setCurrentResponse('')
      } else {
        // All questions answered, complete interview
        await completeInterview()
      }
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to submit response')
    } finally {
      setSubmitting(false)
    }
  }

  const completeInterview = async () => {
    try {
      const response = await axios.post(`http://localhost:8000/api/interviews/${interviewId}/complete`)
      setFinalScores(response.data.final_scores)
      setInterviewCompleted(true)
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to complete interview')
    }
  }

  const handleSkip = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1)
      setCurrentResponse('')
    }
  }

  const handleNext = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1)
      const nextQuestion = questions[currentQuestionIndex + 1]
      setCurrentResponse(responses[nextQuestion.id] || '')
    }
  }

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1)
      const prevQuestion = questions[currentQuestionIndex - 1]
      setCurrentResponse(responses[prevQuestion.id] || '')
    }
  }

  if (loading) {
    return <div className="loading">Loading interview...</div>
  }

  if (interviewCompleted && finalScores) {
    return (
      <div className="App">
        <nav className="navbar">
          <h1>Botboss - Interview Complete</h1>
          <div className="user-info">
            <button onClick={() => navigate('/candidate/dashboard')}>Back to Dashboard</button>
            <button onClick={logout}>Logout</button>
          </div>
        </nav>

        <div className="container">
          <div className="card completion-card">
            <h2>✅ Interview Completed Successfully!</h2>
            <div className="scores-display">
              <h3>Your Scores:</h3>
              <div className="score-grid">
                <div className="score-item">
                  <label>Technical Score</label>
                  <div className="score-value">{finalScores.technical_score}/10</div>
                </div>
                <div className="score-item">
                  <label>Clarity Score</label>
                  <div className="score-value">{finalScores.clarity_score}/10</div>
                </div>
                <div className="score-item">
                  <label>Relevance Score</label>
                  <div className="score-value">{finalScores.relevance_score}/10</div>
                </div>
                <div className="score-item">
                  <label>Sentiment Score</label>
                  <div className="score-value">{finalScores.sentiment_score}/10</div>
                </div>
                <div className="score-item final">
                  <label>Final Score</label>
                  <div className="score-value">{finalScores.final_score}/10</div>
                </div>
              </div>
            </div>
            <button 
              className="btn btn-primary" 
              onClick={() => navigate('/candidate/dashboard')}
            >
              Back to Dashboard
            </button>
          </div>
        </div>
      </div>
    )
  }

  const currentQuestion = questions[currentQuestionIndex]
  const isAnswered = currentQuestion && responses[currentQuestion.id]
  const answeredCount = Object.keys(responses).length

  return (
    <div className="App">
      <nav className="navbar">
        <h1>Botboss - AI Interview</h1>
        <div className="user-info">
          <span>Question {currentQuestionIndex + 1} of {questions.length}</span>
          <button onClick={logout}>Logout</button>
        </div>
      </nav>

      <div className="container">
        <div className="progress-bar">
          <div 
            className="progress-fill" 
            style={{ width: `${((currentQuestionIndex + 1) / questions.length) * 100}%` }}
          ></div>
        </div>

        <div className="card interview-card">
          <div className="question-header">
            <span className="question-number">Question {currentQuestionIndex + 1} of {questions.length}</span>
            <span className="answered-count">{answeredCount}/{questions.length} answered</span>
          </div>

          <h2 className="question-text">{currentQuestion?.question_text}</h2>

          <div className="form-group">
            <label>Your Response</label>
            <textarea
              value={currentResponse}
              onChange={(e) => setCurrentResponse(e.target.value)}
              placeholder="Type your answer here..."
              rows="8"
            />
          </div>

          {error && <div className="error">{error}</div>}

          <div className="interview-actions">
            <div className="nav-buttons">
              <button
                className="btn btn-secondary"
                onClick={handlePrevious}
                disabled={currentQuestionIndex === 0}
              >
                Previous
              </button>
              {!isAnswered && (
                <button
                  className="btn btn-secondary"
                  onClick={handleSkip}
                  disabled={currentQuestionIndex === questions.length - 1}
                >
                  Skip for Now
                </button>
              )}
              {currentQuestionIndex < questions.length - 1 && (
                <button
                  className="btn btn-secondary"
                  onClick={handleNext}
                  disabled={currentQuestionIndex === questions.length - 1}
                >
                  Next
                </button>
              )}
            </div>

            <button
              className="btn btn-primary"
              onClick={handleSubmitResponse}
              disabled={submitting || !currentResponse.trim()}
            >
              {submitting ? 'Submitting...' : isAnswered ? 'Update Response' : 'Submit Answer'}
            </button>
          </div>

          {answeredCount === questions.length && (
            <div className="completion-prompt">
              <p>All questions answered! Click below to complete the interview.</p>
              <button className="btn btn-success" onClick={completeInterview}>
                Complete Interview
              </button>
            </div>
          )}
        </div>

        <div className="questions-sidebar">
          <h3>Questions</h3>
          <div className="questions-list">
            {questions.map((q, index) => (
              <button
                key={q.id}
                className={`question-item ${index === currentQuestionIndex ? 'active' : ''} ${responses[q.id] ? 'answered' : ''}`}
                onClick={() => {
                  setCurrentQuestionIndex(index)
                  setCurrentResponse(responses[q.id] || '')
                }}
              >
                <span className="question-number-small">{index + 1}</span>
                <span className="question-status">
                  {responses[q.id] ? '✓' : '○'}
                </span>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Interview

