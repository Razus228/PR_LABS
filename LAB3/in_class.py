import requests
from bs4 import BeautifulSoup

def extract_urls(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract all links
    links = [a['href'] for a in soup.find_all('a', href=True)]

    # Filter out boosters
    filtered_links = [link for link in links if not link.startswith('/boosters')]

    # Convert relative links to absolute links
    base_url = 'https://999.md'
    absolute_links = [base_url + link for link in filtered_links]

    # Check for pagination
    next_page = soup.find('a', {'class': 'paging-right'})
    if next_page:
        next_page_url = base_url + next_page['href']
        return absolute_links + extract_urls(next_page_url)
    else:
        return absolute_links

# Example usage:
url = 'https://999.md/ro/list/transport/cars'
result_urls = extract_urls(url)

print(result_urls)
