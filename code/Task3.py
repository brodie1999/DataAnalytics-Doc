import json 
from collections import defaultdict
import matplotlib
import matplotlib.pyplot as plt 
from Task2 import plot_chart

def process_views_by_useragent(json_file_path): 
    
    uA_counts = defaultdict(int)

    try: 
        with open(json_file_path, 'r') as file: 
            for line in file: 
                try: 
                    event = json.loads(line)
                    uA = event.get("visitor_useragent")
                    if uA: 
                        uA_counts[uA] += 1
                except json.JSONDecodeError: 
                    continue # Skip invalid JSON lines 
    except FileNotFoundError: 
        print(f"Error: File not found: {json_file_path}")
    except Exception as e: 
        print(f"Error: Unexpected Error - {e}")
    return dict(uA_counts)

# Find and reduce browser to browser name
def simplify_uA(uA): 

    if "Chrome" in uA: 
        return "Chrome"
    elif "Mozilla" in uA: 
        return "Mozilla"
    elif "FireFox" in uA: 
        return "FireFox"
    elif "Safari" in uA and "Chrome" not in uA: 
        return "Safari"
    elif "Edge" in uA: 
        return "Edge"
    elif "Opera" in uA or "Trident" in uA: 
        return "Opera"
    elif "MSIE" in uA or "Trident" in uA: 
        return "Internet Explorer"
    else: 
        return "Other"

def process_views_by_browser(json_file_path):
    browser_cnt = defaultdict(int)

    try: 
        with open(json_file_path, 'r') as file: 
            for line in file: 
                try: 
                    event = json.loads(line)
                    uA = event.get("visitor_useragent")
                    if uA: 
                        browser_name = simplify_uA(uA)
                        browser_cnt[browser_name] += 1
                except json.JSONDecodeError: 
                    continue # Skip invalid JSON lines
    except FileNotFoundError: 
        print(f"Error: File not found - {json_file_path}")
    except Exception as e: 
        print(f"Error: {e}")
    plot_chart(dict(browser_cnt), "Browser Count", browser_name, browser_cnt)
    return dict(browser_cnt)