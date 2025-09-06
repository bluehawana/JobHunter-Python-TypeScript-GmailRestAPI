import React, { useState } from 'react';
import {
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  Alert,
  CircularProgress,
  Card,
  CardContent,
  Chip,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon
} from '@mui/material';
import {
  Link as LinkIcon,
  Work as WorkIcon,
  LocationOn as LocationIcon,
  Business as BusinessIcon,
  Description as DescriptionIcon,
  Send as SendIcon,
  CheckCircle as CheckCircleIcon
} from '@mui/icons-material';
import axios from 'axios';

interface JobDetails {
  title: string;
  company: string;
  location: string;
  description: string;
  requirements: string[];
  url: string;
}

interface JobUrlProcessorProps {
  onApplicationGenerated?: (jobDetails: JobDetails) => void;
}

const JobUrlProcessor: React.FC<JobUrlProcessorProps> = ({ onApplicationGenerated }) => {
  const [jobUrl, setJobUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [jobDetails, setJobDetails] = useState<JobDetails | null>(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [generating, setGenerating] = useState(false);

  const handleUrlSubmit = async () => {
    if (!jobUrl.trim()) {
      setError('Please enter a job URL');
      return;
    }

    setLoading(true);
    setError('');
    setJobDetails(null);

    try {
      const response = await axios.post('/api/v1/jobs/extract-from-url', {
        url: jobUrl.trim()
      });

      if (response.data.success) {
        setJobDetails(response.data.job_details);
        setSuccess('Job details extracted successfully!');
      } else {
        setError(response.data.error || 'Failed to extract job details');
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to process job URL');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateApplication = async () => {
    if (!jobDetails) return;

    setGenerating(true);
    setError('');

    try {
      const response = await axios.post('/api/v1/applications/generate-tailored', {
        job_details: jobDetails,
        application_type: 'android_focused' // Default to Android focus based on ECARX success
      });

      if (response.data.success) {
        setSuccess('Tailored application generated and sent to your email!');
        onApplicationGenerated?.(jobDetails);
      } else {
        setError(response.data.error || 'Failed to generate application');
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate application');
    } finally {
      setGenerating(false);
    }
  };

  const isValidUrl = (url: string) => {
    try {
      new URL(url);
      return true;
    } catch {
      return false;
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
      <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <LinkIcon color="primary" />
        Direct Job URL Processor
      </Typography>
      
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Paste any job URL to automatically extract details and generate a tailored application
      </Typography>

      <Box sx={{ mb: 3 }}>
        <TextField
          fullWidth
          label="Job URL"
          placeholder="https://careers.company.com/job/12345 or LinkedIn job URL"
          value={jobUrl}
          onChange={(e) => setJobUrl(e.target.value)}
          error={!!error && !jobDetails}
          helperText={error && !jobDetails ? error : 'Supports LinkedIn, company career pages, and most job boards'}
          sx={{ mb: 2 }}
        />
        
        <Button
          variant="contained"
          onClick={handleUrlSubmit}
          disabled={loading || !jobUrl.trim() || !isValidUrl(jobUrl)}
          startIcon={loading ? <CircularProgress size={20} /> : <LinkIcon />}
          fullWidth
        >
          {loading ? 'Extracting Job Details...' : 'Extract Job Details'}
        </Button>
      </Box>

      {error && !jobDetails && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 2 }}>
          {success}
        </Alert>
      )}

      {jobDetails && (
        <Card variant="outlined" sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <WorkIcon color="primary" />
              {jobDetails.title}
            </Typography>
            
            <Box sx={{ display: 'flex', gap: 1, mb: 2, flexWrap: 'wrap' }}>
              <Chip 
                icon={<BusinessIcon />} 
                label={jobDetails.company} 
                color="primary" 
                variant="outlined" 
              />
              <Chip 
                icon={<LocationIcon />} 
                label={jobDetails.location} 
                color="secondary" 
                variant="outlined" 
              />
            </Box>

            <Divider sx={{ my: 2 }} />

            <Typography variant="subtitle2" gutterBottom>
              Job Description:
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              {jobDetails.description.substring(0, 300)}...
            </Typography>

            {jobDetails.requirements.length > 0 && (
              <>
                <Typography variant="subtitle2" gutterBottom>
                  Key Requirements:
                </Typography>
                <List dense>
                  {jobDetails.requirements.slice(0, 5).map((req, index) => (
                    <ListItem key={index} sx={{ py: 0.5 }}>
                      <ListItemIcon sx={{ minWidth: 30 }}>
                        <CheckCircleIcon color="success" fontSize="small" />
                      </ListItemIcon>
                      <ListItemText 
                        primary={req} 
                        primaryTypographyProps={{ variant: 'body2' }}
                      />
                    </ListItem>
                  ))}
                </List>
              </>
            )}

            <Box sx={{ mt: 3 }}>
              <Button
                variant="contained"
                color="success"
                onClick={handleGenerateApplication}
                disabled={generating}
                startIcon={generating ? <CircularProgress size={20} /> : <SendIcon />}
                fullWidth
                size="large"
              >
                {generating ? 'Generating Tailored Application...' : 'Generate & Send Tailored Application'}
              </Button>
            </Box>
          </CardContent>
        </Card>
      )}

      <Box sx={{ mt: 2 }}>
        <Typography variant="caption" color="text.secondary">
          💡 Tip: The system will automatically tailor your CV and cover letter based on the job requirements, 
          just like the successful ECARX Android application we just sent!
        </Typography>
      </Box>
    </Paper>
  );
};

export default JobUrlProcessor;