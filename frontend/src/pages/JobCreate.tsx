import React, { useState } from 'react';
import {
  Container,
  Typography,
  TextField,
  Button,
  Paper,
  Grid,
  Box,
  Alert,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormControlLabel,
  Switch,
  Chip,
  Divider,
  CircularProgress
} from '@mui/material';
import {
  Add as AddIcon,
  Work as WorkIcon,
  Business as BusinessIcon,
  LocationOn as LocationIcon,
  Description as DescriptionIcon,
  AttachMoney as SalaryIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

interface CreateJobRequest {
  title: string;
  company: string;
  location: string;
  description: string;
  url: string;
  salary: {
    min?: number;
    max?: number;
  } | null;
  job_type: string;
  requirements: string[];
  benefits: string[];
  experience_level: string;
  remote_option: boolean;
  keywords: string[];
}

const JobCreate: React.FC = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const [formData, setFormData] = useState<CreateJobRequest>({
    title: '',
    company: '',
    location: '',
    description: '',
    url: '',
    salary: null,
    job_type: 'Full-time',
    requirements: [],
    benefits: [],
    experience_level: 'Mid',
    remote_option: false,
    keywords: []
  });

  const [requirementInput, setRequirementInput] = useState('');
  const [benefitInput, setBenefitInput] = useState('');
  const [keywordInput, setKeywordInput] = useState('');
  const [salaryMin, setSalaryMin] = useState<string>('');
  const [salaryMax, setSalaryMax] = useState<string>('');

  const jobTypes = ['Full-time', 'Part-time', 'Contract', 'Internship', 'Temporary'];
  const experienceLevels = ['Internship', 'Junior', 'Mid', 'Senior', 'Lead', 'Executive'];

  const handleInputChange = (field: keyof CreateJobRequest, value: any) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const addRequirement = () => {
    if (requirementInput.trim()) {
      setFormData(prev => ({
        ...prev,
        requirements: [...prev.requirements, requirementInput.trim()]
      }));
      setRequirementInput('');
    }
  };

  const removeRequirement = (index: number) => {
    setFormData(prev => ({
      ...prev,
      requirements: prev.requirements.filter((_, i) => i !== index)
    }));
  };

  const addBenefit = () => {
    if (benefitInput.trim()) {
      setFormData(prev => ({
        ...prev,
        benefits: [...prev.benefits, benefitInput.trim()]
      }));
      setBenefitInput('');
    }
  };

  const removeBenefit = (index: number) => {
    setFormData(prev => ({
      ...prev,
      benefits: prev.benefits.filter((_, i) => i !== index)
    }));
  };

  const addKeyword = () => {
    if (keywordInput.trim()) {
      setFormData(prev => ({
        ...prev,
        keywords: [...prev.keywords, keywordInput.trim()]
      }));
      setKeywordInput('');
    }
  };

  const removeKeyword = (index: number) => {
    setFormData(prev => ({
      ...prev,
      keywords: prev.keywords.filter((_, i) => i !== index)
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.title.trim() || !formData.company.trim() || !formData.description.trim()) {
      setError('Please fill in all required fields (Title, Company, Description)');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Prepare salary data
      const salary = (salaryMin || salaryMax) ? {
        ...(salaryMin ? { min: parseInt(salaryMin) } : {}),
        ...(salaryMax ? { max: parseInt(salaryMax) } : {})
      } : null;

      const requestData = {
        ...formData,
        salary
      };

      const token = localStorage.getItem('access_token');
      const response = await fetch('/api/v1/jobs/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(requestData)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to create job');
      }

      const data = await response.json();
      setSuccess(true);
      
      // Reset form
      setFormData({
        title: '',
        company: '',
        location: '',
        description: '',
        url: '',
        salary: null,
        job_type: 'Full-time',
        requirements: [],
        benefits: [],
        experience_level: 'Mid',
        remote_option: false,
        keywords: []
      });
      setSalaryMin('');
      setSalaryMax('');

      // Redirect after success
      setTimeout(() => {
        navigate('/job-search');
      }, 2000);

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create job');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Add New Job Opportunity
      </Typography>
      
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        Manually add a job opportunity to your job hunting pipeline
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 3 }}>
          Job created successfully! Redirecting to job search...
        </Alert>
      )}

      <Paper elevation={2} sx={{ p: 4 }}>
        <form onSubmit={handleSubmit}>
          <Grid container spacing={3}>
            {/* Basic Information */}
            <Grid item xs={12}>
              <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center' }}>
                <WorkIcon sx={{ mr: 1 }} />
                Basic Information
              </Typography>
              <Divider sx={{ mb: 3 }} />
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                required
                label="Job Title"
                value={formData.title}
                onChange={(e) => handleInputChange('title', e.target.value)}
                placeholder="e.g., Senior Software Engineer"
                InputProps={{
                  startAdornment: <WorkIcon sx={{ mr: 1, color: 'action.active' }} />
                }}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                required
                label="Company"
                value={formData.company}
                onChange={(e) => handleInputChange('company', e.target.value)}
                placeholder="e.g., Google, Microsoft, Tesla"
                InputProps={{
                  startAdornment: <BusinessIcon sx={{ mr: 1, color: 'action.active' }} />
                }}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Location"
                value={formData.location}
                onChange={(e) => handleInputChange('location', e.target.value)}
                placeholder="e.g., San Francisco, CA or Remote"
                InputProps={{
                  startAdornment: <LocationIcon sx={{ mr: 1, color: 'action.active' }} />
                }}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Job Posting URL"
                value={formData.url}
                onChange={(e) => handleInputChange('url', e.target.value)}
                placeholder="https://company.com/careers/job-id"
                type="url"
              />
            </Grid>

            <Grid item xs={12}>
              <TextField
                fullWidth
                required
                multiline
                rows={4}
                label="Job Description"
                value={formData.description}
                onChange={(e) => handleInputChange('description', e.target.value)}
                placeholder="Enter the complete job description including responsibilities, qualifications, and requirements..."
                InputProps={{
                  startAdornment: <DescriptionIcon sx={{ mr: 1, color: 'action.active', alignSelf: 'flex-start', mt: 1 }} />
                }}
              />
            </Grid>

            {/* Job Details */}
            <Grid item xs={12}>
              <Typography variant="h6" sx={{ mb: 2, mt: 3 }}>
                Job Details
              </Typography>
              <Divider sx={{ mb: 3 }} />
            </Grid>

            <Grid item xs={12} md={4}>
              <FormControl fullWidth>
                <InputLabel>Job Type</InputLabel>
                <Select
                  value={formData.job_type}
                  onChange={(e) => handleInputChange('job_type', e.target.value)}
                >
                  {jobTypes.map((type) => (
                    <MenuItem key={type} value={type}>
                      {type}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12} md={4}>
              <FormControl fullWidth>
                <InputLabel>Experience Level</InputLabel>
                <Select
                  value={formData.experience_level}
                  onChange={(e) => handleInputChange('experience_level', e.target.value)}
                >
                  {experienceLevels.map((level) => (
                    <MenuItem key={level} value={level}>
                      {level}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12} md={4}>
              <FormControlLabel
                control={
                  <Switch
                    checked={formData.remote_option}
                    onChange={(e) => handleInputChange('remote_option', e.target.checked)}
                  />
                }
                label="Remote Work Option"
              />
            </Grid>

            {/* Salary */}
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Minimum Salary"
                value={salaryMin}
                onChange={(e) => setSalaryMin(e.target.value)}
                type="number"
                placeholder="e.g., 80000"
                InputProps={{
                  startAdornment: <SalaryIcon sx={{ mr: 1, color: 'action.active' }} />
                }}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Maximum Salary"
                value={salaryMax}
                onChange={(e) => setSalaryMax(e.target.value)}
                type="number"
                placeholder="e.g., 120000"
                InputProps={{
                  startAdornment: <SalaryIcon sx={{ mr: 1, color: 'action.active' }} />
                }}
              />
            </Grid>

            {/* Requirements */}
            <Grid item xs={12}>
              <Typography variant="h6" sx={{ mb: 2, mt: 3 }}>
                Requirements & Skills
              </Typography>
              <Divider sx={{ mb: 3 }} />
            </Grid>

            <Grid item xs={12}>
              <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
                <TextField
                  fullWidth
                  label="Add Requirement"
                  value={requirementInput}
                  onChange={(e) => setRequirementInput(e.target.value)}
                  placeholder="e.g., 5+ years Python experience"
                  onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addRequirement())}
                />
                <Button variant="outlined" onClick={addRequirement}>
                  Add
                </Button>
              </Box>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {formData.requirements.map((req, index) => (
                  <Chip
                    key={index}
                    label={req}
                    onDelete={() => removeRequirement(index)}
                    color="primary"
                    variant="outlined"
                  />
                ))}
              </Box>
            </Grid>

            {/* Benefits */}
            <Grid item xs={12}>
              <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
                <TextField
                  fullWidth
                  label="Add Benefit"
                  value={benefitInput}
                  onChange={(e) => setBenefitInput(e.target.value)}
                  placeholder="e.g., Health insurance, 401k matching"
                  onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addBenefit())}
                />
                <Button variant="outlined" onClick={addBenefit}>
                  Add
                </Button>
              </Box>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {formData.benefits.map((benefit, index) => (
                  <Chip
                    key={index}
                    label={benefit}
                    onDelete={() => removeBenefit(index)}
                    color="secondary"
                    variant="outlined"
                  />
                ))}
              </Box>
            </Grid>

            {/* Keywords */}
            <Grid item xs={12}>
              <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
                <TextField
                  fullWidth
                  label="Add Keyword/Skill"
                  value={keywordInput}
                  onChange={(e) => setKeywordInput(e.target.value)}
                  placeholder="e.g., React, Node.js, AWS"
                  onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addKeyword())}
                />
                <Button variant="outlined" onClick={addKeyword}>
                  Add
                </Button>
              </Box>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {formData.keywords.map((keyword, index) => (
                  <Chip
                    key={index}
                    label={keyword}
                    onDelete={() => removeKeyword(index)}
                    variant="outlined"
                  />
                ))}
              </Box>
            </Grid>

            {/* Submit Button */}
            <Grid item xs={12}>
              <Box sx={{ mt: 4, display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
                <Button
                  variant="outlined"
                  onClick={() => navigate(-1)}
                  disabled={loading}
                >
                  Cancel
                </Button>
                <Button
                  type="submit"
                  variant="contained"
                  disabled={loading}
                  startIcon={loading ? <CircularProgress size={20} /> : <AddIcon />}
                >
                  {loading ? 'Creating...' : 'Create Job'}
                </Button>
              </Box>
            </Grid>
          </Grid>
        </form>
      </Paper>
    </Container>
  );
};

export default JobCreate;