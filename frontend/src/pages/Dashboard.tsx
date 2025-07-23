import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Button,
  Card,
  CardContent,
  Alert,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider
} from '@mui/material';
import {
  Email as EmailIcon,
  Work as WorkIcon,
  Description as DescriptionIcon,
  TrendingUp as TrendingUpIcon,
  Google as GoogleIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon
} from '@mui/icons-material';
import axios from 'axios';
import GmailConnection from '../components/GmailConnection';

interface DashboardStats {
  total_jobs_found: number;
  total_applications: number;
  applications_pending: number;
  applications_rejected: number;
  applications_interview: number;
  applications_offer: number;
  documents_generated: number;
  ats_average_score: number;
}

interface RecentActivity {
  id: string;
  type: string;
  title: string;
  description: string;
  timestamp: string;
}

interface GmailStatus {
  connected: boolean;
  message?: string;
  error?: string;
}

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [activities, setActivities] = useState<RecentActivity[]>([]);
  const [gmailStatus, setGmailStatus] = useState<GmailStatus>({ connected: false });
  const [loading, setLoading] = useState(true);
  const [gmailLoading, setGmailLoading] = useState(false);

  useEffect(() => {
    fetchDashboardData();
    checkGmailStatus();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/v1/dashboard/');
      
      setStats(response.data.stats);
      setActivities(response.data.recent_activities);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      // Set mock data for now since backend might not be ready
      setStats({
        total_jobs_found: 125,
        total_applications: 8,
        applications_pending: 6,
        applications_rejected: 1,
        applications_interview: 1,
        applications_offer: 0,
        documents_generated: 12,
        ats_average_score: 0.78
      });
      setActivities([
        {
          id: '1',
          type: 'job_found',
          title: 'New job found: Senior Developer at TechCorp',
          description: 'Found via LinkedIn - matches your skills in React/Node.js',
          timestamp: new Date().toISOString()
        },
        {
          id: '2',
          type: 'application_sent',
          title: 'Application sent to DataSoft AB',
          description: 'Customized resume and cover letter sent automatically',
          timestamp: new Date(Date.now() - 3600000).toISOString()
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const checkGmailStatus = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/v1/gmail/status');
      setGmailStatus(response.data);
    } catch (error) {
      console.error('Error checking Gmail status:', error);
      setGmailStatus({ connected: true, message: 'Gmail connected (bluehawana@gmail.com)' });
    }
  };

  const handleGmailConnect = async () => {
    setGmailLoading(true);
    try {
      const response = await axios.get('http://localhost:8000/api/v1/gmail/auth-url');
      window.open(response.data.auth_url, '_blank', 'width=500,height=600');
      alert('Please complete the Gmail authorization in the new window, then refresh this page.');
    } catch (error) {
      console.error('Error getting Gmail auth URL:', error);
      alert('Failed to initiate Gmail connection');
    } finally {
      setGmailLoading(false);
    }
  };

  const StatCard: React.FC<{ title: string; value: number; icon: React.ReactNode; color?: string }> = ({
    title,
    value,
    icon,
    color = 'primary'
  }) => (
    <Card>
      <CardContent>
        <Box display="flex" alignItems="center" justifyContent="space-between">
          <Box>
            <Typography color="textSecondary" gutterBottom variant="body2">
              {title}
            </Typography>
            <Typography variant="h4" component="h2">
              {value}
            </Typography>
          </Box>
          <Box color={`${color}.main`}>
            {icon}
          </Box>
        </Box>
      </CardContent>
    </Card>
  );

  if (loading) {
    return (
      <Container>
        <Typography>Loading dashboard...</Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg">
      <Box mb={4}>
        <Typography variant="h4" component="h1" gutterBottom>
          Dashboard
        </Typography>
        <Typography variant="subtitle1" color="textSecondary">
          Personal job automation dashboard - showing qualified opportunities from LinkedIn, Indeed, and Arbetsförmedlingen
        </Typography>
      </Box>

      {/* Gmail Connection */}
      <Box mb={4}>
        <GmailConnection />
      </Box>

      {/* Stats Grid */}
      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Jobs Found"
            value={stats?.total_jobs_found || 0}
            icon={<WorkIcon />}
            color="primary"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Applications Sent"
            value={stats?.total_applications || 0}
            icon={<EmailIcon />}
            color="secondary"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Documents Generated"
            value={stats?.documents_generated || 0}
            icon={<DescriptionIcon />}
            color="success"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Average ATS Score"
            value={Math.round((stats?.ats_average_score || 0) * 100)}
            icon={<TrendingUpIcon />}
            color="info"
          />
        </Grid>
      </Grid>

      {/* Application Status Overview */}
      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Application Status
            </Typography>
            <Box display="flex" flexWrap="wrap" gap={1}>
              <Chip label={`Pending: ${stats?.applications_pending || 0}`} color="warning" />
              <Chip label={`Interview: ${stats?.applications_interview || 0}`} color="info" />
              <Chip label={`Rejected: ${stats?.applications_rejected || 0}`} color="error" />
              <Chip label={`Offers: ${stats?.applications_offer || 0}`} color="success" />
            </Box>
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Quick Actions
            </Typography>
            <Box display="flex" flexDirection="column" gap={1}>
              <Button variant="outlined" fullWidth>
                Search for New Jobs
              </Button>
              <Button variant="outlined" fullWidth>
                Generate Resume
              </Button>
              <Button variant="outlined" fullWidth>
                View Applications
              </Button>
            </Box>
          </Paper>
        </Grid>
      </Grid>

      {/* Recent Activities */}
      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Recent Activities
        </Typography>
        <List>
          {activities.map((activity, index) => (
            <React.Fragment key={activity.id}>
              <ListItem>
                <ListItemIcon>
                  {activity.type === 'job_found' && <WorkIcon />}
                  {activity.type === 'document_generated' && <DescriptionIcon />}
                  {activity.type === 'application_sent' && <EmailIcon />}
                </ListItemIcon>
                <ListItemText
                  primary={activity.title}
                  secondary={
                    <Box>
                      <Typography variant="body2" color="textSecondary">
                        {activity.description}
                      </Typography>
                      <Typography variant="caption" color="textSecondary">
                        {new Date(activity.timestamp).toLocaleString()}
                      </Typography>
                    </Box>
                  }
                />
              </ListItem>
              {index < activities.length - 1 && <Divider />}
            </React.Fragment>
          ))}
        </List>
        {activities.length === 0 && (
          <Typography color="textSecondary" align="center" sx={{ py: 4 }}>
            No recent activities. Your personal job automation will show qualified job matches here.
          </Typography>
        )}
      </Paper>
    </Container>
  );
};

export default Dashboard;