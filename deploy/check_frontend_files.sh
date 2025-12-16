#!/bin/bash
# Check if all required frontend files exist

echo "🔍 Checking frontend files..."

FRONTEND_DIR="/var/www/lego-job-generator/frontend"

# Check if directory exists
if [ ! -d "$FRONTEND_DIR" ]; then
    echo "❌ Frontend directory not found: $FRONTEND_DIR"
    echo "Run: cp -r ~/frontend /var/www/lego-job-generator/"
    exit 1
fi

cd "$FRONTEND_DIR"

# Required files
FILES=(
    "package.json"
    "public/index.html"
    "src/index.js"
    "src/App.js"
    "src/pages/LegoJobGenerator.tsx"
    "src/styles/LegoJobGenerator.css"
)

MISSING=0

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file (MISSING)"
        MISSING=$((MISSING + 1))
    fi
done

echo ""
if [ $MISSING -eq 0 ]; then
    echo "✅ All required files present!"
    echo "You can proceed with: npm install && npm run build"
else
    echo "⚠️  $MISSING file(s) missing!"
    echo ""
    echo "Creating missing files..."
    
    # Create src/index.js if missing
    if [ ! -f "src/index.js" ]; then
        mkdir -p src
        cat > src/index.js << 'EOF'
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
EOF
        echo "✅ Created src/index.js"
    fi
    
    # Create src/App.js if missing
    if [ ! -f "src/App.js" ]; then
        cat > src/App.js << 'EOF'
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LegoJobGenerator from './pages/LegoJobGenerator';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<LegoJobGenerator />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
EOF
        echo "✅ Created src/App.js"
    fi
    
    # Create src/index.css if missing
    if [ ! -f "src/index.css" ]; then
        cat > src/index.css << 'EOF'
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}
EOF
        echo "✅ Created src/index.css"
    fi
    
    # Create src/App.css if missing
    if [ ! -f "src/App.css" ]; then
        cat > src/App.css << 'EOF'
.App {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
EOF
        echo "✅ Created src/App.css"
    fi
    
    # Create public/index.html if missing
    if [ ! -f "public/index.html" ]; then
        mkdir -p public
        cat > public/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="LEGO Bricks Job Application Generator" />
    <title>LEGO Job Generator - jobs.bluehawana.com</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
EOF
        echo "✅ Created public/index.html"
    fi
    
    echo ""
    echo "✅ Missing files created!"
    echo "Now run: npm install && npm run build"
fi

echo ""
echo "📦 Checking package.json dependencies..."
if [ -f "package.json" ]; then
    if grep -q "react-router-dom" package.json; then
        echo "✅ react-router-dom found in package.json"
    else
        echo "⚠️  react-router-dom not found - will be installed during npm install"
    fi
fi
