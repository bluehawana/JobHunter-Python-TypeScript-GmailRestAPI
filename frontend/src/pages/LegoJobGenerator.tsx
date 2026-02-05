import React, { useState } from 'react';
import '../styles/LegoJobGenerator.css';

interface JobAnalysis {
  roleType: string;
  keywords: string[];
  requiredSkills: string[];
  achievements: string[];
  company: string;
  title: string;
}

interface GeneratedDocs {
  cvUrl: string;
  clUrl: string;
  cvPreview: string;
  clPreview: string;
}

const LegoJobGenerator: React.FC = () => {
  const [jobInput, setJobInput] = useState('');
  const [jobUrl, setJobUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState<JobAnalysis | null>(null);
  const [generatedDocs, setGeneratedDocs] = useState<GeneratedDocs | null>(null);
  const [step, setStep] = useState<'input' | 'analysis' | 'generated'>('input');

  const analyzeJob = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/analyze-job', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          jobDescription: jobInput,
          jobUrl: jobUrl
        })
      });

      const data = await response.json();

      if (!response.ok) {
        // Show detailed error message from server
        const errorMsg = data.suggestion
          ? `${data.error}\n\n💡 Suggestion: ${data.suggestion}`
          : data.error || 'Failed to analyze job. Please try again.';
        alert(errorMsg);
        return;
      }

      setAnalysis(data.analysis);
      // If job description was fetched from URL, update the textarea
      if (data.jobDescription && !jobInput) {
        setJobInput(data.jobDescription);
      }
      setStep('analysis');
    } catch (error) {
      console.error('Error analyzing job:', error);
      alert('Failed to analyze job. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const generateDocuments = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/generate-lego-application', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          jobDescription: jobInput,
          jobUrl: jobUrl,
          analysis: analysis
        })
      });

      const data = await response.json();
      setGeneratedDocs(data.documents);
      setStep('generated');
    } catch (error) {
      console.error('Error generating documents:', error);
      alert('Failed to generate documents. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const regenerateWithFeedback = async (feedback: string) => {
    setLoading(true);
    try {
      const response = await fetch('/api/regenerate-application', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          jobDescription: jobInput,
          analysis: analysis,
          feedback: feedback
        })
      });

      const data = await response.json();
      setGeneratedDocs(data.documents);
    } catch (error) {
      console.error('Error regenerating documents:', error);
      alert('Failed to regenerate documents. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const downloadDocuments = () => {
    if (generatedDocs) {
      // Create temporary links and trigger downloads
      const downloadFile = (url: string) => {
        // Extract the actual filename from the URL (e.g., /api/download/20260205_145627/cv_harvad_CompanyName.pdf)
        const filename = url.split('/').pop() || 'document.pdf';
        
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        link.style.display = 'none';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      };
      
      // Download CV with smart filename
      downloadFile(generatedDocs.cvUrl);
      
      // Download CL with a small delay to avoid browser blocking
      setTimeout(() => {
        downloadFile(generatedDocs.clUrl);
      }, 100);
    }
  };

  const resetToHome = () => {
    setJobInput('');
    setJobUrl('');
    setAnalysis(null);
    setGeneratedDocs(null);
    setStep('input');
  };

  return (
    <div className="lego-generator-container">
      <header className="lego-header">
        <div className="header-content">
          <button onClick={resetToHome} className="home-button" title="Back to Home">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <polyline points="9 22 9 12 15 12 15 22" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            <span>Home</span>
          </button>
          <div className="header-text">
            <h1>🧱 LEGO Bricks Job Application Generator</h1>
            <p>Paste a job description or URL, and we'll build the perfect CV & Cover Letter</p>
          </div>
        </div>
      </header>

      {step === 'input' && (
        <div className="input-section">
          <div className="input-group">
            <label>Job URL (LinkedIn, Indeed, etc.)</label>
            <input
              type="text"
              placeholder="https://www.linkedin.com/jobs/view/..."
              value={jobUrl}
              onChange={(e) => setJobUrl(e.target.value)}
              className="url-input"
            />
          </div>

          <div className="input-group">
            <label>Or paste the full job description</label>
            <textarea
              placeholder="Paste the complete job description here..."
              value={jobInput}
              onChange={(e) => setJobInput(e.target.value)}
              rows={15}
              className="job-input"
            />
          </div>

          <button
            onClick={analyzeJob}
            disabled={loading || (!jobInput && !jobUrl)}
            className="primary-button"
          >
            {loading ? '🔄 Analyzing...' : '🔍 Analyze Job'}
          </button>
        </div>
      )}

      {step === 'analysis' && analysis && (
        <div className="analysis-section">
          <h2>📊 Job Analysis</h2>

          <div className="analysis-card">
            <h3>Role Identified</h3>
            <div className="role-badge">{analysis.roleType}</div>
          </div>

          <div className="analysis-card">
            <h3>Company & Title</h3>
            <p><strong>{analysis.company}</strong> - {analysis.title}</p>
          </div>

          <div className="analysis-card">
            <h3>Key Requirements</h3>
            <div className="skills-grid">
              {analysis.requiredSkills.map((skill, idx) => (
                <span key={idx} className="skill-tag">{skill}</span>
              ))}
            </div>
          </div>

          <div className="analysis-card">
            <h3>ATS Keywords</h3>
            <div className="keywords-grid">
              {analysis.keywords.map((keyword, idx) => (
                <span key={idx} className="keyword-tag">{keyword}</span>
              ))}
            </div>
          </div>

          <div className="analysis-card">
            <h3>🧱 LEGO Bricks Selected</h3>
            <ul className="bricks-list">
              <li>✅ Profile: {analysis.roleType} focus</li>
              <li>✅ Skills: Prioritized by job requirements</li>
              <li>✅ Experience: Relevant achievements emphasized</li>
              <li>✅ Styling: Professional blue design</li>
            </ul>
          </div>

          <div className="button-group">
            <button onClick={() => setStep('input')} className="secondary-button">
              ← Back to Edit
            </button>
            <button onClick={generateDocuments} disabled={loading} className="primary-button">
              {loading ? '🔄 Generating...' : '🧱 Generate CV & Cover Letter'}
            </button>
          </div>
        </div>
      )}

      {step === 'generated' && generatedDocs && (
        <div className="generated-section">
          <h2>✅ Documents Generated!</h2>

          <div className="documents-grid">
            <div className="document-preview">
              <h3>📄 CV Preview</h3>
              <iframe
                src={generatedDocs.cvUrl}
                title="CV Preview"
                className="pdf-preview"
              />
              <a href={generatedDocs.cvUrl} target="_blank" rel="noopener noreferrer" className="view-button">
                View Full CV
              </a>
            </div>

            <div className="document-preview">
              <h3>💌 Cover Letter Preview</h3>
              <iframe
                src={generatedDocs.clUrl}
                title="Cover Letter Preview"
                className="pdf-preview"
              />
              <a href={generatedDocs.clUrl} target="_blank" rel="noopener noreferrer" className="view-button">
                View Full Cover Letter
              </a>
            </div>
          </div>

          <div className="feedback-section">
            <h3>Need adjustments?</h3>
            <textarea
              placeholder="Describe what you'd like to change..."
              rows={4}
              className="feedback-input"
              id="feedback-input"
            />
            <button
              onClick={() => {
                const feedback = (document.getElementById('feedback-input') as HTMLTextAreaElement).value;
                regenerateWithFeedback(feedback);
              }}
              disabled={loading}
              className="secondary-button"
            >
              {loading ? '🔄 Regenerating...' : '🔄 Regenerate with Feedback'}
            </button>
          </div>

          <div className="button-group">
            <button onClick={() => {
              setStep('input');
              setJobInput('');
              setJobUrl('');
              setAnalysis(null);
              setGeneratedDocs(null);
            }} className="secondary-button">
              ← Start New Application
            </button>
            <button onClick={downloadDocuments} className="primary-button">
              ⬇️ Download Both Documents
            </button>
          </div>
        </div>
      )}

      {loading && (
        <div className="loading-overlay">
          <div className="loading-spinner">
            <div className="spinner"></div>
            <p>Building your perfect application with LEGO bricks...</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default LegoJobGenerator;
