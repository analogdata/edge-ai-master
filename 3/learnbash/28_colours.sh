#!/bin/bash
# Colour codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'    # NC = No Colour (reset)

echo -e "${GREEN}✅ Service is running${NC}"
echo -e "${RED}❌ Error: File not found${NC}"
echo -e "${YELLOW}⚠️  Warning: Disk is 80% full${NC}"
echo -e "${BLUE}ℹ️  Info: Starting inference...${NC}"
