import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
import argparse

RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
END = '\033[0m'

def check_requirements_update(library, version, verbose=False):
    base_url = f'https://pypi.org/pypi/{library}/{version}'.strip()
    response = requests.get(base_url)
    if response.status_code == 200:
        html_content = response.content

        # Parsing the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Finding the desired HTML tag using its class attribute
        tag = str(soup.find('a', class_='status-badge status-badge--bad', href='/project/requests/'))

        item1 = tag.find("(")
        item2 = tag.find(")")
    
        last_version = tag[item1+1:item2]
        return last_version
    else:
        print("Connection failed")
        return False

def check_elapse_time(library, version, verbose=False):
    rss_url = f"https://pypi.org/rss/project/{library}/releases.xml"

    response = requests.get(rss_url)
    if response.status_code == 200:
        root = ET.fromstring(response.content)

        versions_dates = []
        for item in root.findall("./channel/item"):
            version = item.find("title").text
            date = item.find("pubDate").text
            date_unix = convert_time(date)
            versions_dates.append((version, date_unix))
        return (versions_dates)
    else:
        return False

def convert_time(time_rss):
    date_obj = datetime.strptime(time_rss, "%a, %d %b %Y %H:%M:%S %Z")
    date_obj = date_obj.replace(tzinfo=timezone.utc) # Set the timezone explicitly to UTC
    unixtime = date_obj.timestamp()
    return unixtime

def time_btw(date):
    today = datetime.now()
    delta = today - datetime.fromtimestamp(date)
    jours = delta.days
    return jours

def start(file_requirements="requirements.txt", verbose=False, overwrite=False):
     #Check if the requirements file is present
    try:
        with open(file_requirements) as f:
            requirements = f.readlines()
    except FileNotFoundError:
        print(f"{RED}[-]{END} ERROR: {file_requirements} file not found")
        exit()

    if overwrite:
        requirements_save = file_requirements
    else:
        requirements_save = "requirements-updated.txt"
    save_elements = ""
    req = []

    for line in requirements:
        if "==" in line:
            req.append(line)
    
    for requirement in req:
        library, version = requirement.split('==')
        version = version.strip()
        new_version = check_requirements_update(library, version)

        if new_version == False:
            new_version = version
            if verbose:
                print(f'{RED}[-]{END} ERROR: {library} not found')
        elif new_version == "Non":
            new_version = version
            if verbose:  
                print(f'{GREEN}[+]{END} {library} is up to date')
        elif new_version != version:
            if verbose:
                print(f'{BLUE}[i]{END} New version of {library} available : {library} ==> {new_version}')
            result = check_elapse_time(library, version)
            
            nb_last = 0
            days = 0
            found = False

            for elements in result:

                if elements[0].strip() == version.strip():
                    found = True
                    days = time_btw(elements[1])
                    if verbose:
                        if days > 100:
                            print(f'    {RED}Last version of {library} was released {days} days ago and {nb_last} versions have been released since then{END}')
                        else:
                            print(f'    Last version of {library} was released {days} days ago and {nb_last} versions have been released since then')
                nb_last += 1
            if found == False:
                if verbose:
                    print(f'{RED}Last version of {library} was released more than {days} versions ago{END}') 

        else:  
            if verbose:  
                print(f'{GREEN}[+]{END} {library} is up to date')
        
        save_elements += f'{library}=={new_version}\n'

    with open(requirements_save,"w") as file:
        file.write(save_elements)

def parse_args():
    parser = argparse.ArgumentParser(
        description='Check if the libraries in the requirements.txt file are up to date')
    
    parser.add_argument('-p', '--path', dest='file', default='requirements.txt',
                        help='Path of the requirements file')
    parser.add_argument('-v', '--verbose', action='store_true', default=True,
                        help='Display additional information')
    parser.add_argument('-f', '--force', action='store_true', default=False,
                        help='Overwrite the requirements file')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    start(args.file, args.verbose, args.force)