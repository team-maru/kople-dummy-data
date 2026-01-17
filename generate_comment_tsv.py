import csv
import random

MEMBER_COUNT = 50
POST_COUNT = 50
COMMENT_COUNT = 83  # 네가 확인한 row 수

COMMENTS = [
    "Thanks for sharing, this is really helpful!",
    "I had the same question, appreciate the info.",
    "This totally makes sense, thanks!",
    "Does anyone know if this is still valid?",
    "I tried this last week and it worked well.",
    "Great tip, especially for newcomers.",
    "This saved me a lot of time, thanks!",
    "I was wondering about this too.",
    "Really useful post, appreciate it.",
    "Can you share more details about this?"
]

with open("comment.tsv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["member_index", "post_index", "content"])

    for _ in range(COMMENT_COUNT):
        writer.writerow([
            random.randint(1, MEMBER_COUNT),
            random.randint(1, POST_COUNT),
            random.choice(COMMENTS)
        ])

print("✅ comment.tsv generated")
