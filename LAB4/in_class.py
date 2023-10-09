import socket
import re
import json

# Define your web server address and port
SERVER_ADDRESS = "localhost"
SERVER_PORT = 8080

# Define the routes to the product pages
PRODUCT_LISTING_PAGE = '/products-listing'
PRODUCT_DETAILS_REGEX = r'/product/(\d+)'

def send_request(path):
    # Create a socket connection to the web server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_ADDRESS, SERVER_PORT))

    # Send an HTTP GET request
    request = f"GET {path} HTTPS/1.1\r\nHost: {SERVER_ADDRESS}\r\n\r\n"
    client_socket.send(request.encode())

    # Receive and parse the HTTP response
    response = b""
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        response += data

    # Close the socket connection
    client_socket.close()

    return response.decode()

def parse_product_details(page_content):
    # Use regular expressions to extract product details from the product page
    product_details = {}
    name_match = re.search(r'<h1>(.*?)</h1>', page_content)
    if name_match:
        product_details["name"] = name_match.group(1)

    author_match = re.search(r'Author: (.*?)<', page_content)
    if author_match:
        product_details["author"] = author_match.group(1)

    price_match = re.search(r'Price: (\d+\.\d+)', page_content)
    if price_match:
        product_details["price"] = float(price_match.group(1))

    description_match = re.search(r'<p>(.*?)</p>', page_content)
    if description_match:
        product_details["description"] = description_match.group(1)

    return product_details

def main():
    # Send a request to the product listing page to get the list of product routes
    product_listing_page_content = send_request(PRODUCT_LISTING_PAGE)

    # Find product routes using regular expressions
    product_routes = re.findall(PRODUCT_DETAILS_REGEX, product_listing_page_content)

    # Iterate over product routes and fetch product details
    product_data = []
    for route in product_routes:
        product_page_content = send_request(f'/product/{route}')
        product_details = parse_product_details(product_page_content)
        product_data.append(product_details)

    # Print or save the product data as needed
    print(json.dumps(product_data, indent=4))

if __name__ == "__main__":
    main()
