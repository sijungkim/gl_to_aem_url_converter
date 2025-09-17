# 🐳 Docker Troubleshooting Guide

## ERR_CONNECTION_REFUSED Solutions

### **🌐 WSL2 Networking Issue**

The "ERR_CONNECTION_REFUSED" error is common with WSL2. The application is working, but the URL access method matters.

### **✅ Solutions to Try:**

#### **1. Use Different URLs:**
```bash
# Try these URLs in order:
http://localhost:8501          # Windows browser (most common)
http://127.0.0.1:8501         # WSL browser
http://172.27.8.105:8501      # WSL2 IP (your IP may differ)
```

#### **2. Check Container Status:**
```bash
# Verify container is running
docker ps

# Should show gl-to-aem-url container with status "Up" and "(healthy)"
```

#### **3. Check Port Binding:**
```bash
# Look for port mapping: 0.0.0.0:8501->8501/tcp
docker port gl-to-aem-url
```

#### **4. Test Connection from WSL:**
```bash
# Test if application responds
curl http://localhost:8501

# Should return HTML content, not connection refused
```

### **🔧 Advanced Troubleshooting:**

#### **Check Application Logs:**
```bash
# View container logs
docker logs gl-to-aem-url

# Should show: "You can now view your Streamlit app in your browser."
```

#### **Interactive Container Access:**
```bash
# Access container shell for debugging
docker exec -it gl-to-aem-url /bin/bash

# Check if Streamlit is running
ps aux | grep streamlit
```

#### **Firewall Issues (Windows):**
```bash
# If Windows Defender blocks, add firewall rule:
# Windows -> Settings -> Network -> Windows Defender Firewall
# -> Allow an app through firewall -> Add Docker Desktop
```

### **🚀 Working Example:**

```bash
# From anywhere in WSL:
cd /tmp
aem-docker

# Output should show:
# 🌐 Application URLs:
#    Windows Browser: http://localhost:8501
#    WSL Browser:     http://127.0.0.1:8501
#    Alternative:     http://172.27.8.105:8501
```

### **💡 Pro Tips:**

1. **Windows Browser**: Almost always use `localhost:8501`
2. **WSL Browser**: Use `127.0.0.1:8501` or the alternative IP
3. **Wait 10-15 seconds**: Container needs time to fully start
4. **Check container health**: Look for "(healthy)" status
5. **Use incognito mode**: Clears any browser cache issues

### **🆘 If Still Not Working:**

#### **Manual Container Test:**
```bash
# Stop any running containers
docker stop gl-to-aem-url

# Run manually for testing
docker run --rm -p 8501:8501 gl_to_aem_url:latest

# Wait for: "You can now view your Streamlit app in your browser."
# Then try: http://localhost:8501
```

#### **Alternative Port:**
```bash
# Try different port if 8501 is blocked
aem-docker --port 8502

# Then access: http://localhost:8502
```

#### **Network Mode:**
```bash
# Last resort - use host networking (Linux only)
docker run --rm --network host gl_to_aem_url:latest

# Then access: http://localhost:8501
```

### **✅ Success Indicators:**

1. **Container Status**: Shows "Up X seconds (healthy)"
2. **Port Binding**: Shows "0.0.0.0:8501->8501/tcp"
3. **Application Log**: Shows Streamlit startup message
4. **URL Response**: `curl localhost:8501` returns HTML
5. **Browser Access**: Shows AEM URL Converter interface

### **🔍 Quick Diagnostic:**

```bash
# Run this one-liner to check everything:
echo "=== Docker Status ===" && \
docker ps | grep gl-to-aem && \
echo "=== Port Test ===" && \
curl -I http://localhost:8501 2>/dev/null && \
echo "=== SUCCESS: Application is running ===" || \
echo "=== ISSUE: Check URLs above ==="
```

The Docker setup is working correctly - it's just a matter of using the right URL for your environment! 🎉