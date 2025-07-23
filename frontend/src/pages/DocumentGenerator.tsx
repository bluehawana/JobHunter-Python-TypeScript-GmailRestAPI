import React from 'react';
import { Container, Typography } from '@mui/material';

const DocumentGenerator: React.FC = () => {
  return (
    <Container>
      <Typography variant="h4" component="h1" gutterBottom>
        Document Generator
      </Typography>
      <Typography variant="body1">
        Document generation functionality will be implemented here.
      </Typography>
    </Container>
  );
};

export default DocumentGenerator;