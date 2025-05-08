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
git clone https://github.com/RanaAkshat/threat_monitor.git
cd threat_monitor
```

# Backend Setup (Django)

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
On Windows: .\venv\Scripts\activate
pip install fastapi uvicorn
pip install pandas

Your backend will now be running at:           (pip install pandas - needed )
http://127.0.0.1:8000/api/threats

 # Frontend Setup (React)

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
