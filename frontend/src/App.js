import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [resumeText, setResumeText] = useState('');
  const [jobText, setJobText] = useState('');
  const [result, setResult] = useState(null);
  const [agenticResult, setAgenticResult] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState('');
  const [activeTab, setActiveTab] = useState('upload');

  const handleFileUpload = async () => {
    if (!file) {
      setUploadStatus('Please select a file');
      return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    setLoading(true);
    setUploadStatus('Uploading...');
    try {
      const response = await axios.post('http://localhost:8000/upload-resume', formData);
      if (response.data.extracted_text) {
        setResumeText(response.data.extracted_text);
      }
      setResult(response.data);
      setUploadStatus('Resume uploaded successfully');
      setActiveTab('analyze');
    } catch (error) {
      setUploadStatus('Upload failed');
    }
    setLoading(false);
  };

  const handleAnalyze = async () => {
    if (!resumeText) {
      alert('Please paste resume text');
      return;
    }
    
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/analyze-text', {
        resume_text: resumeText,
        job_text: jobText || null
      });
      setResult(response.data);
      setAgenticResult(null);
    } catch (error) {
      alert('Analysis failed');
    }
    setLoading(false);
  };

  const handleAgenticAnalyze = async () => {
    if (!resumeText) {
      alert('Please paste resume text');
      return;
    }
    
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/agentic-analyze', {
        resume_text: resumeText,
        job_text: jobText || null
      });
      setAgenticResult(response.data);
      setResult(null);
    } catch (error) {
      alert('Agentic analysis failed');
    }
    setLoading(false);
  };

  const handleGenerateQuestions = async () => {
    if (!resumeText) {
      alert('Please paste resume text first');
      return;
    }
    
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/generate-questions', {
        role: 'Machine Learning Engineer',
        question_type: 'technical',
        count: 5,
        resume_text: resumeText
      });
      setQuestions(response.data.questions);
    } catch (error) {
      alert('Failed to generate questions');
    }
    setLoading(false);
  };

  const styles = {
    container: { padding: '30px', fontFamily: 'Segoe UI, Arial, sans-serif', maxWidth: '1000px', margin: '0 auto', color: '#333' },
    header: { fontSize: '28px', fontWeight: '600', borderBottom: '3px solid #2c3e50', paddingBottom: '12px', marginBottom: '30px', color: '#2c3e50' },
    tabs: { display: 'flex', gap: '10px', marginBottom: '20px', borderBottom: '1px solid #ddd', paddingBottom: '10px', flexWrap: 'wrap' },
    tab: { padding: '10px 20px', cursor: 'pointer', border: 'none', background: 'none', fontSize: '15px', fontWeight: '500', color: '#666' },
    tabActive: { padding: '10px 20px', cursor: 'pointer', border: 'none', background: 'none', fontSize: '15px', fontWeight: '600', color: '#2c3e50', borderBottom: '3px solid #2c3e50' },
    section: { border: '1px solid #e0e0e0', padding: '20px', borderRadius: '6px', marginBottom: '20px', backgroundColor: '#fafafa' },
    sectionTitle: { marginTop: '0', marginBottom: '15px', color: '#2c3e50', fontSize: '18px', fontWeight: '600' },
    input: { width: '100%', padding: '10px', border: '1px solid #ddd', borderRadius: '4px', fontFamily: 'Segoe UI, Arial, sans-serif', fontSize: '14px', boxSizing: 'border-box' },
    button: { padding: '8px 24px', backgroundColor: '#2c3e50', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '14px', fontWeight: '500' },
    buttonDisabled: { padding: '8px 24px', backgroundColor: '#95a5a6', color: 'white', border: 'none', borderRadius: '4px', cursor: 'not-allowed', fontSize: '14px', fontWeight: '500', opacity: 0.6 },
    resultContainer: { border: '1px solid #27ae60', padding: '20px', borderRadius: '6px', backgroundColor: '#f0f8f0', marginTop: '20px' },
    agenticContainer: { border: '1px solid #8e44ad', padding: '20px', borderRadius: '6px', backgroundColor: '#f4ecf7', marginTop: '20px' },
    resultSection: { marginBottom: '15px' },
    resultLabel: { fontWeight: '600', color: '#2c3e50', fontSize: '14px', marginBottom: '4px' },
    resultValue: { fontSize: '14px', color: '#333', padding: '8px 12px', backgroundColor: 'white', borderRadius: '4px', border: '1px solid #e0e0e0' },
    skillTag: { display: 'inline-block', padding: '4px 12px', margin: '4px', backgroundColor: '#e8e8e8', borderRadius: '20px', fontSize: '13px', color: '#333' },
    scoreLarge: { fontSize: '32px', fontWeight: '700', padding: '10px', textAlign: 'center' },
    scoreGreen: { color: '#27ae60' },
    scoreOrange: { color: '#e67e22' },
    scoreRed: { color: '#e74c3c' }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.header}>AI Resume Analyzer</h1>
      
      <div style={styles.tabs}>
        <button style={activeTab === 'upload' ? styles.tabActive : styles.tab} onClick={() => setActiveTab('upload')}>
          Upload PDF
        </button>
        <button style={activeTab === 'analyze' ? styles.tabActive : styles.tab} onClick={() => setActiveTab('analyze')}>
          AI Analysis
        </button>
        <button style={activeTab === 'questions' ? styles.tabActive : styles.tab} onClick={() => setActiveTab('questions')}>
          Interview Prep
        </button>
      </div>

      {activeTab === 'upload' && (
        <div style={styles.section}>
          <h3 style={styles.sectionTitle}>Upload Resume PDF</h3>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
            <input type="file" accept=".pdf" onChange={(e) => setFile(e.target.files[0])} style={{ flex: 1 }} />
            <button onClick={handleFileUpload} disabled={loading} style={loading ? styles.buttonDisabled : styles.button}>
              {loading ? 'Uploading...' : 'Upload'}
            </button>
          </div>
          {uploadStatus && <p style={{ marginTop: '10px', color: uploadStatus.includes('success') ? '#27ae60' : '#e74c3c' }}>{uploadStatus}</p>}
        </div>
      )}

      {activeTab === 'analyze' && (
        <div>
          <div style={styles.section}>
            <h3 style={styles.sectionTitle}>Paste Resume Text</h3>
            <textarea
              placeholder="Paste your resume text here..."
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
              rows={8}
              style={styles.input}
            />
            <textarea
              placeholder="Paste job description (optional)..."
              value={jobText}
              onChange={(e) => setJobText(e.target.value)}
              rows={4}
              style={{ ...styles.input, marginTop: '10px' }}
            />
            <div style={{ display: 'flex', gap: '10px', marginTop: '10px', flexWrap: 'wrap' }}>
              <button onClick={handleAnalyze} disabled={loading} style={loading ? styles.buttonDisabled : styles.button}>
                {loading ? 'Analyzing...' : 'Run Analysis'}
              </button>
              <button onClick={handleAgenticAnalyze} disabled={loading} style={{ ...(loading ? styles.buttonDisabled : styles.button), backgroundColor: '#8e44ad' }}>
                {loading ? 'Analyzing...' : 'Run Agentic AI Analysis'}
              </button>
            </div>
          </div>

          {result && result.structured_info && (
            <div style={styles.resultContainer}>
              <h3 style={{ ...styles.sectionTitle, color: '#27ae60' }}>Analysis Results</h3>
              <div style={styles.resultSection}>
                <div style={styles.resultLabel}>Name</div>
                <div style={styles.resultValue}>{result.structured_info.name || 'Not Found'}</div>
              </div>
              <div style={styles.resultSection}>
                <div style={styles.resultLabel}>Contact Information</div>
                <div style={styles.resultValue}>
                  <div><strong>Email:</strong> {result.structured_info.email || 'Not Found'}</div>
                  <div><strong>Phone:</strong> {result.structured_info.phone || 'Not Found'}</div>
                </div>
              </div>
              <div style={styles.resultSection}>
                <div style={styles.resultLabel}>Education</div>
                <div style={styles.resultValue}>
                  {result.structured_info.education && result.structured_info.education.length > 0 ? (
                    result.structured_info.education.map((edu, i) => <div key={i}>• {edu}</div>)
                  ) : 'Not Found'}
                </div>
              </div>
              <div style={styles.resultSection}>
                <div style={styles.resultLabel}>Experience</div>
                <div style={styles.resultValue}>
                  {result.structured_info.experience && result.structured_info.experience.length > 0 ? (
                    result.structured_info.experience.map((exp, i) => <div key={i}>• {exp}</div>)
                  ) : 'Not Found'}
                </div>
              </div>
              <div style={styles.resultSection}>
                <div style={styles.resultLabel}>Skills ({result.skill_count || 0})</div>
                <div style={styles.resultValue}>
                  {result.structured_info.skills && result.structured_info.skills.length > 0 ? (
                    result.structured_info.skills.map((skill, i) => (
                      <span key={i} style={styles.skillTag}>{skill}</span>
                    ))
                  ) : 'No skills found'}
                </div>
              </div>
              {result.status && (
                <div style={styles.resultSection}>
                  <div style={styles.resultLabel}>Status</div>
                  <div style={{ ...styles.resultValue, color: '#27ae60' }}>{result.status}</div>
                </div>
              )}
            </div>
          )}

          {agenticResult && (
            <div style={styles.agenticContainer}>
              <h3 style={{ ...styles.sectionTitle, color: '#8e44ad' }}>Agentic AI Analysis Results</h3>
              
              {agenticResult.ml_classification && (
                <div style={styles.resultSection}>
                  <div style={styles.resultLabel}>ML Classification</div>
                  <div style={styles.resultValue}>
                    <div><strong>Predicted Role:</strong> {agenticResult.ml_classification.predicted_category}</div>
                    <div><strong>Confidence:</strong> {(agenticResult.ml_classification.confidence * 100).toFixed(1)}%</div>
                    {agenticResult.ml_classification.matched_keywords && (
                      <div><strong>Matched Keywords:</strong> {agenticResult.ml_classification.matched_keywords.join(', ')}</div>
                    )}
                  </div>
                </div>
              )}

              {agenticResult.match_score && (
                <div style={styles.resultSection}>
                  <div style={styles.resultLabel}>Match Score</div>
                  <div style={{ ...styles.scoreLarge, ...(agenticResult.match_score.score > 70 ? styles.scoreGreen : agenticResult.match_score.score > 40 ? styles.scoreOrange : styles.scoreRed) }}>
                    {agenticResult.match_score.score}%
                  </div>
                  <div style={styles.resultValue}>
                    <div><strong>Matching Skills:</strong> {agenticResult.match_score.matching.join(', ')}</div>
                    <div style={{ color: '#e74c3c' }}><strong>Missing Skills:</strong> {agenticResult.match_score.missing.join(', ')}</div>
                  </div>
                </div>
              )}

              {agenticResult.questions && agenticResult.questions.length > 0 && (
                <div style={styles.resultSection}>
                  <div style={styles.resultLabel}>Personalized Questions</div>
                  <div style={styles.resultValue}>
                    {agenticResult.questions.map((q, i) => (
                      <div key={i} style={{ padding: '5px 0', borderBottom: '1px solid #eee' }}>
                        <strong>Q{i+1}:</strong> {q}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {agenticResult.summary && (
                <div style={styles.resultSection}>
                  <div style={styles.resultLabel}>Summary</div>
                  <div style={styles.resultValue}>{agenticResult.summary}</div>
                </div>
              )}

              {agenticResult.status && (
                <div style={styles.resultSection}>
                  <div style={styles.resultLabel}>Status</div>
                  <div style={{ ...styles.resultValue, color: '#8e44ad' }}>{agenticResult.status}</div>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {activeTab === 'questions' && (
        <div>
          <div style={styles.section}>
            <h3 style={styles.sectionTitle}>Generate Interview Questions</h3>
            <button onClick={handleGenerateQuestions} disabled={loading} style={loading ? styles.buttonDisabled : styles.button}>
              {loading ? 'Generating...' : 'Generate Questions'}
            </button>
            
            {questions.length > 0 && (
              <div style={{ marginTop: '15px' }}>
                <h4 style={{ color: '#2c3e50', marginBottom: '10px', fontSize: '15px' }}>Interview Questions</h4>
                {questions.map((q, index) => (
                  <div key={index} style={{ padding: '10px', borderBottom: '1px solid #eee' }}>
                    <strong>Q{index + 1}:</strong> {typeof q === 'string' ? q : q.question}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;