# ESIC_Matching_Tool

# 🧾 ESIC Contribution Matching Tool (Gradio Web App)

A Python-based web utility to automate and validate **ESIC contribution reconciliation** between internal HR Annexure sheets and official ESIC Portal exports.

This app leverages **Gradio** for a lightweight web interface, designed for HR/Compliance teams to quickly upload and match records, and to download flagged mismatches in `.xlsx` format for audit or correction.

---

## 📌 Problem Statement

Manual ESIC matching is:
- Time-consuming ⚙️
- Prone to human error ❌
- Unscalable across multiple locations 🧭

This tool streamlines the comparison of:
- `ESIC No.` (unique employee identifier)
- `Employee Contribution @ 0.75%`

across the two primary data sources:
1. **Annexure Report** (Internal HR-generated Excel)
2. **Portal Export** (ESIC.gov.in contribution report)

---

## 🔧 Tech Stack

| Layer         | Tool/Framework       | Purpose                                     |
|---------------|----------------------|---------------------------------------------|
| UI            | Gradio               | File upload, UI logic, result preview       |
| Backend Logic | Pandas + OpenPyXL    | Excel parsing, matching, numeric comparison |
| Temp I/O      | Python `tempfile`    | Stores comparison result for download       |
| Frontend Host | Hugging Face / Local | Hosting (Optional Deployment Layer)         |

---

## 🗂️ File Structure




---

## ⚙️ Core Logic Overview

> 📍 Located in `esic_tool_gradio.py > match_esic_contributions()`

**Workflow:**
1. Skip header rows (2 for Annexure, 9 for Portal)
2. Auto-detect ESIC No. and contribution columns (uses fuzzy keyword detection)
3. Merge both sheets on ESIC No.
4. Normalize and round contributions to 2 decimal places
5. Flag exact matches and mismatches
6. Write comparison results to a temp Excel file
7. Return human-readable summary + download link

```python
comparison_df['Match'] = comparison_df['ANNEXURE_CONTRIB'] == comparison_df['IPContribution']



Running the Application

# Step 1: Clone
git clone https://github.com/your-org/esic-matching-tool.git
cd esic-matching-tool

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Launch app
python esic_tool_gradio.py

🧪 Sample Inputs (Dev Testing)
Place these in /samples directory (not included here)

Book1.xlsx (Annexure)

ContributionData.xlsx (ESIC Portal Export)

These test files simulate a realistic mismatch scenario with 25 records and 3 deltas.

🧑‍💻 Hosting Options
Platform	Notes
🧠 Hugging Face Spaces	Recommended for MVP/testing (free)
🔒 PythonAnywhere	Better for password-protected internal tools
🏢 Custom VPS (EC2)	Use Gunicorn + Nginx + Docker for production

🛡️ Data Security Notes
No files are stored persistently. All uploads use tempfile.NamedTemporaryFile() and are wiped after runtime.

For sensitive production deployment, consider:

HTTPS + Auth Layer (Flask/FastAPI wrapper)

Local-only deployment via LAN access

Containerize via Docker

📥 API Extension (Future-Ready)
You can wrap the core logic into a FastAPI endpoint like so:

python
Copy code
@app.post("/match")
def match(annexure: UploadFile, portal: UploadFile):
    # Call logic.match_esic_contributions()
    ...
This would allow:

Integration with internal dashboards

CLI / batch-mode operation

Scheduled jobs with cron + webhook callbacks

🔗 Credits
Code: Ishant (Intern, Murti Supply Chain Solutions)

Mentorship: Aditi Kaushik, Digitalpreneur & Automation Strategist

Frameworks Used: Gradio, Pandas, OpenPyXL

🧭 Roadmap Ideas
 Add email notifications for mismatches

 Upload CSV support

 Track monthly stats for audit trail

 Convert into desktop .exe using PyInstaller

📜 License
Internal tool. Use at your own risk. For production deployments, consider reviewing ESIC compliance regulations and IT Act 2000 (India) for data storage and sharing.
