import re

# Regex to match image URLs
image_url_pattern = re.compile(r'https?://[^\s,"]+\.(?:png|jpg|jpeg|gif|webp)')

# List to hold groups of image URLs
image_groups = []

# Read the file
with open("wc-product-export-8-5-2025-1746685215835.csv", "r", encoding="utf-8") as file:
    for line in file:
        # Find all image URLs in the line
        urls = image_url_pattern.findall(line)
        if urls:
            image_groups.append(urls)

# Example: print the groups
for i, group in enumerate(image_groups, 1):
    print("[")
    for url in group:
        print(f'"{url}",')
    print("],")
