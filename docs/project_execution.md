
Use this final path first:

cd E:\Intership\PRESAGE-09
Option 1: Full integrated app
This is the best way for your demo.

Install backend dependencies:
python -m pip install -r requirements.txt
Install frontend dependencies:
D:\Nodejs\Nodejs\npm.cmd --prefix frontend install
Build the frontend:
D:\Nodejs\Nodejs\npm.cmd --prefix frontend run build
Start the backend:
python app.py
Open in browser:
http://localhost:5000
What you will see:

Landing page
Click logo/button
Main Presage workspace
Sidebar with modules
Overview, Incidents, Telemetry, Attack Center
Module pages for each attack
How to see it working:

Open Overview
Open Telemetry
Open Attack Center
Run one attack
Go to Incidents
See the new incident appear
For high severity attacks, status should move to Under Investigation
Option 2: Frontend dev mode
Use this if you want React hot reload.

Terminal 1:

cd E:\Intership\PRESAGE-09
python app.py
Terminal 2:

cd E:\Intership\PRESAGE-09\frontend
npm run start
Then open:

http://localhost:5173
Backend API will still run from:

http://localhost:5000
Optional CLI mode
If you want terminal-based attack triggering:

cd E:\Intership\PRESAGE-09
python siem.py
Quick test commands
Backend health:

python -c "from app import app; c=app.test_client(); print(c.get('/api/health').status_code); print(c.get('/api/state').status_code)"
Frontend build test:

D:\Nodejs\Nodejs\npm.cmd --prefix frontend run build
Best demo flow

Start app with python app.py
Open http://localhost:5000
Enter workspace
Show Overview
Show Telemetry
Run Brute Force or Windows Failed Logon
Open Incidents
Explain alert, incident, and playbook response
If you want, I can next give you a very short “what to say while demoing” script.


what is the difference between both option 

The difference is mainly how the frontend is served.

Option 1: Full integrated app

React frontend is built first
Flask serves the built frontend from frontend/dist
you open everything on http://localhost:5000
Use this when:

you want the final demo flow
you want one main app
you want the same behavior as presentation/submission mode
Good for:

project demo
final review
showing the working product
Option 2: Frontend dev mode

Flask backend runs separately
React runs on Vite dev server
frontend opens on http://localhost:5173
backend API stays on http://localhost:5000
Use this when:

you are editing frontend code
you want instant React hot reload
you are developing UI faster
Good for:

frontend development
UI changes
live React editing
In simple words

Option 1 = final product mode
Option 2 = developer mode
For you right now

use Option 1 for presentation and checking the full working model
use Option 2 only when you want to keep changing the React UI quickly