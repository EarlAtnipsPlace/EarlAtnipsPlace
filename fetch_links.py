import sys
import json

try:
    import requests
    from lxml import html
except ImportError:
    print("The 'requests' and 'lxml' libraries are required. Please install them by running:")
    print(f"{sys.executable} -m pip install requests lxml")
    sys.exit(1)

def fetch_links_from_subtree(url, xpath):
    """
    Fetches all links from a specific element's subtree on a webpage.

    Args:
        url: The URL of the webpage.
        xpath: The XPath of the parent element.

    Returns:
        A list of links found within the element's subtree.
    """
    try:
        print(f"Fetching content from: {url}")
        response = requests.get(url)
        response.raise_for_status()
        print("Successfully fetched content.")

        tree = html.fromstring(response.content)

        print(f"Searching for element with XPath: {xpath}")
        container_elements = tree.xpath(xpath)

        if not container_elements:
            print(f"Error: Element with XPath '{xpath}' not found.")
            return []

        element = container_elements[0]
        print("Element found. Extracting all descendant links...")

        # './/a/@href' finds all 'a' tags that are descendants of the current element
        links = element.xpath('.//a/@href')
        return links

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

if __name__ == "__main__":
    target_url = "https://sites.google.com/site/earlatnipsplace/earl-atnips-place?authuser=0"
    target_xpath = '//*[@id="yuynLe"]/ul/li[1]/div[2]'
    output_filename = "all_links.json"

    extracted_links = fetch_links_from_subtree(target_url, target_xpath)

    if extracted_links:
        print(f"\nFound {len(extracted_links)} links. Saving to {output_filename}...")
        
        # Save the links to a JSON file
        with open(output_filename, 'w') as f:
            json.dump(extracted_links, f, indent=4)
            
        print(f"Successfully saved links to {output_filename}.")
    else:
        print("\nNo links were found in the specified element's subtree.")
