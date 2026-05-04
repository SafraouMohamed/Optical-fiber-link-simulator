# GitHub Upload Instructions

## Files to Upload (just these 2 files needed):

```
optical_simulator/
├── index.html    ← Main file (open in browser!)
└── README.md   ← Documentation
```

## Commands to Push to GitHub:

```powershell
# 1. Go to folder
cd "C:\Users\moham\OneDrive\Documents\TP Optique\TP 3\optical_simulator"

# 2. Initialize git (if not already)
git init

# 3. Add files
git add index.html README.md

# 4. Commit
git commit -m "Optical fiber link simulator - Prof. BAHLOUL ENIT"

# 5. Create repo on GitHub.com first, then copy the URL
# Example: https://github.com/USERNAME/optical-simulator.git

# 6. Add remote (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/optical-simulator.git

# 7. Push
git push -u origin main
```

## OR - Quick Upload Without Git:

1. Go to: https://github.com/new
2. Create repo named: `optical-simulator`
3. Make it **Public**
4. Click "uploading an existing file"
5. Drag & drop only `index.html` (done!)

---

**Done!** Your colleagues can now open `index.html` directly in their browser!

## Share Link Example:
```
https://username.github.io/optical-simulator/index.html
```