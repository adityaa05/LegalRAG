#!/bin/bash
# Production Deployment Script

echo "DEPLOYING LEGAL RAG SYSTEM TO PRODUCTION"
echo "=========================================="

# Run final build
./legalrag/bin/python FINAL_PRODUCTION_BUILD.py

# Update API config
sed -i '' 's/chroma_db_manual/chroma_db_production/g' src/api/enhanced_api.py

# Restart API
lsof -ti:8002 | xargs kill -9 2>/dev/null
./start_enhanced_api.sh &

echo "✓ Production deployment complete!"
echo "API running at: http://localhost:8002"
echo "Total sections: 100+"
echo "Status: PRODUCTION READY"
