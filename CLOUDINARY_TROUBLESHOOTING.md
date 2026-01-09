# Cloudinary Troubleshooting Guide

## Issue: Cannot See Verified Images in Cloudinary Platform

## Current Status
✅ **Integration is working correctly** - We've confirmed that:
- 4 verified documents are stored in your Cloudinary account
- Cloudinary credentials are properly configured
- API connection is successful
- Documents are accessible via direct URLs

## Why You Might Not See Images in Cloudinary Dashboard

### 1. **Wrong Account/Console**
Make sure you're logged into the correct Cloudinary account:
- **Cloud Name**: `dlrf0evj0`
- **Account Email**: The email associated with your Cloudinary account

### 2. **Folder Navigation**
The documents are stored in the `verified_documents` folder:
1. Log into [Cloudinary Console](https://cloudinary.com/console/)
2. Look for the `verified_documents` folder in your media library
3. Click on the folder to see the documents inside

### 3. **Direct URL Access**
You can access your documents directly using these URLs:
1. [Document 1](https://res.cloudinary.com/dlrf0evj0/image/upload/v1765693756/verified_documents/n5i3gjy5q7p8vairqdku.png)
2. [Document 2](https://res.cloudinary.com/dlrf0evj0/image/upload/v1765692093/verified_documents/rlqdkpr6oaxszct2lkqu.png)
3. [Document 3](https://res.cloudinary.com/dlrf0evj0/image/upload/v1765692851/verified_documents/t1imlamnbve8e74xqxhv.png)
4. [Document 4](https://res.cloudinary.com/dlrf0evj0/image/upload/v1765692148/verified_documents/wgyxjjssg06cjgnfwhdm.png)

## How the Integration Works

### Document Flow
```
Document Image → ML Model → Prediction (REAL/FAKE) → IF REAL → Upload to Cloudinary
```

### Storage Location
- **Folder**: `verified_documents`
- **Access**: Private (requires authentication)
- **Format**: Images are stored as PNG files

## Troubleshooting Steps

### 1. Check Cloudinary Console
1. Visit [Cloudinary Console](https://cloudinary.com/console/)
2. Login with your credentials
3. Navigate to Media Library
4. Look for `verified_documents` folder

### 2. Verify Credentials
Ensure your environment variables are set correctly:
```bash
export CLOUDINARY_URL=cloudinary://978394893957497:XxzS-1R-SCMYGvM6Or3BRmZ8SW0@dlrf0evj0
```

### 3. Test Connection
Run the debug script to verify connection:
```bash
cd /Users/rahulpoojari/Documents/mlmodel
source venv/bin/activate
python debug_cloudinary.py
```

## System Status

✅ **Working Components**:
- Cloudinary SDK integration
- Authentication with API keys
- Document upload functionality
- Document retrieval via API
- Frontend display of images

## Support Resources

### Cloudinary Documentation
- [Cloudinary Dashboard Guide](https://cloudinary.com/documentation/media_library_overview)
- [Folder Management](https://cloudinary.com/documentation/folders_overview)

### Contact Support
If you continue to have issues accessing your documents:
1. Cloudinary Support: support@cloudinary.com
2. Check [Cloudinary Status Page](https://status.cloudinary.com/)

## Next Steps

1. **View Documents**: Click the "Open Preview" button to see your verified documents
2. **Check Console**: Log into Cloudinary console to verify folder structure
3. **Test Upload**: Try uploading a new document through the system