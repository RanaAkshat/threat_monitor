# 🛡️ Threat Monitor - AI Based Social Media Crime Detection Dashboard

An AI-powered full-stack web application for monitoring and detecting threats like hate speech, cyberbullying, fake accounts, and public safety risks across social media platforms.

## 🧠 Tech Stack

- **Frontend:** React.js + Tailwind CSS
- **Backend:** Django + Django REST Framework
- **Database:** SQLite (or your choice)
- **Visualization:** Charts, Tables, Stats (React components)
- **Deployment:** Localhost (for now)

---

## 🚀 Features

- 🔁 Real-time data refresh every 10 seconds
- 📊 Threat categorization dashboard
- ⚠️ Alert panel for live monitoring
- 📈 Graphs for trends and threat types
- 🧾 Exportable reports (CSV, PDF)

---

## 🛠️ Setup Instructions

### 📁 1. Clone the repository

```bash
git clone --recurse-submodules https://github.com/RanaAkshat/threat_monitor.git
cd threat_monitor
```

# Backend Setup (Django)
# for windows
pip install -r requirements.txt
.\venv\Scripts\activate
pip install fastapi uvicorn
pip install pandas

Your backend will now be running at:           (pip install pandas - needed )
http://127.0.0.1:8000/api/threats

# for mac
pip install -r requirements.txt
source venv/bin/activate
pip install fastapi uvicorn
pip install pandas



 # Frontend Setup (React)
 
# windows
uvicorn is used .
Frontend Setup (React) cd ../frontend # or wherever your React app is
for this you have to open two windows in powershell and run commands simultaneously
in window 1 , where you are in...
(\__\__\threat_monitor)  - run this command - uvicorn api.server:app --reload 
in window 2 , where you are in ...
(\__\__\frontend) - run this commands
npm install 
npm run dev
Visit the dashboard at:
http://localhost:8080/

# mac
in window 1 of powershell :
cd frontend
npm install --no-optional --loglevel=error
npm run dev
pip install fastapi uvicorn
pip install pandas
uvicorn api.server:app --reload
In your frontend directory, run:
rm -rf node_modules package-lock.json
npm cache clean --force
npm install --no-optional
npm install @rollup/rollup-darwin-arm64
npm run build
npx serve dist
now frontend is ssuccseful

# now check backend is working or not
cd api
uvicorn server:app --reload
uvicorn server:app --reload --port 8080
lsof -i :8080
curl http://localhost:8080/api/threats
now go to : http://localhost:8080/api/threats

#  Auto-Refresh Logic
useEffect(() => {
  const loadData = async () => {
    const data = await fetchThreats();
    setThreats(data);
    setLoading(false);
  };

  loadData();
  const interval = setInterval(loadData, 10000);
  return () => clearInterval(interval);
}, []);

Author
Name: Akshat Rana
GitHub: @RanaAkshat
