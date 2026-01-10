import sys
import json
import os
import time

try:
    import requests
    from lxml import html
    from markdownify import markdownify as md
except ImportError:
    print("The 'requests', 'lxml', and 'markdownify' libraries are required.")
    print(f"Please install them by running:")
    print(f"{sys.executable} -m pip install requests lxml markdownify")
    sys.exit(1)

def fetch_and_convert(url, content_xpath):
    """
    Fetches a webpage, extracts content from a specific element, and converts it to Markdown.
    """
    try:
        print(f"Fetching: {url}")
        response = requests.get(url)
        response.raise_for_status()

        tree = html.fromstring(response.content)
        content_elements = tree.xpath(content_xpath)

        if not content_elements:
            print(f"Warning: Content element not found for {url}")
            return None

        # Extract the inner HTML of the found element
        content_html = html.tostring(content_elements[0], pretty_print=True).decode('utf-8')
        
        # Convert HTML to Markdown
        markdown_content = md(content_html, heading_style="ATX")
        
        return markdown_content

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred for {url}: {e}")
        return None

def main():
    """
    Main function to read links, fetch content, and create MDX files.
    """
    links_file = 'all_links.json'
    output_dir = '/Users/jacobatnip/Desktop/files/software_projects/earls-blog/src/content/posts/'
    base_url = 'https://sites.google.com'
    content_xpath = '//*[@id="yDmH0d"]/div[1]/div/div[2]/div[3]/div/div[1]'

    if not os.path.exists(links_file):
        print(f"Error: '{links_file}' not found. Please run the link fetching script first.")
        return

    if not os.path.exists(output_dir):
        print(f"Error: Output directory '{output_dir}' does not exist.")
        return

    with open(links_file, 'r') as f:
        relative_links = json.load(f)

    print(f"Found {len(relative_links)} links to process.")

    for link in relative_links:
        full_url = base_url + link
        
        # Generate a filename from the link
        # e.g., /site/earlatnipsplace/earl-atnips-place/2011-buffalo-river -> 2011-buffalo-river.mdx
        filename = link.split('/')[-1] + '.mdx'
        output_path = os.path.join(output_dir, filename)

        # Check if the file already exists to avoid re-processing
        # if os.path.exists(output_path):
        #     print(f"Skipping {filename}, file already exists.")
        #     continue

        markdown_content = fetch_and_convert(full_url, content_xpath)

        if markdown_content:
            current_date = time.strftime('%Y-%m-%d')
            # Basic frontmatter for Astro
            frontmatter = f"""---
title: "{filename.replace('.mdx', '').replace('-', ' ').title()}"
description: "A post about {filename.replace('.mdx', '').replace('-', ' ')}"
postDate: {current_date}
layout: '@/layouts/ArticleLayout.astro'
---
"""
            full_content = frontmatter + "\n" + markdown_content

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(full_content)
            print(f"Successfully created/updated: {output_path}")
        else:
            print(f"Failed to create MDX for {full_url}")
        
        # Add a small delay to be polite to the server
        time.sleep(1)

    print("\nProcessing complete.")

if __name__ == "__main__":
    main()
