import csv
import random
from datetime import datetime, timedelta, timezone
from faker import Faker

fake = Faker()
random.seed(42)
Faker.seed(42)

# =========================
# CONFIG
# =========================
START_MEMBER_ID = 1
MEMBER_COUNT = 50

POST_COUNT = 80
COMMENT_COUNT = 160

CATEGORIES = ["CAMPUS", "DAILY_TIPS", "EATS", "ACTIVITY", "QNA"]

COMMENTS = [
    "I totally agree with this!",
    "저도 비슷하게 느꼈어요.",
    "Thanks for sharing, this helps a lot.",
    "이거 진짜 공감돼요 ㅋㅋ",
    "I had the same question before.",
    "저도 궁금했는데 감사합니다!",
    "Sounds interesting, I want to try this.",
    "다음에 같이 가요!"
]

# =========================
# TIME HELPER
# =========================
def random_time(days=20):
    return (
        datetime.now(timezone.utc)
        - timedelta(
            days=random.randint(0, days),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
        )
    ).isoformat().replace("+00:00", "Z")

# =========================
# POST GENERATORS
# =========================
def generate_post_title():
    patterns = [
        "Anyone tried {} near campus?",
        "{} 해보신 분 계신가요?",
        "After {} weeks in Korea, here’s what I noticed",
        "Looking for people to {} together",
        "혼자 {} 다녀와봤는데 후기 남겨요",
        "{} 관련해서 질문 있어요!",
    ]

    keyword = random.choice([
        "good cafes",
        "local food spots",
        "hiking",
        "language exchange",
        "weekend trips",
        "gym",
        "part-time jobs",
        "events",
    ])

    title = random.choice(patterns).format(keyword)
    return title[:80]

def generate_post_content():
    paragraphs = []

    paragraphs.append(
        fake.paragraph(nb_sentences=random.randint(3, 5))
    )

    if random.random() < 0.7:
        paragraphs.append(
            fake.paragraph(nb_sentences=random.randint(4, 6))
        )

    paragraphs.append(
        random.choice([
            "Has anyone had a similar experience?",
            "Would love to hear your thoughts!",
            "혹시 추천이나 조언 있으면 알려주세요 🙏",
            "다른 분들은 어떻게 생각하시나요?",
        ])
    )

    content = "\n\n".join(paragraphs)
    return content[:1000]

# =========================
# FreePost CSV
# =========================
with open("free_post.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "id",
        "member_id",
        "title",
        "content",
        "category",
        "like_count",
        "comment_count",
        "created_at",
        "updated_at",
        "deleted_at",
    ])

    for post_id in range(1, POST_COUNT + 1):
        writer.writerow([
            post_id,
            random.randint(START_MEMBER_ID, START_MEMBER_ID + MEMBER_COUNT - 1),
            generate_post_title(),
            generate_post_content(),
            random.choice(CATEGORIES),
            0,
            0,
            random_time(),
            "",
            "",
        ])

# =========================
# Comment CSV
# =========================
with open("comment.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "id",
        "member_id",
        "post_id",
        "content",
        "parent_id",
        "like_count",
        "created_at",
        "updated_at",
        "deleted_at",
    ])

    for cid in range(1, COMMENT_COUNT + 1):
        writer.writerow([
            cid,
            random.randint(START_MEMBER_ID, START_MEMBER_ID + MEMBER_COUNT - 1),
            random.randint(1, POST_COUNT),
            random.choice(COMMENTS)[:500],
            "",
            0,
            random_time(),
            "",
            "",
        ])

# =========================
# FreeLike (Post Like)
# =========================
with open("free_like.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["member_id", "post_id"])

    for post_id in range(1, POST_COUNT + 1):
        likers = random.sample(
            range(START_MEMBER_ID, START_MEMBER_ID + MEMBER_COUNT),
            random.randint(3, 7),
        )
        for member_id in likers:
            writer.writerow([member_id, post_id])

# =========================
# CommentLike CSV
# =========================
COMMENT_LIKE_MAX = 5

with open("comment_like.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["member_id", "comment_id"])

    for comment_id in range(1, COMMENT_COUNT + 1):
        like_count = random.randint(0, COMMENT_LIKE_MAX)
        likers = random.sample(
            range(START_MEMBER_ID, START_MEMBER_ID + MEMBER_COUNT),
            like_count,
        )

        for member_id in likers:
            writer.writerow([member_id, comment_id])

print("✅ free_post / comment / free_like / comment_like CSV generated")
