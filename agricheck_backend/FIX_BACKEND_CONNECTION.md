# Fix Backend Connection from Phone

## Problem
Your phone can't access the backend at `http://192.168.1.10:8000`

## Solution: Allow Port 8000 in Windows Firewall

### Option 1: Run the Script (Easiest)
1. Right-click `fix_firewall.bat`
2. Select **"Run as administrator"**
3. Click "Yes" when prompted
4. The script will add the firewall rule automatically

### Option 2: Manual Windows Firewall Setup
1. Press `Win + R` and type: `wf.msc` (or search "Windows Defender Firewall with Advanced Security")
2. Click **"Inbound Rules"** on the left
3. Click **"New Rule"** on the right
4. Select **"Port"** → Next
5. Select **"TCP"** and enter **8000** → Next
6. Select **"Allow the connection"** → Next
7. Check all profiles (Domain, Private, Public) → Next
8. Name it: **"Agricheck Backend"** → Finish

### Option 3: PowerShell (Run as Admin)
Open PowerShell as Administrator and run:
```powershell
New-NetFirewallRule -DisplayName "Agricheck Backend" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
```

## Verify It Works
1. Make sure backend is running: `D:\dev\agricheck_backend\start_backend.bat`
2. On your phone's browser, go to: `http://192.168.1.10:8000/health`
3. You should see: `{"status":"ok"}`

## If It Still Doesn't Work
- Make sure both devices are on the same WiFi network
- Check if your computer's IP is still `192.168.1.10` (run `ipconfig`)
- Try disabling Windows Firewall temporarily to test (not recommended long-term)
- Check if antivirus is blocking the connection

