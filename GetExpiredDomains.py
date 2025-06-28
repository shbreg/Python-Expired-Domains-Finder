import whois
import concurrent.futures
from datetime import datetime
import time
import tldextract
from collections import OrderedDict

extractor = tldextract.TLDExtract()

def get_base_domain(domain):
    extracted = extractor(domain)
    if not extracted.suffix:
        return domain
    return f"{extracted.domain}.{extracted.suffix}"

def is_domain_expired(domain):
    try:
        w = whois.whois(domain)
        if w.expiration_date:
            if isinstance(w.expiration_date, list):
                expiry = w.expiration_date[0]
            else:
                expiry = w.expiration_date
            if expiry and expiry < datetime.now():
                return True
        return False
    except (whois.parser.PywhoisError, ConnectionResetError):
        return True
    except Exception as e:
        print(f"Error checking {domain}: {str(e)}")
        return False

def main():
    try:
        with open('outBoundDomains.txt', 'r', encoding="utf8") as file:
            raw_domains = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print("Error: outBoundDomains.txt not found in current directory")
        return

    base_domains = OrderedDict()
    for domain in raw_domains:
        base = get_base_domain(domain)
        if base not in base_domains:
            base_domains[base] = True

    print(f"Processing {len(base_domains)} unique base domains...")
    start_time = time.time()

    with open('ExpiredDomains.txt', 'w', encoding="utf8") as expired_file:
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            future_to_domain = {}
            for domain in base_domains:
                future = executor.submit(is_domain_expired, domain)
                future_to_domain[future] = domain
            for future in concurrent.futures.as_completed(future_to_domain):
                domain = future_to_domain[future]
                try:
                    if future.result():
                        expired_file.write(domain + '\n')
                        expired_file.flush()
                        print(f"EXPIRED: {domain}")
                    else:
                        print(f"active: {domain}")
                except Exception as e:
                    print(f"Error processing {domain}: {str(e)}")

    print(f"\nCompleted in {time.time()-start_time:.2f} seconds")
    print("Expired domains saved to ExpiredDomains.txt")

if __name__ == "__main__":
    main()