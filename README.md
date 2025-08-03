🧠 AI-Powered-Lead-Scoring-Automation
🚀 Overview
This project demonstrates my ability to build a functional AI agent using n8n, a powerful automation tool. The agent automatically processes incoming leads from Google Sheets, scores them using OpenAI, and takes conditional actions such as sending alerts and updating records.

🎯 Purpose
To streamline the lead qualification process by:

Scoring incoming leads based on job title, company, and domain.

Automatically notifying relevant stakeholders of high-quality leads.

Maintaining a live, updated Google Sheet with lead statuses.

🔧 Key Features
Automated Lead Intake
Triggered by a Google Sheet update.

OpenAI-Powered Scoring System
Uses OpenAI to evaluate lead quality on a 0–100 scale based on predefined rules.

Conditional Actions
If the score > 70:

Apply Gmail label "IMPORTANT".

Send a notification email.

Append or update the lead in the same sheet.

Memory + Toolchain Integration
Uses n8n’s memory and Google Calendar tool integration to simulate interactive AI agent behavior.

🧩 Workflow Components
Node	Description
Google Sheets Trigger	Detects new leads in real-time.
Agent (Langchain)	Guides user through setup steps, ensures proper memory and tool configuration.
OpenAI Model	Scores the lead with quality evaluation logic.
If Node	Checks if score > 70.
Gmail (Add Label & Send)	Flags and notifies for high-quality leads.
Google Sheets Append/Update	Stores processed data for tracking.

🛠️ Tech Stack
n8n

OpenAI API

Google Sheets API

Gmail API

📂 File
AI-Powered-Lead-Scoring-Automation.json
This is the complete workflow that can be imported directly into an n8n instance.

💡 Why This Project Matters
This project proves I can:

Work with automation platforms like n8n.

Integrate APIs and tools seamlessly.

Build intelligent workflows with real-world impact.

Follow conditional logic and apply AI in a practical, business-focused setting.

✅ How to Use
Import the workflow into your n8n environment.

Connect your OpenAI, Google Sheets, and Gmail accounts.

Set up a Google Sheet with new leads.

Watch the agent analyze and act on leads autonomously!

