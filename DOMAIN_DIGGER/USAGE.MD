# 🚀 QUICK START
python domain_digger.py your_domain

# 📋 BASIC SCANS
python domain_digger.py your_domain
python domain_digger.py your_domain --workers 50
python domain_digger.py your_domain --counter 50000
python domain_digger.py your_domain --output your_domain_results.json

# ⚡ ADVANCED SCANS
python domain_digger.py your_domain --workers 100 --counter 100000
python domain_digger.py your_domain --workers 50 --batch 10000
python domain_digger.py your_domain --workers 200 --counter 500000 --output your_domain_found.json

# 🎯 QUICK SCANS
python domain_digger.py your_domain --workers 30 --counter 10000
python domain_digger.py your_domain --workers 75 --counter 25000
python domain_digger.py your_domain --workers 50 --counter 5000 --batch 2000

# 💥 MAX POWER SCANS
python domain_digger.py your_domain --workers 250 --counter 1000000 --batch 50000
python domain_digger.py your_domain --workers 150 --counter 750000 --output your_domain_full.json

# 🌐 REAL-WORLD EXAMPLES

# Social Media Platforms
python domain_digger.py twitter --counter 50000 --workers 100
python domain_digger.io instagram --counter 75000 --workers 150
python domain_digger.py linkedin --counter 30000 --workers 80

# E-commerce Sites
python domain_digger.py ebay --counter 60000 --workers 120 --output ebay_found.json
python domain_digger.py alibaba --counter 100000 --workers 200
python domain_digger.io shopify --counter 40000 --workers 100

# Tech Companies
python domain_digger.py github --counter 35000 --workers 90
python domain_digger.py slack --counter 25000 --workers 70
python domain_digger.io zoom --counter 45000 --workers 110

# Financial Services
python domain_digger.py stripe --counter 30000 --workers 85
python domain_digger.py paypal --counter 80000 --workers 180
python domain_digger.io coinbase --counter 20000 --workers 60

# Streaming Services
python domain_digger.py netflix --counter 100000 --workers 150
python domain_digger.io spotify --counter 60000 --workers 120
python domain_digger.py disney --counter 40000 --workers 100

# Cloud Providers
python domain_digger.py aws --counter 50000 --workers 100
python domain_digger.io azure --counter 30000 --workers 80
python domain_digger.py googlecloud --counter 70000 --workers 160

# Gaming Platforms
python domain_digger.py steam --counter 25000 --workers 70
python domain_digger.io epicgames --counter 35000 --workers 90
python domain_digger.py xbox --counter 20000 --workers 60

# 🎪 SPECIALIZED SCANS

# Quick Test (1 minute)
python domain_digger.py test --counter 1000 --workers 10 --batch 500

# Medium Investigation (5 minutes)
python domain_digger.py target --counter 20000 --workers 50 --batch 5000

# Deep Investigation (30+ minutes)
python domain_digger.py target --counter 200000 --workers 150 --batch 20000 --output deep_scan.json

# 💡 PRO TIPS
# 1. Press Ctrl+C anytime for instant exit
# 2. Results auto-save to JSON files
# 3. Higher workers = faster but more CPU/RAM
# 4. Use --output to save with custom filename
# 5. .io extension often works for tech companies

# 🛑 EXIT & RECOVERY
# Ctrl+C = Immediate exit with progress save
# Files saved: target_scan_progress.json
# Interrupted scans: target_interrupted.json
# Final results: target_scan_YYYYMMDD_HHMMSS.json
