import fitz
import json
import re

PDF_FILE = "Inventory.pdf"
OUTPUT_FILE = "products.json"

doc = fitz.open(PDF_FILE)

products = []

# Regex
item_regex = re.compile(r'^\d+$')
barcode_regex = re.compile(r'^\d{12,14}$')
price_regex = re.compile(r'^\d+\.\d+$')

for page in doc:

    lines = [l.strip() for l in page.get_text().splitlines() if l.strip()]

    i = 0

    while i < len(lines):

        # Look for item number
        if item_regex.fullmatch(lines[i]):

            item_no = lines[i]
            i += 1

            block = []

            # Collect everything until next item number
            while i < len(lines) and not item_regex.fullmatch(lines[i]):
                block.append(lines[i])
                i += 1

            barcode = None
            barcode_index = -1

            # Find barcode
            for idx, value in enumerate(block):
                if barcode_regex.fullmatch(value):
                    barcode = value
                    barcode_index = idx
                    break

            if barcode is None:
                continue

            # Product name = everything before barcode
            name = " ".join(block[:barcode_index]).strip()

            # Remove leading item code stuck to the name
            name = re.sub(r'^\d+', '', name).strip()

            # Find all decimal numbers after barcode
            decimals = []

            for value in block[barcode_index + 1:]:

                clean = value.replace(",", "")

                if price_regex.fullmatch(clean):
                    decimals.append(float(clean))

            if len(decimals) < 2:
                continue

            selling_price = decimals[1]

            products.append({
                "item_no": item_no,
                "name": name,
                "barcode": barcode,
                "price": selling_price
            })

        else:
            i += 1

doc.close()

# Remove duplicate barcodes
unique = {}

for p in products:
    unique[p["barcode"]] = p

products = list(unique.values())

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(products, f, indent=4, ensure_ascii=False)

print(f"✅ Saved {len(products)} products.")
