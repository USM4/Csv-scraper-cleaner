import re

# Path to your file
file_path = "final-result.csv"

# Regex to match image URLs
image_url_pattern = re.compile(r'https?://[^\s,"]+\.(png|jpg|jpeg|gif|webp)')

# New base URL to replace with
new_base_url = "https://zumcy.com/wp-content/uploads/2025/05"

# Store updated lines
updated_lines = []

product_counter = 1

with open(file_path, "r", encoding="utf-8") as f:
    for line in f:
        matches = list(image_url_pattern.finditer(line))
        if matches:
            new_urls = []
            for i, match in enumerate(matches, start=1):
                ext = match.group(1)
                new_url = f"{new_base_url}/product-{product_counter}-image-{i}.{ext}"
                new_urls.append(new_url)

            # Replace all matched image URLs with new formatted ones
            old_urls = [m.group(0) for m in matches]
            for old, new in zip(old_urls, new_urls):
                line = line.replace(old, new)

            product_counter += 1

        updated_lines.append(line)

# Write changes back to the same file (overwrite)
with open(file_path, "w", encoding="utf-8") as f:
    f.writelines(updated_lines)

print("✅ File updated and overwritten successfully.")
