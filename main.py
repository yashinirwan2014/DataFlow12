import csv
from pathlib import Path
from collections import Counter

SOURCE = Path("data/raw_students.csv")
OUTPUT = Path("output")
REQUIRED = ["name", "class", "score"]

def clean_text(value):
    return (value or "").strip()

def process_file(source=SOURCE, output=OUTPUT):
    output.mkdir(parents=True, exist_ok=True)
    counts = Counter()
    cleaned, seen = [], set()
    with open(source, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        headers = [h.strip().lower() for h in (reader.fieldnames or [])]
        missing = [field for field in REQUIRED if field not in headers]
        if missing:
            raise ValueError("Missing columns: " + ", ".join(missing))
        for number, raw in enumerate(reader, 2):
            row = {str(k).strip().lower(): clean_text(v) for k, v in raw.items() if k}
            if any(not row.get(field) for field in REQUIRED):
                counts["missing_required"] += 1
                continue
            try:
                score = float(row["score"])
                if not 0 <= score <= 100:
                    raise ValueError()
            except ValueError:
                counts["invalid_score"] += 1
                continue
            row["score"] = str(round(score, 2))
            key = tuple(row.get(h, "") for h in headers)
            if key in seen:
                counts["duplicates"] += 1
                continue
            seen.add(key)
            cleaned.append(row)
            counts["accepted"] += 1
    with open(output / "cleaned.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(cleaned)
    with open(output / "quality_report.txt", "w", encoding="utf-8") as file:
        file.write("DATA QUALITY REPORT\n")
        for key in sorted(counts):
            file.write(f"{key}: {counts[key]}\n")
    return counts

if __name__ == "__main__":
    try:
        print(process_file())
        print("Created output/cleaned.csv and output/quality_report.txt")
    except (OSError, ValueError) as error:
        print("Processing failed:", error)