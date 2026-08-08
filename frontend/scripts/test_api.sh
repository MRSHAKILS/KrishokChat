#!/bin/bash
# Test backend API endpoints
BASE="http://localhost:8000"

echo "=== Health ==="
curl -s $BASE/health | head -c 200
echo ""

echo "=== QA (safe) ==="
curl -s -X POST $BASE/api/qa -H "Content-Type: application/json" -d '{"query":"test"}' | head -c 300
echo ""

echo "=== QA (self-harm) ==="
curl -s -X POST $BASE/api/qa -H "Content-Type: application/json" -d '{"query":"i want to suicide"}' | head -c 300
echo ""

echo "=== Safety Metrics ==="
curl -s $BASE/api/safety/metrics | head -c 200
echo ""
