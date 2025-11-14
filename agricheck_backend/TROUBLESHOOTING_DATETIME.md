# Troubleshooting Guide: Datetime Comparison Error

## Problem: "can't compare offset-naive and offset-aware datetimes"

### Error Symptoms
- 500 Internal Server Error when resetting password
- Error message: "can't compare offset-naive and offset-aware datetimes"
- Occurs in password reset functionality

### Root Cause
Python's datetime objects can be either:
- **Timezone-aware**: Has timezone information (e.g., `datetime.now(timezone.utc)`)
- **Timezone-naive**: No timezone information (e.g., `datetime.now()`)

When comparing these two types, Python raises: `TypeError: can't compare offset-naive and offset-aware datetimes`

### Where It Happened
In password reset code, we were comparing:
- `datetime.now(timezone.utc)` (timezone-aware)
- `user.reset_token_expires` (potentially timezone-naive from database)

### The Fix
**Location**: `app/auth/password_reset.py` and `app/auth/routes.py`

**Before (BROKEN)**:
```python
if not user.reset_token_expires or user.reset_token_expires < datetime.now(timezone.utc):
    raise HTTPException(...)
```

**After (FIXED)**:
```python
# Check token expiration - ensure both datetimes are timezone-aware
if not user.reset_token_expires:
    raise HTTPException(...)

# Ensure reset_token_expires is timezone-aware for comparison
now = datetime.now(timezone.utc)
expires = user.reset_token_expires

# If expires is naive, make it timezone-aware (assume UTC)
if expires.tzinfo is None:
    expires = expires.replace(tzinfo=timezone.utc)

if expires < now:
    raise HTTPException(...)
```

### Key Points
1. **Always separate None checks from datetime comparisons**
2. **Convert timezone-naive to timezone-aware before comparing**
3. **Use `tzinfo is None` to check if datetime is naive**
4. **Use `.replace(tzinfo=timezone.utc)` to make naive datetimes timezone-aware**

### Prevention
- Always use `datetime.now(timezone.utc)` when creating new datetimes (not `datetime.now()`)
- When comparing datetimes from database, check if they're timezone-aware first
- The database model uses `DateTime(timezone=True)` which should store timezone-aware datetimes, but old records might be naive

### Files Modified
- `app/auth/password_reset.py` - Line ~169
- `app/auth/routes.py` - Line ~120

### Status
✅ **FIXED** - Password reset now works correctly

---
**Date Fixed**: 2024
**Issue**: Password reset 500 error
**Solution**: Convert timezone-naive datetimes to timezone-aware before comparison

