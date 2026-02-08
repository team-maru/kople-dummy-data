import csv
import random

START_MEMBER_ID = 31
MEMBER_COUNT = 50

# interest_item.code (이미 DB에 존재)
INTEREST_CODES = [
    "EXPLORING_NEW_CITY", "CAMPUS_EVENTS", "HIKING", "RUNNING",
    "YOGA", "GYM_FITNESS", "FOOTBALL", "MOVIES", "MUSIC",
    "GAMING", "PHOTOGRAPHY", "COOKING", "CAFES",
    "KPOP", "KDRAMA", "KOREAN_LANGUAGE",
    "LANGUAGE_EXCHANGE", "LOCAL_TRAVEL"
]

with open("member_interest.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["member_id", "interest_item_code"])

    for i in range(MEMBER_COUNT):
        member_id = START_MEMBER_ID + i
        interests = random.sample(INTEREST_CODES, random.randint(2, 4))

        for code in interests:
            writer.writerow([member_id, code])

print("✅ member_interest.csv generated")
