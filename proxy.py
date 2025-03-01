import requests
from bs4 import BeautifulSoup
import re

# ASCII Logo
logo = """
  _____                     
 |  __ \                    
 | |__) | __ _____  ___   _ 
 |  ___/ '__/ _ \ \/ / | | |
 | |   | | | (_) >  <| |_| |
 |_|   |_|  \___/_/\_\\__, |
                       __/ |
                      |___/  
"""

# Function to scrape proxy IPs
def scrape_proxy_ips():
    url = "https://free-proxy-list.net/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract text and find all IP addresses
    text = soup.get_text()
    ip_pattern = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', text)
    
    return list(set(ip_pattern))  # Remove duplicates and return as a list

# Function to check if proxies are working
def check_proxies(ip_list):
    print("\nChecking Proxies... (This may take some time)\n")
    
    working_proxies = []
    for ip in ip_list:
        try:
            proxy = {"http": f"http://{ip}", "https": f"https://{ip}"}
            response = requests.get("https://httpbin.org/ip", proxies=proxy, timeout=3)
            
            if response.status_code == 200:
                print(f"✅ Working Proxy: {ip}")
                working_proxies.append(ip)
            else:
                print(f"❌ Failed: {ip}")
        
        except:
            print(f"❌ Failed: {ip}")

    return working_proxies

# Menu System
while True:
    print(logo)  # Display the logo at the start
    print("\n========== IP Scraper & Checker ==========")
    print("1. Scrape IPs")
    print("2. Check Proxies")
    print("3. Show Example IPs")
    print("4. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        print("\nScraping IPs... Please wait.")
        scraped_ips = scrape_proxy_ips()
        print(f"\n✅ Scraped {len(scraped_ips)} IPs!")
        print(scraped_ips[:10])  # Show first 10 IPs

    elif choice == "2":
        if 'scraped_ips' in locals() and scraped_ips:
            working_ips = check_proxies(scraped_ips)
            print(f"\n✅ {len(working_ips)} Working Proxies Found!")
        else:
            print("\n⚠️ No scraped IPs found. Please scrape first!")

    elif choice == "3":
        example_ips = ["192.168.1.1", "8.8.8.8", "123.45.67.89"]
        print("\nExample IPs:", example_ips)

    elif choice == "4":
        print("\nExiting... Goodbye!")
        break

    else:
        print("\n⚠️ Invalid choice! Please try again.")
