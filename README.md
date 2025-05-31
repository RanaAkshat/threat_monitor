# 🛡️ Threat Monitor - AI-Based Social Media Crime Detection Dashboard
An AI-powered full-stack web application that monitors and detects online threats like hate speech, cyberbullying, fake accounts, and public safety risks across social media platforms like Twitter, YouTube, and Instagram — now enhanced with real-time WhatsApp alerting and Dockerized deployment.

# live demo - https://threat-monitor-u6gy.vercel.app/
# Youtube link - https://youtu.be/TFEXHVwIhY8
# ppt - https://www.canva.com/design/DAGo5ojhv_c/-HnoPRs-Qw96CE56atSEUg/edit?utm_content=DAGo5ojhv_c&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

🚀 Key Features
🔁 Auto-refreshing dashboard (every 10 seconds)

📊 Threat Categorization Engine using NLP

⚠️ Live Alert Panel with WhatsApp integration (via Twilio)

📈 Trend Analysis via interactive charts and stats

📤 Export Reports to CSV and PDF

🐳 One-Command Docker Deployment

📱 Modular social media ingestion (Twitter, YouTube, Instagram ready)

# 🧠 Tech Stack
Layer                      |                  Tech Used
___________________________|______________________________________
Frontend                   |          	React.js + Tailwind CSS
Backend	                   |                 FastAPI 
Alerts                     |      	Twilio WhatsApp API + Python
Database                   |                 Pandas + CSV
Deployment                 |          	Docker, Docker Compose

# 🐳 Run the App with One Command

- First time (build + run)
docker compose up --build
- Subsequent runs
docker compose up
- Stop all containers
docker compose down

# Access the App
Frontend: http://localhost:8080/
Backend API: http://localhost:8000/api/threats

# 🛠️ Manual Setup (Dev Mode)

📁 Clone the Repo
git clone --recurse-submodules https://github.com/RanaAkshat/threat_monitor.git
cd threat_monitor

# 🧪 Backend (FastAPI)

cd api
pip install -r requirements.txt
uvicorn server:app --reload --port 8000
Runs at: http://127.0.0.1:8000/api/threats

# 💻 Frontend (React + Vite)

cd frontend
npm install --legacy-peer-deps
npm run dev
Runs at: http://localhost:8080/

# 🔔 Alert System (Twilio WhatsApp Alerts)

cd alerts
(Make sure .env is configured with your Twilio credentials)
python alert_system.py

# 🧪 Example Auto-Refresh Logic (Frontend)

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


# 👨‍💻 Author

Name: Akshat Rana
GitHub: @RanaAkshat

