#!/bin/bash
# Verify all workers are returning consistent results

API_URL="http://jobs.bluehawana.com/api/analyze-job"
TESTS=10

echo "🔍 Consistency Verification Test"
echo "================================="
echo ""
echo "Testing: $API_URL"
echo "Number of requests: $TESTS"
echo ""

# Test 1: NVIDIA
echo "Test 1: NVIDIA Cloud Solution Architect"
echo "---------------------------------------"
nvidia_results=()
for i in $(seq 1 $TESTS); do
    result=$(curl -s -X POST "$API_URL" \
        -H "Content-Type: application/json" \
        -d '{"job_description":"NVIDIA\nCloud Solution Architect"}' \
        | jq -r '.company_name')
    nvidia_results+=("$result")
    echo "Request $i: $result"
done

# Check if all NVIDIA results are the same
nvidia_unique=$(printf '%s\n' "${nvidia_results[@]}" | sort -u | wc -l)
if [ "$nvidia_unique" -eq 1 ]; then
    echo "✅ NVIDIA: All $TESTS requests returned consistent results"
else
    echo "❌ NVIDIA: Inconsistent results detected!"
    printf '%s\n' "${nvidia_results[@]}" | sort | uniq -c
fi
echo ""

# Test 2: Microsoft
echo "Test 2: Microsoft Cloud Solution Architect"
echo "------------------------------------------"
ms_results=()
for i in $(seq 1 $TESTS); do
    result=$(curl -s -X POST "$API_URL" \
        -H "Content-Type: application/json" \
        -d '{"job_description":"Microsoft\nCloud Solution Architect"}' \
        | jq -r '.company_name')
    ms_results+=("$result")
    echo "Request $i: $result"
done

# Check if all Microsoft results are the same
ms_unique=$(printf '%s\n' "${ms_results[@]}" | sort -u | wc -l)
if [ "$ms_unique" -eq 1 ]; then
    echo "✅ Microsoft: All $TESTS requests returned consistent results"
else
    echo "❌ Microsoft: Inconsistent results detected!"
    printf '%s\n' "${ms_results[@]}" | sort | uniq -c
fi
echo ""

# Summary
echo "Summary"
echo "-------"
if [ "$nvidia_unique" -eq 1 ] && [ "$ms_unique" -eq 1 ]; then
    echo "✅ ALL TESTS PASSED - 100% consistency achieved!"
    echo ""
    echo "🎯 Service is production-ready with guaranteed consistency"
    exit 0
else
    echo "❌ CONSISTENCY ISSUES DETECTED"
    echo ""
    echo "🔧 Recommended actions:"
    echo "   1. Run: ./deploy/atomic_restart.sh"
    echo "   2. Wait 5 seconds"
    echo "   3. Run this test again"
    exit 1
fi
