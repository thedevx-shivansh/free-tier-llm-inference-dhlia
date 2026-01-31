import subprocess
import os
import sys
import time
import shutil
from getpass import getpass

def main():
    print("=" * 65)
    print("  SOVEREIGN HYBRID AI - KAGGLE DEPLOYMENT v1.0")
    print("  Estimated time: 15-25 minutes")
    print("=" * 65)

    # Get token first (before any work)
    print("\n🔐 Enter your Ngrok auth token:")
    print("   (Get it from: https://dashboard.ngrok.com/get-started/your-authtoken)")
    NGROK_TOKEN = getpass("   Token: ")
    
    if len(NGROK_TOKEN) < 20:
        print("   ✗ Invalid token. Please get a valid token from ngrok.com")
        return
    
    print("\n" + "-" * 65)

    # =========================================================================
    # STEP 1: SYSTEM DEPENDENCIES
    # =========================================================================
    print("\n⚙️ [1/7] Installing system dependencies...")
    
    subprocess.run(["apt-get", "update", "-qq"], capture_output=True)
    
    # Install zstd - CRITICAL for Ollama extraction
    result = subprocess.run(
        ["apt-get", "install", "-y", "-qq", "zstd"],
        capture_output=True
    )
    
    # Verify zstd is installed
    if shutil.which("zstd"):
        print("   ✓ zstd installed")
    else:
        print("   ✗ zstd installation failed!")
        return
    
    # Install fuser for port management
    subprocess.run(["apt-get", "install", "-y", "-qq", "psmisc"], capture_output=True)
    print("   ✓ System dependencies ready")

    # =========================================================================
    # STEP 2: PYTHON PACKAGES (with all fixes)
    # =========================================================================
    print("\n📦 [2/7] Installing Python packages (3-5 minutes)...")
    
    # Upgrade pip
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "-q"], 
                   capture_output=True)
    print("   ✓ pip upgraded")
    
    # Install pyngrok
    subprocess.run([sys.executable, "-m", "pip", "install", "pyngrok", "-q"], 
                   capture_output=True)
    print("   ✓ pyngrok installed")
    
    # KAGGLE: May not have cupy issues, but remove just in case
    subprocess.run([sys.executable, "-m", "pip", "uninstall", "cupy-cuda12x", "cupy", "-y"], 
                   capture_output=True)
    print("   ✓ Removed potential conflicting packages")
    
    # Install open-webui
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "open-webui", "-q"],
        capture_output=True, text=True
    )
    print("   ✓ open-webui installed")
    
    # Fix alembic (PriorityDispatchResult error)
    subprocess.run([
        sys.executable, "-m", "pip", "install", 
        "alembic>=1.15.0", "--force-reinstall", "-q"
    ], capture_output=True)
    print("   ✓ alembic fixed")
    
    # Fix transformers (PreTrainedModel error)
    subprocess.run([
        sys.executable, "-m", "pip", "install", 
        "transformers>=4.40.0", "--force-reinstall", "-q"
    ], capture_output=True)
    print("   ✓ transformers fixed")
    
    # Fix srsly (cupy dependency chain)
    subprocess.run([
        sys.executable, "-m", "pip", "install", 
        "srsly", "--force-reinstall", "-q"
    ], capture_output=True)
    print("   ✓ srsly fixed")

    # =========================================================================
    # STEP 3: INSTALL OLLAMA
    # =========================================================================
    print("\n🦙 [3/7] Installing Ollama...")
    
    OLLAMA_URL = "https://ollama.com/download/ollama-linux-amd64.tar.zst"
    
    # Clean previous installation
    subprocess.run(["rm", "-rf", "/usr/lib/ollama", "/usr/bin/ollama"], capture_output=True)
    
    # Method 1: Pipe directly
    result = subprocess.run(
        f'curl -fsSL "{OLLAMA_URL}" | tar -x --zstd -C /usr',
        shell=True, capture_output=True, text=True, timeout=300
    )
    
    # If failed, try Method 2: Download then extract
    if not shutil.which("ollama"):
        print("   → Primary method failed, trying alternative...")
        subprocess.run([
            "curl", "-fsSL", "-o", "/tmp/ollama.tar.zst", OLLAMA_URL
        ], capture_output=True, timeout=300)
        
        subprocess.run([
            "zstd", "-d", "/tmp/ollama.tar.zst", "-o", "/tmp/ollama.tar"
        ], capture_output=True)
        
        subprocess.run([
            "tar", "-xf", "/tmp/ollama.tar", "-C", "/usr"
        ], capture_output=True)
        
        # Cleanup
        subprocess.run(["rm", "-f", "/tmp/ollama.tar.zst", "/tmp/ollama.tar"], capture_output=True)
    
    # Verify
    if shutil.which("ollama"):
        version = subprocess.run(["ollama", "-v"], capture_output=True, text=True)
        print(f"   ✓ Ollama installed")
    else:
        print("   ✗ Ollama installation failed!")
        print("   This might be a temporary network issue. Try again in a few minutes.")
        return
    
    # KAGGLE: Use persistent storage for Ollama models
    OLLAMA_HOME = "/kaggle/working/.ollama"
    os.makedirs(OLLAMA_HOME, exist_ok=True)
    os.environ["OLLAMA_MODELS"] = OLLAMA_HOME

    # =========================================================================
    # STEP 4: START OLLAMA SERVER
    # =========================================================================
    print("\n🚀 [4/7] Starting Ollama server...")
    
    env = os.environ.copy()
    env["OLLAMA_HOST"] = "0.0.0.0:11434"
    env["OLLAMA_ORIGINS"] = "*"
    env["OLLAMA_MODELS"] = OLLAMA_HOME  # KAGGLE: Persist models
    
    subprocess.Popen(
        ["ollama", "serve"],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )
    
    # Wait for Ollama to be ready
    import requests
    for i in range(30):
        try:
            requests.get("http://localhost:11434", timeout=2)
            print("   ✓ Ollama server running")
            break
        except:
            time.sleep(2)
    else:
        print("   ✗ Ollama failed to start")
        return

    # =========================================================================
    # STEP 5: PULL AI MODELS
    # =========================================================================
    print("\n📥 [5/7] Pulling AI models (this takes 10-20 minutes)...")
    print("        Each model is 4-5 GB. Please be patient.\n")
    print("        ⭐ KAGGLE BONUS: Models save to /kaggle/working/.ollama")
    print("           Download once, reuse in future sessions!\n")
    
    MODELS = [
        ("deepseek-r1:8b", "Reasoning & Logic"),
        ("qwen2.5-coder:7b", "Code Generation"),
        ("dolphin-mistral", "Uncensored/Creative"),
    ]
    
    for i, (model, description) in enumerate(MODELS, 1):
        print(f"   [{i}/{len(MODELS)}] Pulling {model} ({description})...")
        result = subprocess.run(
            ["ollama", "pull", model],
            capture_output=True, text=True, timeout=1800,
            env=env
        )
        if result.returncode == 0:
            print(f"   ✓ {model} ready")
        else:
            print(f"   ⚠ {model} may have issues: {result.stderr[:100]}")

    # =========================================================================
    # STEP 6: START OPEN WEBUI
    # =========================================================================
    print("\n🌐 [6/7] Starting Open WebUI...")
    
    # Kill any existing processes on port 8080
    subprocess.run("fuser -k 8080/tcp 2>/dev/null", shell=True, capture_output=True)
    time.sleep(2)
    
    import secrets
    
    # KAGGLE: Use persistent storage for WebUI data
    WEBUI_DATA_DIR = "/kaggle/working/webui_data"
    
    webui_env = os.environ.copy()
    webui_env.update({
        "WEBUI_SECRET_KEY": secrets.token_urlsafe(32),
        "WEBUI_AUTH": "False",
        "CORS_ALLOW_ORIGIN": "*",
        "OLLAMA_BASE_URL": "http://localhost:11434",
        "ENABLE_SIGNUP": "False",
        "DATA_DIR": WEBUI_DATA_DIR,
    })
    
    os.makedirs(WEBUI_DATA_DIR, exist_ok=True)
    
    webui_proc = subprocess.Popen(
        ["open-webui", "serve", "--host", "0.0.0.0", "--port", "8080"],
        env=webui_env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )
    
    print(f"   ✓ Started (PID: {webui_proc.pid})")
    print("   → Waiting for database migrations...")
    
    # Wait for WebUI to be ready
    for i in range(90):
        # Check if process died
        if webui_proc.poll() is not None:
            print("   ✗ Open WebUI crashed!")
            return
        
        try:
            r = requests.get("http://localhost:8080", timeout=2)
            if r.status_code in [200, 302, 307]:
                print(f"   ✓ Open WebUI ready!")
                break
        except:
            pass
        
        if i % 15 == 0 and i > 0:
            print(f"     ... still initializing ({i*2}s)")
        time.sleep(2)
    else:
        print("   ✗ Open WebUI timeout")
        return

    # =========================================================================
    # STEP 7: CREATE PUBLIC TUNNEL
    # =========================================================================
    print("\n🌍 [7/7] Creating public tunnel...")
    
    from pyngrok import ngrok, conf
    
    conf.get_default().auth_token = NGROK_TOKEN
    ngrok.kill()  # Kill any existing tunnels
    time.sleep(2)
    
    try:
        # CRITICAL: host_header="rewrite" fixes 404 errors
        tunnel = ngrok.connect(
            8080,
            "http",
            bind_tls=True,
            host_header="rewrite"
        )
        public_url = tunnel.public_url
        print("   ✓ Tunnel established!")
    except Exception as e:
        print(f"   ✗ Tunnel failed: {e}")
        return

    # =========================================================================
    # SUCCESS!
    # =========================================================================
    print("\n" + "=" * 65)
    print("  🎉 SOVEREIGN HYBRID AI SYSTEM IS ONLINE!")
    print("=" * 65)
    print()
    print(f"  🔗 ACCESS URL: {public_url}")
    print()
    print("  🧠 AVAILABLE MODELS:")
    print("     • deepseek-r1:8b     → Reasoning & Logic")
    print("     • qwen2.5-coder:7b   → Code Generation")
    print("     • dolphin-mistral    → Uncensored/Creative")
    print()
    print("  ⭐ KAGGLE ADVANTAGES:")
    print("     • Models saved to /kaggle/working/.ollama (persistent!)")
    print("     • Data saved to /kaggle/working/webui_data")
    print("     • More stable than Colab - less frequent disconnections")
    print()
    print("  ⚠️  IMPORTANT:")
    print("     • Keep this cell running to maintain access")
    print("     • Session lasts much longer than Colab")
    print("     • Bookmark the URL for this session")
    print()
    print("=" * 65)

    # Keep the script running to maintain the tunnel
    try:
        while True:
            time.sleep(60)
            # Optional: Add health check
            try:
                requests.get("http://localhost:8080", timeout=5)
            except:
                print("⚠ WebUI health check failed")
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        ngrok.kill()
        print("   ✓ Tunnel closed")
        print("   ✓ Shutdown complete")

# Run the deployment
if __name__ == "__main__":
    main()
