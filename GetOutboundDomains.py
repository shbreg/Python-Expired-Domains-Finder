import requests
import csv
import time
import re
from urllib.parse import quote
import json
from io import StringIO

SEMRUSH_KEY = "API_KEY"
DEPTH_DOMAINS = 100

CATEGORY = "Food Recipes"
COUNTRY = "United States" #Keep empty for worldwide

def extract_json_array(text):
    match = re.search(r'(\[.*?\])', text, re.DOTALL)
    if match:
        return json.loads(match.group(1))
    else:
        raise ValueError("No JSON array found")

def getTopWebsites():
    for x in range(10):
        try:
            prompt = """Give me the top """ + str(DEPTH_DOMAINS) + """ websites """ + ("worldwide" if COUNTRY=="" else "in this country `" + COUNTRY + "`") + """, in this category `""" + CATEGORY + """`
IMPORTANT NOTICES :
- Do not write anything else
- Return the value as a json because it will be automatically json decoded"""
            response = requests.get("https://text.pollinations.ai/" + quote(prompt) + "?model=openai")
            topWebsites = response.text.replace("```json", "").replace("```", "")
            return extract_json_array(topWebsites)
        except Exception as exp:
            print("Top Websites Error: ", exp)
            time.sleep(1)

def extractDomainsFromCSV(csv_content):
    domains = []
    reader = csv.DictReader(StringIO(csv_content))
    for row in reader:
        domains.append(row['Domain'])
    return domains

def getOutboundDomains(domain):
    try:
        url = "https://www.semrush.com/backlinks/webapi2/"
        params = {
            "action": "export",
            "key": SEMRUSH_KEY,
            "type": "backlinks_outgoing_domains",
            "export_columns": "domain_ascore,domain,links_num,first_seen,last_seen",
            "target": domain,
            "target_type": "root_domain",
            "export": "csv",
            "display_filter": "",
            "sort_field": "links_num",
            "sort_type": "desc"
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            domains = extractDomainsFromCSV(response.text)
            return domains
        else:
            print(f"GetOutboundDomains Error: {response.status_code}")
            print(response.text)
            return False
    except Exception as exp:
        print("GetOutboundDomains Errors", exp)

def main():
    outboundDomainsList = []
    topWebsites = getTopWebsites()
    if topWebsites:
        print("Top Websites generated")
        for website in topWebsites:
            outboundDomains = getOutboundDomains(website)
            if outboundDomains:
                print("Outbound domains generated for website %s" % (website))
                for a in outboundDomains:
                    outboundDomainsList.append(a)
    outboundDomainsList = list(dict.fromkeys(outboundDomainsList))
    open("outBoundDomains.txt", "w", encoding="utf8").write("\n".join(outboundDomainsList))

if __name__ == "__main__":
    main()