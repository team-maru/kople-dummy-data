import csv
import random

START_MEMBER_ID = 1
MEMBER_COUNT = 50

INTEREST_ITEM_IDS = list(range(1, 42))

with open("member_interest.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["member_id", "interest_item_id"])

    for i in range(MEMBER_COUNT):
        member_id = START_MEMBER_ID + i

        interest_count = random.randint(1, 3)
        interest_ids = random.sample(INTEREST_ITEM_IDS, interest_count)

        for interest_item_id in interest_ids:
            writer.writerow([member_id, interest_item_id])
            
print("✅ member_interest.csv generated (1~3 interests per member)")
