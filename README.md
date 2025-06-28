# 🔍 Outbound & Expired Domains Finder

Created by **S Amine (Shbreg)**

---

## 🚀 Overview

This toolset automates finding **expired domains** by:

1. Fetching the **top N websites** in a specified **category** and **country**, then extracting all their **outbound domains**.
2. Scanning those outbound domains to find which ones are **expired**, so you can capture valuable dropped domains.

It is split into **two Python scripts**:

* `GetOutboundDomains.py`: Fetches top websites, gets their outbound domains, and saves them into `outBoundDomains.txt`.
* `GetExpiredDomains.py`: Checks each outbound domain to see if it is expired, then saves expired ones into `ExpiredDomains.txt`.

---

## 📂 Files

* `GetOutboundDomains.py`
  🔸 Grabs top websites and extracts all their outbound links.

* `GetExpiredDomains.py`
  🔸 Reads `outBoundDomains.txt`, checks which domains are expired, and writes them into `ExpiredDomains.txt`.

---

## ⚙️ Setup

### 1️⃣ Install requirements

Make sure you have Python 3.7+ installed.

```bash
pip install -r requirements.txt
```

---

## ✍️ Configuration

Before running `GetOutboundDomains.py`, you need to edit **four variables** at the top of the script:

```python
SEMRUSH_KEY = ""
DEPTH_DOMAINS = 100
CATEGORY = "Food Recipes"
COUNTRY = "United States"
```

### 🔑 How to get your SEMrush API Key

1. Go to: [https://www.semrush.com/projects/](https://www.semrush.com/projects/)
2. Open Developer Console in your browser (usually F12).
3. Paste:

```javascript
window.sm2.user.api_key
```

4. Copy the key it prints, then paste into your `SEMRUSH_KEY` in the script.

---

## 🚀 How it works

### 🔍 Step 1: Get outbound domains

Run:

```bash
python GetOutboundDomains.py
```

* It will:

  * Fetch the **top `DEPTH_DOMAINS` websites** for the `CATEGORY` and `COUNTRY`.
  * Extract all their outbound domains (links pointing to other domains).
  * Save the list to `outBoundDomains.txt`.

---

### ⏳ Step 2: Find expired domains

Run:

```bash
python GetExpiredDomains.py
```

* It will:

  * Read `outBoundDomains.txt`.
  * Check each domain to see if it is expired / available for registration.
  * Save all expired domains into `ExpiredDomains.txt`.

---

## 📝 Example use case

* Say you want to find expired domains that were linked from **top Food Recipes websites in the United States**.
* You set:

```python
CATEGORY = "Food Recipes"
COUNTRY = "United States"
DEPTH_DOMAINS = 100
```

* The tool will:

  * Get the top 100 sites.
  * Extract thousands of outbound links.
  * Then identify which of those domains are expired so you can buy them.

---

## 🧑‍💻 Author

Made with passion by **S Amine (Shbreg)**.

---

✅ **Ready to use:**
Just adjust your variables in `GetOutboundDomains.py`, install the requirements, and run the scripts.
