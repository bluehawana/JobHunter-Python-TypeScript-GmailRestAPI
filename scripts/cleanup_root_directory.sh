#!/bin/bash
# Cleanup and organize root directory files

echo "🧹 Cleaning up root directory..."
echo ""

# Create archive directories if they don't exist
mkdir -p docs/archive/summaries
mkdir -p docs/archive/deployment
mkdir -p scripts/archive
mkdir -p templates/archive

echo "📁 Moving old documentation files..."

# Move old summary/status files to archive
mv AI_CONTENT_CUSTOMIZATION_SUCCESS.md docs/archive/summaries/ 2>/dev/null
mv AI_CUSTOMIZATION_DEPLOYED.md docs/archive/summaries/ 2>/dev/null
mv AI_PROMPTS_INTEGRATION_SUCCESS.md docs/archive/summaries/ 2>/dev/null
mv AI_PROMPTS_STATUS.md docs/archive/summaries/ 2>/dev/null
mv CLEANUP_SUMMARY.md docs/archive/summaries/ 2>/dev/null
mv CV_CL_FIXES_SUMMARY.md docs/archive/summaries/ 2>/dev/null
mv CV_LINK_COLOR_FIX_SUCCESS.md docs/archive/summaries/ 2>/dev/null
mv DEPLOYMENT_READY.md docs/archive/deployment/ 2>/dev/null
mv DEPLOYMENT_SUCCESS.md docs/archive/deployment/ 2>/dev/null
mv DEPLOYMENT_SUCCESS_SUMMARY.md docs/archive/deployment/ 2>/dev/null
mv DEPLOYMENT_SUMMARY.md docs/archive/deployment/ 2>/dev/null
mv FINAL_STATUS_AND_RECOMMENDATIONS.md docs/archive/summaries/ 2>/dev/null
mv FIXES_SUMMARY.md docs/archive/summaries/ 2>/dev/null
mv GIT_PUSH_SUCCESS.md docs/archive/summaries/ 2>/dev/null
mv IMPLEMENTATION_COMPLETE.md docs/archive/summaries/ 2>/dev/null
mv INTELLIGENT_SYSTEM_SUMMARY.md docs/archive/summaries/ 2>/dev/null
mv JOB_EXTRACTION_ENHANCEMENT_SUMMARY.md docs/archive/summaries/ 2>/dev/null
mv LEGO_BRICKS_SUCCESS_SUMMARY.md docs/archive/summaries/ 2>/dev/null
mv LEGO_FORMAT_UPDATE_SUCCESS.md docs/archive/summaries/ 2>/dev/null
mv LEGO_TEMPLATES_UPDATE_SUCCESS.md docs/archive/summaries/ 2>/dev/null
mv ROOT_DIRECTORY_CLEAN.md docs/archive/summaries/ 2>/dev/null
mv SESSION_SUMMARY.md docs/archive/summaries/ 2>/dev/null
mv TEMPLATE_FORMAT_UPDATE_COMPLETE.md docs/archive/summaries/ 2>/dev/null
mv TEMPLATE_LIBRARY_UPDATE_SUCCESS.md docs/archive/summaries/ 2>/dev/null
mv TEMPLATE_SYSTEM_STATUS.md docs/archive/summaries/ 2>/dev/null
mv TEMPLATE_UPDATES_SUMMARY.md docs/archive/summaries/ 2>/dev/null
mv VOLVO_APPLICATION_READY.md docs/archive/summaries/ 2>/dev/null
mv VPS_DEPLOYMENT_SUCCESS.md docs/archive/deployment/ 2>/dev/null

echo "📁 Moving deployment documentation..."

# Keep important deployment docs in docs/, move old ones to archive
mv DEPLOY_TO_ALPHAVPS_MANUAL.md docs/archive/deployment/ 2>/dev/null
mv DEPLOY_TO_VPS_MANUAL_COPY.md docs/archive/deployment/ 2>/dev/null
mv DEPLOYMENT_INSTRUCTIONS.md docs/archive/deployment/ 2>/dev/null
mv QUICK_DEPLOY_CHECKLIST.md docs/archive/deployment/ 2>/dev/null
mv README_AI_DEPLOYMENT.md docs/archive/deployment/ 2>/dev/null

# Move current deployment docs to docs/
mv DEPLOY_TO_PRODUCTION.md docs/ 2>/dev/null
mv FIX_VPS_500_ERROR.md docs/ 2>/dev/null
mv SWEDISH_JOB_EXTRACTION_FIX.md docs/ 2>/dev/null
mv VPS_AI_DEPLOYMENT_GUIDE.md docs/ 2>/dev/null

# Move guides to docs/
mv APPLICATION_GENERATORS_README.md docs/ 2>/dev/null
mv COMPREHENSIVE_SYSTEM_GUIDE.md docs/ 2>/dev/null
mv LEGO_WEB_APP_README.md docs/ 2>/dev/null
mv RESUME_TRUTH_CHECK.md docs/ 2>/dev/null
mv TEMPLATE_SYSTEM_SETUP.md docs/ 2>/dev/null

echo "📁 Moving test scripts..."

# Move test scripts to scripts/
mv test_*.py scripts/ 2>/dev/null
mv debug_*.py scripts/ 2>/dev/null
mv fix_*.py scripts/ 2>/dev/null
mv update_*.py scripts/ 2>/dev/null
mv create_*.py scripts/ 2>/dev/null
mv compile_*.py scripts/ 2>/dev/null
mv regenerate_*.py scripts/ 2>/dev/null

echo "📁 Moving deployment scripts..."

# Move deployment scripts to deploy/
mv DEPLOY_COMMANDS.sh deploy/ 2>/dev/null
mv DEPLOY_UPDATED_TEMPLATES.sh deploy/ 2>/dev/null
mv QUICK_DEPLOY_TO_VPS.sh deploy/ 2>/dev/null

echo "📁 Moving LaTeX templates..."

# Move loose LaTeX templates to templates/archive
mv *.tex templates/archive/ 2>/dev/null

echo "📁 Cleaning up empty files..."

# Remove empty or very small files
find . -maxdepth 1 -type f -size 0 -delete 2>/dev/null

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "📊 Summary:"
echo "  - Old summaries → docs/archive/summaries/"
echo "  - Old deployment docs → docs/archive/deployment/"
echo "  - Test scripts → scripts/"
echo "  - Deployment scripts → deploy/"
echo "  - LaTeX templates → templates/archive/"
echo ""
echo "📝 Files remaining in root:"
ls -1 *.md *.py *.sh 2>/dev/null | wc -l
echo ""
echo "🎯 Key files kept in root:"
echo "  - README.md"
echo "  - DEPLOY.md"
echo "  - requirements.txt"
echo "  - runtime.txt"
echo "  - Procfile"
