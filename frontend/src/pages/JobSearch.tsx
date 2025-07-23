import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  TextField,
  Button,
  Paper,
  Grid,
  Card,
  CardContent,
  CardActions,
  Chip,
  Box,
  CircularProgress,
  Alert,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormControlLabel,
  Switch,
  Autocomplete,
  Divider,
  IconButton,
  Collapse
} from '@mui/material';
import {
  Search as SearchIcon,
  LocationOn as LocationIcon,
  AttachMoney as SalaryIcon,
  Work as WorkIcon,
  FilterList as FilterIcon,
  Bookmark as BookmarkIcon,
  BookmarkBorder as BookmarkBorderIcon,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon
} from '@mui/icons-material';

interface JobPosting {
  title: string;
  company: string;
  location: string;
  description: string;
  url: string;
  source: string;
  posting_date: string | null;
  salary: any;
  job_type: string | null;
  requirements: string[];
  benefits: string[];
  experience_level: string | null;
  remote_option: boolean;
  keywords: string[];
  match_score: number;
  confidence_score: number;
  ats_score: number;
  category: string;
  application_difficulty: string;
}

interface SearchFilters {
  query: string;
  location: string;
  max_results: number;
  include_remote: boolean;
  job_types: string[];
  salary_min: number | null;
  salary_max: number | null;
  date_posted: string;
  experience_levels: string[];
  companies_exclude: string[];
  keywords_required: string[];
  keywords_exclude: string[];
}

