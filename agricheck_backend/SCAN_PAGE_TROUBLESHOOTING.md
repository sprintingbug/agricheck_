# Scan Page Troubleshooting Guide

## Common Issues and Solutions

### Issue: Scan Page Not Working

#### Possible Causes:

1. **Backend Server Not Running**
   - Check if backend is running on `http://localhost:8000`
   - Start backend: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

2. **Model Not Loaded**
   - The model file might be corrupted or still being written by training
   - Check if `models/best_finetuned.keras` exists and is not being written to
   - Restart backend server to reload model

3. **Model Training Still Running**
   - If training is still running, the model file might be locked
   - Wait for training to complete, then restart backend

4. **Connection Error**
   - Check if Flutter app can reach backend at `http://localhost:8000`
   - Verify backend CORS settings allow requests from Flutter app

5. **Image Validation Failing**
   - Image might be too blurry
   - Image might not be recognized as a rice leaf
   - Check error message in Flutter app

## Error Messages

### "Ang ML model ay hindi pa na-load"
- **Solution**: Restart the backend server
- The model might still be loading or failed to load

### "May problema sa pag-process ng scan"
- **Solution**: Check backend logs for detailed error
- Common causes:
  - Model file corrupted
  - TensorFlow error
  - Image preprocessing error

### "Mababa ang kumpiyansa sa diagnosis"
- **Solution**: Use a clearer, better-lit image of a rice leaf
- Image might be too blurry or not a proper rice leaf photo

### "Ang image ay malabo"
- **Solution**: Take a clearer photo with better lighting
- Ensure the leaf is in focus

### "Ang image ay hindi mukhang dahon ng palay"
- **Solution**: Upload a proper rice leaf image
- The image should show a rice leaf clearly

## Debugging Steps

1. **Check Backend Logs**
   - Look for error messages when scanning
   - Check if model loaded successfully at startup

2. **Verify Model File**
   ```bash
   dir models\best_finetuned.keras
   ```
   - File should exist and not be 0 bytes
   - File should not be locked (no training running)

3. **Test Backend Health**
   - Open: `http://localhost:8000/health`
   - Should return: `{"status":"ok"}`

4. **Test Scan Endpoint**
   - Use Swagger UI: `http://localhost:8000/docs`
   - Try uploading an image through the API docs

5. **Check Model Loading**
   - Backend logs should show:
     ```
     Successfully loaded Keras model from models/best_finetuned.keras
     Model input shape: (None, 224, 224, 3)
     Model output shape: (None, 4)
     ```

## After Training Model

1. **Wait for Training to Complete**
   - Training saves model as `best_finetuned.keras`
   - Don't use model while training is still running

2. **Restart Backend Server**
   ```bash
   # Stop current server (Ctrl+C)
   # Start again
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Verify Model Loaded**
   - Check backend startup logs
   - Should see "Successfully loaded Keras model"

4. **Test Scan**
   - Try scanning a rice leaf image
   - Should work with new model

## Quick Fixes

### Restart Everything
1. Stop backend server (Ctrl+C)
2. Wait 5 seconds
3. Start backend server again
4. Try scan again

### Check Model File
```bash
# Navigate to backend directory
cd agricheck_backend

# Check if model exists
dir models\best_finetuned.keras

# Check file size (should be ~50MB, not 0 bytes)
```

### Reinstall Dependencies
```bash
# If model loading fails
pip install --upgrade tensorflow pillow numpy
```

## Still Not Working?

1. Check backend terminal for error messages
2. Check Flutter app console for error messages
3. Verify backend is accessible: `http://localhost:8000/health`
4. Try a different image (clear rice leaf photo)
5. Check if training completed successfully

---

**Last Updated**: After improving error handling in scan route

