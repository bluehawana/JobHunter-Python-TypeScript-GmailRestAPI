import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  CardActions,
  Typography,
  Button,
  Box,
  Alert,
  CircularProgress,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemText,
  IconButton,
  Tooltip
} from '@mui/material';
import {
  Email as EmailIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Refresh as RefreshIcon,
  Info as InfoIcon,
  Link as LinkIcon,
  LinkOff as LinkOffIcon
} from '@mui/icons-material';

interface GmailStatus {
  gmail_connected: boolean;
  credentials_valid: boolean;
  connected_at?: string;
  email_count_estimate?: string;
}

interface TestResult {
  connection_status: string;
  recent_job_emails_count: number;
  sample_emails: Array<{
    subject: string;
    from: string;
    date: string;
  }>;
}

const GmailConnection: React.FC = () => {
  const [status, setStatus] = useState<GmailStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [connecting, setConnecting] = useState(false);
  const [disconnecting, setDisconnecting] = useState(false);
  const [testing, setTesting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [testResult, setTestResult] = useState<TestResult | null>(null);
  const [showTestDialog, setShowTestDialog] = useState(false);

  const fetchStatus = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const token = localStorage.getItem('access_token');
      const response = await fetch('/api/v1/gmail/status', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch Gmail status');
      }

      const data = await response.json();
      setStatus(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch status');
    } finally {
      setLoading(false);
    }
  };

  const handleConnect = async () => {
    try {
      setConnecting(true);
      setError(null);

      const token = localStorage.getItem('access_token');
      const response = await fetch('/api/v1/gmail/connect', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to initiate Gmail connection');
      }

      const data = await response.json();
      
      // Redirect to Google OAuth
      window.location.href = data.authorization_url;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to connect Gmail');
      setConnecting(false);
    }
  };

  const handleDisconnect = async () => {
    try {
      setDisconnecting(true);
      setError(null);

      const token = localStorage.getItem('access_token');
      const response = await fetch('/api/v1/gmail/disconnect', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to disconnect Gmail');
      }

      await fetchStatus(); // Refresh status
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to disconnect Gmail');
    } finally {
      setDisconnecting(false);
    }
  };

  const handleTestConnection = async () => {
    try {
      setTesting(true);
      setError(null);

      const token = localStorage.getItem('access_token');
      const response = await fetch('/api/v1/gmail/test-connection', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('Connection test failed');
      }

      const data = await response.json();
      setTestResult(data);
      setShowTestDialog(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Connection test failed');
    } finally {
      setTesting(false);
    }
  };

  useEffect(() => {
    fetchStatus();

    // Check for OAuth callback results
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('gmail_connected') === 'true') {
      setTimeout(() => {
        fetchStatus();
        // Remove URL parameters
        window.history.replaceState({}, document.title, window.location.pathname);
      }, 1000);
    } else if (urlParams.get('gmail_error') === 'true') {
      setError('Failed to connect Gmail account');
      // Remove URL parameters
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  }, []);

  const getStatusColor = () => {
    if (!status?.gmail_connected) return 'default';
    if (!status?.credentials_valid) return 'warning';
    return 'success';
  };

  const getStatusText = () => {
    if (!status?.gmail_connected) return 'Not Connected';
    if (!status?.credentials_valid) return 'Connection Issues';
    return 'Connected';
  };

  const getStatusIcon = () => {
    if (!status?.gmail_connected) return <LinkOffIcon />;
    if (!status?.credentials_valid) return <ErrorIcon />;
    return <CheckCircleIcon />;
  };

  if (loading) {
    return (
      <Card>
        <CardContent>
          <Box display="flex" alignItems="center" justifyContent="center" py={4}>
            <CircularProgress />
            <Typography variant="body2" sx={{ ml: 2 }}>
              Loading Gmail status...
            </Typography>
          </Box>
        </CardContent>
      </Card>
    );
  }

  return (
    <>
      <Card>
        <CardContent>
          <Box display="flex" alignItems="center" mb={2}>
            <EmailIcon sx={{ mr: 2, fontSize: 32, color: 'primary.main' }} />
            <Box flex={1}>
              <Typography variant="h6" component="h3">
                Gmail Integration
              </Typography>
              <Box display="flex" alignItems="center" gap={1} mt={1}>
                <Chip
                  icon={getStatusIcon()}
                  label={getStatusText()}
                  color={getStatusColor()}
                  size="small"
                />
                {status?.connected_at && (
                  <Typography variant="caption" color="text.secondary">
                    Connected: {new Date(status.connected_at).toLocaleDateString()}
                  </Typography>
                )}
              </Box>
            </Box>
            <Tooltip title="Refresh status">
              <IconButton onClick={fetchStatus} disabled={loading}>
                <RefreshIcon />
              </IconButton>
            </Tooltip>
          </Box>

          <Typography variant="body2" color="text.secondary" paragraph>
            Connect your Gmail account to automatically find job opportunities from your LinkedIn and Indeed email subscriptions.
          </Typography>

          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          {status?.gmail_connected && !status?.credentials_valid && (
            <Alert severity="warning" sx={{ mb: 2 }}>
              Your Gmail connection has expired or encountered issues. Please reconnect to continue receiving job opportunities from your emails.
            </Alert>
          )}

          {status?.gmail_connected && status?.credentials_valid && (
            <Alert severity="info" sx={{ mb: 2 }} icon={<InfoIcon />}>
              Gmail is connected and working properly. Job opportunities from your LinkedIn and Indeed subscription emails will automatically appear in your job search results.
            </Alert>
          )}
        </CardContent>

        <CardActions>
          <Box display="flex" gap={1} width="100%">
            {!status?.gmail_connected ? (
              <Button
                variant="contained"
                onClick={handleConnect}
                disabled={connecting}
                startIcon={connecting ? <CircularProgress size={20} /> : <LinkIcon />}
                fullWidth
              >
                {connecting ? 'Connecting...' : 'Connect Gmail'}
              </Button>
            ) : (
              <>
                <Button
                  variant="outlined"
                  onClick={handleTestConnection}
                  disabled={testing}
                  startIcon={testing ? <CircularProgress size={20} /> : <InfoIcon />}
                >
                  {testing ? 'Testing...' : 'Test Connection'}
                </Button>
                <Button
                  variant="outlined"
                  color="error"
                  onClick={handleDisconnect}
                  disabled={disconnecting}
                  startIcon={disconnecting ? <CircularProgress size={20} /> : <LinkOffIcon />}
                >
                  {disconnecting ? 'Disconnecting...' : 'Disconnect'}
                </Button>
              </>
            )}
          </Box>
        </CardActions>
      </Card>

      {/* Test Connection Dialog */}
      <Dialog
        open={showTestDialog}
        onClose={() => setShowTestDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Gmail Connection Test Results</DialogTitle>
        <DialogContent>
          {testResult && (
            <Box>
              <Alert 
                severity={testResult.connection_status === 'success' ? 'success' : 'error'}
                sx={{ mb: 2 }}
              >
                Connection Status: {testResult.connection_status === 'success' ? 'Successful' : 'Failed'}
              </Alert>
              
              <Typography variant="h6" gutterBottom>
                Recent Job-Related Emails
              </Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                Found {testResult.recent_job_emails_count} job-related emails in the last 7 days
              </Typography>

              {testResult.sample_emails.length > 0 && (
                <Box>
                  <Typography variant="subtitle2" gutterBottom>
                    Sample Emails:
                  </Typography>
                  <List dense>
                    {testResult.sample_emails.map((email, index) => (
                      <ListItem key={index} divider>
                        <ListItemText
                          primary={email.subject}
                          secondary={
                            <Box>
                              <Typography variant="caption" display="block">
                                From: {email.from}
                              </Typography>
                              <Typography variant="caption" color="text.secondary">
                                Date: {new Date(email.date).toLocaleDateString()}
                              </Typography>
                            </Box>
                          }
                        />
                      </ListItem>
                    ))}
                  </List>
                </Box>
              )}
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowTestDialog(false)}>
            Close
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default GmailConnection;