const JobSearch: React.FC = () => {
  const [jobs, setJobs] = useState<JobPosting[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showFilters, setShowFilters] = useState(false);
  const [savedJobs, setSavedJobs] = useState<Set<string>>(new Set());

  const [filters, setFilters] = useState<SearchFilters>({
    query: '',
    location: '',
    max_results: 25,
    include_remote: true,
    job_types: [],
    salary_min: null,
    salary_max: null,
    date_posted: 'all',
    experience_levels: [],
    companies_exclude: [],
    keywords_required: [],
    keywords_exclude: []
  });

  const jobTypes = ['fulltime', 'parttime', 'contract', 'internship', 'temporary'];
  const experienceLevels = ['junior', 'mid', 'senior', 'internship'];
  const dateOptions = [
    { value: 'all', label: 'All Time' },
    { value: 'today', label: 'Today' },
    { value: 'week', label: 'This Week' },
    { value: 'month', label: 'This Month' }
  ];

  const handleSearch = async () => {
    if (!filters.query.trim()) {
      setError('Please enter a search query');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch('/api/v1/jobs/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(filters)
      });

      if (!response.ok) {
        throw new Error('Search failed');
      }

      const data = await response.json();
      setJobs(data.jobs || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Search failed');
    } finally {
      setLoading(false);
    }
  };

  const handleSaveJob = async (job: JobPosting) => {
    try {
      const token = localStorage.getItem('access_token');
      const jobId = `${job.company}_${job.title}`.replace(/\s+/g, '_');
      
      const response = await fetch(`/api/v1/jobs/${jobId}/save`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        setSavedJobs(prev => new Set(prev).add(jobId));
      }
    } catch (err) {
      console.error('Failed to save job:', err);
    }
  };

  const formatSalary = (salary: any) => {
    if (!salary) return 'Salary not specified';
    
    if (salary.min && salary.max) {
      return `$${salary.min.toLocaleString()} - $${salary.max.toLocaleString()}`;
    } else if (salary.min) {
      return `$${salary.min.toLocaleString()}+`;
    }
    
    return 'Salary not specified';
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy': return 'success';
      case 'medium': return 'warning';
      case 'hard': return 'error';
      default: return 'default';
    }
  };

  const getMatchScoreColor = (score: number) => {
    if (score >= 0.8) return 'success';
    if (score >= 0.6) return 'warning';
    return 'error';
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Job Search
      </Typography>
      
      {/* Search Bar */}
      <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              label="Job Title or Keywords"
              value={filters.query}
              onChange={(e) => setFilters({ ...filters, query: e.target.value })}
              placeholder="e.g., Python Developer, Data Scientist"
              InputProps={{
                startAdornment: <SearchIcon sx={{ mr: 1, color: 'action.active' }} />
              }}
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <TextField
              fullWidth
              label="Location"
              value={filters.location}
              onChange={(e) => setFilters({ ...filters, location: e.target.value })}
              placeholder="e.g., San Francisco, CA"
              InputProps={{
                startAdornment: <LocationIcon sx={{ mr: 1, color: 'action.active' }} />
              }}
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <FormControlLabel
              control={
                <Switch
                  checked={filters.include_remote}
                  onChange={(e) => setFilters({ ...filters, include_remote: e.target.checked })}
                />
              }
              label="Include Remote"
            />
          </Grid>
          <Grid item xs={12} md={2}>
            <Button
              fullWidth
              variant="contained"
              onClick={handleSearch}
              disabled={loading}
              startIcon={loading ? <CircularProgress size={20} /> : <SearchIcon />}
            >
              {loading ? 'Searching...' : 'Search'}
            </Button>
          </Grid>
        </Grid>

        {/* Advanced Filters Toggle */}
        <Box sx={{ mt: 2 }}>
          <Button
            startIcon={<FilterIcon />}
            endIcon={showFilters ? <ExpandLessIcon /> : <ExpandMoreIcon />}
            onClick={() => setShowFilters(!showFilters)}
          >
            Advanced Filters
          </Button>
        </Box>

        {/* Advanced Filters */}
        <Collapse in={showFilters}>
          <Divider sx={{ my: 2 }} />
          <Grid container spacing={2}>
            <Grid item xs={12} md={3}>
              <FormControl fullWidth>
                <InputLabel>Job Type</InputLabel>
                <Select
                  multiple
                  value={filters.job_types}
                  onChange={(e) => setFilters({ ...filters, job_types: e.target.value as string[] })}
                  renderValue={(selected) => (
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                      {selected.map((value) => (
                        <Chip key={value} label={value} size="small" />
                      ))}
                    </Box>
                  )}
                >
                  {jobTypes.map((type) => (
                    <MenuItem key={type} value={type}>
                      {type.charAt(0).toUpperCase() + type.slice(1)}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={3}>
              <FormControl fullWidth>
                <InputLabel>Experience Level</InputLabel>
                <Select
                  multiple
                  value={filters.experience_levels}
                  onChange={(e) => setFilters({ ...filters, experience_levels: e.target.value as string[] })}
                  renderValue={(selected) => (
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                      {selected.map((value) => (
                        <Chip key={value} label={value} size="small" />
                      ))}
                    </Box>
                  )}
                >
                  {experienceLevels.map((level) => (
                    <MenuItem key={level} value={level}>
                      {level.charAt(0).toUpperCase() + level.slice(1)}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={2}>
              <TextField
                fullWidth
                label="Min Salary"
                type="number"
                value={filters.salary_min || ''}
                onChange={(e) => setFilters({ ...filters, salary_min: e.target.value ? parseInt(e.target.value) : null })}
                InputProps={{
                  startAdornment: <SalaryIcon sx={{ mr: 1, color: 'action.active' }} />
                }}
              />
            </Grid>
            <Grid item xs={12} md={2}>
              <TextField
                fullWidth
                label="Max Salary"
                type="number"
                value={filters.salary_max || ''}
                onChange={(e) => setFilters({ ...filters, salary_max: e.target.value ? parseInt(e.target.value) : null })}
                InputProps={{
                  startAdornment: <SalaryIcon sx={{ mr: 1, color: 'action.active' }} />
                }}
              />
            </Grid>
            <Grid item xs={12} md={2}>
              <FormControl fullWidth>
                <InputLabel>Date Posted</InputLabel>
                <Select
                  value={filters.date_posted}
                  onChange={(e) => setFilters({ ...filters, date_posted: e.target.value })}
                >
                  {dateOptions.map((option) => (
                    <MenuItem key={option.value} value={option.value}>
                      {option.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </Collapse>
      </Paper>

      {/* Error Display */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Results Summary */}
      {jobs.length > 0 && (
        <Typography variant="h6" sx={{ mb: 2 }}>
          Found {jobs.length} job{jobs.length !== 1 ? 's' : ''}
        </Typography>
      )}

      {/* Job Results */}
      <Grid container spacing={3}>
        {jobs.map((job, index) => {
          const jobId = `${job.company}_${job.title}`.replace(/\s+/g, '_');
          const isSaved = savedJobs.has(jobId);

          return (
            <Grid item xs={12} key={index}>
              <Card elevation={2} sx={{ '&:hover': { elevation: 4 } }}>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                    <Box sx={{ flexGrow: 1 }}>
                      <Typography variant="h6" component="h3" sx={{ mb: 1 }}>
                        {job.title}
                      </Typography>
                      <Typography variant="subtitle1" color="primary" sx={{ mb: 1 }}>
                        {job.company}
                      </Typography>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          <LocationIcon fontSize="small" sx={{ mr: 0.5, color: 'text.secondary' }} />
                          <Typography variant="body2" color="text.secondary">
                            {job.location}
                            {job.remote_option && ' (Remote Available)'}
                          </Typography>
                        </Box>
                        <Typography variant="body2" color="text.secondary">
                          {formatSalary(job.salary)}
                        </Typography>
                      </Box>
                    </Box>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Chip
                        label={`${Math.round(job.match_score * 100)}% Match`}
                        color={getMatchScoreColor(job.match_score)}
                        size="small"
                      />
                      <Chip
                        label={job.application_difficulty}
                        color={getDifficultyColor(job.application_difficulty)}
                        size="small"
                      />
                      <IconButton
                        onClick={() => handleSaveJob(job)}
                        color={isSaved ? 'primary' : 'default'}
                      >
                        {isSaved ? <BookmarkIcon /> : <BookmarkBorderIcon />}
                      </IconButton>
                    </Box>
                  </Box>

                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    {job.description.substring(0, 300)}
                    {job.description.length > 300 ? '...' : ''}
                  </Typography>

                  {/* Keywords */}
                  {job.keywords.length > 0 && (
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                        Skills & Keywords:
                      </Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {job.keywords.slice(0, 10).map((keyword, idx) => (
                          <Chip key={idx} label={keyword} size="small" variant="outlined" />
                        ))}
                        {job.keywords.length > 10 && (
                          <Chip label={`+${job.keywords.length - 10} more`} size="small" variant="outlined" />
                        )}
                      </Box>
                    </Box>
                  )}

                  {/* Job Metadata */}
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', pt: 1, borderTop: 1, borderColor: 'divider' }}>
                    <Box sx={{ display: 'flex', gap: 2 }}>
                      <Typography variant="caption" color="text.secondary">
                        Source: {job.source}
                      </Typography>
                      {job.posting_date && (
                        <Typography variant="caption" color="text.secondary">
                          Posted: {new Date(job.posting_date).toLocaleDateString()}
                        </Typography>
                      )}
                      <Typography variant="caption" color="text.secondary">
                        ATS Score: {Math.round(job.ats_score * 100)}%
                      </Typography>
                    </Box>
                    <Chip label={job.category} size="small" />
                  </Box>
                </CardContent>
                <CardActions>
                  <Button
                    size="small"
                    variant="contained"
                    href={job.url}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    View Job
                  </Button>
                  <Button size="small" color="primary">
                    Apply Now
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          );
        })}
      </Grid>

      {/* No Results */}
      {!loading && jobs.length === 0 && filters.query && (
        <Box sx={{ textAlign: 'center', py: 8 }}>
          <WorkIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
          <Typography variant="h6" color="text.secondary">
            No jobs found
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Try adjusting your search criteria or filters
          </Typography>
        </Box>
      )}

      {/* Initial State */}
      {!loading && jobs.length === 0 && !filters.query && (
        <Box sx={{ textAlign: 'center', py: 8 }}>
          <SearchIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
          <Typography variant="h6" color="text.secondary">
            Start your job search
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Enter keywords and location to find relevant opportunities
          </Typography>
        </Box>
      )}
    </Container>
  );
};

export default JobSearch;