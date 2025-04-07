
# 📊 Salesforce CSV Analysis Dashboard

This project is a secure, interactive **Streamlit dashboard** designed to analyze Salesforce lead data. It provides response time metrics, conversion performance, media channel quality, and CRM insights.

Built for internal marketing and CRM teams, this dashboard helps evaluate lead handling efficiency and identify high-quality lead sources.

---

## 🚀 Features

- 🔐 **Password Protected** access
- 📁 Upload **raw Salesforce CSV** to generate automatic insights
- 🔁 Upload **conversion match CSV** to auto-tag leads as “Converted”
- 🧠 Calculates:
  - Response time (Real-time & Ramadan timing)
  - Conversion rates per owner
  - Media channel lead quality
  - Weekly lead volume trends
- ✅ **Highlights matched leads** with explanation of how they matched
- 📦 Download CSV of matched & converted leads
- 📱 Fully interactive filters by:
  - Media Channel
  - Media Source
  - Stage
  - Opportunity Owner

---

## 📂 File Requirements

### 1. **Main CSV – Raw Export from Salesforce**

This CSV should include the following **required columns**:

| Column Name                | Description                           |
|---------------------------|---------------------------------------|
| OpportunityId             | Unique identifier                     |
| Data Load ID              | Internal reference                    |
| Lead Id                   | Salesforce lead ID                    |
| Opportunity Name          | Name of the opportunity               |
| Opportunity Record Type   | Type of opportunity                   |
| Primary Contact           | Lead contact name                     |
| Created Date              | When the opportunity was created      |
| Contacted Date            | When the lead was contacted           |
| Assigned Date             | Assignment date                       |
| Account Name              | Customer account                      |
| Purchase Horizon          | Intent timing                         |
| Brand                     | Product brand                         |
| Model                     | Product model                         |
| Model Name                | Specific model name                   |
| BAC Code                  | Internal code                         |
| Primary Contact Mobile    | Mobile number                         |
| Primary Contact Email     | Email address                         |
| Primary Contact Phone     | Phone number                          |
| Stage                     | Lead status                           |
| Sub Stage                 | Detailed stage                        |
| Form Website              | Lead form source                      |
| Customer Comment          | Optional comments                     |
| Media Channel             | General media source (e.g. Facebook)  |
| Media Source              | Specific campaign/source              |
| Lead Source               | Original source channel               |
| Lead Enquiry Type         | Type of lead (e.g. Sales, Service)    |
| Lead Source Details       | Additional lead metadata              |
| Primary Campaign Source Id| Campaign source                       |
| Opportunity Owner         | Assigned CRM agent                    |
| Billing Country           | Country info                          |
| Created By                | CRM user who created it               |
| Last Modified By          | Last user who modified the record     |
| Last Modified Date        | Timestamp of last update              |
| Product Name              | Product associated                    |
| Account Record Type       | Type of customer                      |
| VIN                       | Vehicle ID Number                     |
| Email Opt Out             | Opt-out status                        |

> 📝 **Note**: `Created Date` and `Contacted Date` must be in a date format (dd/mm/yyyy or similar).

---

### 2. **Conversion Match CSV (Optional)**

This file marks entries as “Converted” by matching leads based on:

| Column Name               | Description                   |
|--------------------------|-------------------------------|
| Primary Contact Mobile   | Match on **last 6 digits**    |
| Primary Contact Email    | **Case-insensitive full match** |
| Primary Contact Phone    | Match on **last 6 digits**    |

> If a record in the main CSV matches any of the above in this file, it is tagged as `Converted` and the method is shown in the `Matched By` column.

---

## 🧮 Metrics & Calculations

- **Avg Opportunities per Day & Week**
- **Real-Time Response Time** in hours/days
- **Ramadan Response Time** (Mon–Fri, 9AM–3PM)
- **% of Interested Leads** (Converted, Deciding, Experiencing)
- **Total Converted Opportunities**
- **Lead Quality by Media Channel & Sub-Stage**
- **Opportunity Owner Performance & Conversion Rates**

---

## 🎯 Getting Started

1. Clone the repo:
   ```bash
   git clone https://github.com/your-org/salesforce-csv-analysis.git
   cd salesforce-csv-analysis
   ```

2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

4. Access it in your browser and **use the password `Mm@872932`** when prompted.

---

## 🔒 Security

- The dashboard is **password protected**
- CSV files are processed only in memory
- No data is stored after upload

---

## 📦 Included Files

- `app.py` – main dashboard logic
- `requirements.txt` – list of dependencies
- `README.md` – this file
