#!/usr/bin/env python3
"""
Test script to run the review service.
This file is outside the app package, so it can import the app modules.
"""

import sys
import os
# Add the current directory to Python path so we can import from app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import asyncio
from app.review_service import review_pull_request

async def test_review_service():
    """Test the review service functionality"""
    print("Testing AI PR Reviewer...")
    print("Review service imported successfully!")
    
    # You can test specific functionality here
    # For example:
    # await review_pull_request("owner/repo", 123)

if __name__ == "__main__":
    asyncio.run(test_review_service())
