#!/bin/bash
# Overleaf Batch Upload Instructions
echo "📱 OVERLEAF COMPILATION GUIDE"
echo "============================="
echo ""
echo "1. Go to: https://www.overleaf.com/"
echo "2. Create account (free)"
echo "3. Click 'New Project' > 'Upload Project'"
echo "4. Select files in this order:"
echo ""

echo "🏢 PRIORITY 1: Gothenburg CVs"
for file in cv_*volvo* cv_*polestar* cv_*skf* cv_*hasselblad* cv_*stena* cv_*cevt*; do
    if [ -f "$file" ]; then
        echo "   📄 $file"
    fi
done

echo ""
echo "📝 PRIORITY 2: Gothenburg Cover Letters"
for file in cover_letter_*volvo* cover_letter_*polestar* cover_letter_*skf* cover_letter_*hasselblad* cover_letter_*stena* cover_letter_*cevt*; do
    if [ -f "$file" ]; then
        echo "   📄 $file"
    fi
done

echo ""
echo "⭐ PRIORITY 3: High Match Companies"
for file in *spotify* *klarna* *techcorp*; do
    if [ -f "$file" ]; then
        echo "   📄 $file"
    fi
done

echo ""
echo "🔧 STEPS:"
echo "1. Upload 3-5 files at once to Overleaf"
echo "2. Click each file and press 'Recompile'"
echo "3. Download PDF for each compiled file"
echo "4. Repeat until all files are done"
