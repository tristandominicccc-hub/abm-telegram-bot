import fitz
import re
import json

PDF_FILE = "Inventory.pdf"
OUTPUT_FILE = "products.json"

doc = fitz.open(PDF_FILE)

products = []

for page in doc:
    text = page.get_text()

    for line in text.split("\n"):

        line = line.strip()

        if not line:
            continue

        # Find a barcode (12-14 digits)
        barcode_match = re.search(r"\b\d{12,14}\b", line)

        if not barcode_match:
            continue

        barcode = barcode_match.group()

        before = line[:barcode_match.start()].strip()
        after = line[barcode_match.end():].strip()

        # Remove item number
        before = re.sub(r"^\d+\s+", "", before)

        name = before.strip()

        # Selling price comes after cost price
        prices = re.findall(r"\d+\.\d+", after)

        if len(prices) < 2:
            continue

        selling_price = float(prices[1])

        products.append({
            "name": name,
            "barcode": barcode,
            "price": selling_price
        })

doc.close()

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(products, f, indent=4, ensure_ascii=False)

print(f"Saved {len(products)} products.")