import csv
import random

POST_COUNT = 50
TOTAL_COMMENT_TARGET = 80
MEMBER_COUNT = 50

CATEGORIES = ["CAMPUS", "DAILY_TIPS", "EATS", "ACTIVITY", "QNA"]

# -------------------------------
# Post titles (English, realistic)
# -------------------------------
POST_TITLES = {
    "CAMPUS": [
        "Any good cafes near campus?",
        "Dorm life tips for exchange students",
        "Best places to study on campus?"
    ],
    "DAILY_TIPS": [
        "Things I wish I knew before coming to Korea",
        "Small daily tips for living in Korea",
        "What surprised me the most here"
    ],
    "EATS": [
        "Best food spots near school?",
        "Good places for eating alone?",
        "Late night food recommendations"
    ],
    "ACTIVITY": [
        "Anyone down for hiking this weekend?",
        "Looking for people to run together",
        "Any yoga studios you recommend?"
    ],
    "QNA": [
        "Question about exchange student classes",
        "How does part-time work work here?",
        "Foreigner registration card questions"
    ]
}

COMMENTS = [
    "I had a similar experience.",
    "Totally agree with this.",
    "Thanks for sharing!",
    "Do you mind sharing the location?",
    "This was helpful, appreciate it.",
    "I was wondering the same thing.",
    "Good to know, thanks!"
]

def generate_post_content(title: str) -> str:
    # CSV-safe: single line only
    return (
        f"{title} I wanted to share my experience and hear what others think. "
        "If you have any recommendations or similar experiences, feel free to comment. Thanks!"
    )

# =====================================================
# FreePost CSV
# =====================================================
with open("free_post.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["member_index", "title", "content", "category"])

    for _ in range(POST_COUNT):
        category = random.choice(CATEGORIES)
        title = random.choice(POST_TITLES[category])
        content = generate_post_content(title)

        writer.writerow([
            random.randint(1, MEMBER_COUNT),
            title,
            content,
            category
        ])

# -------------------------------
# Comment TSV (SAFE VERSION)
# -------------------------------
with open("comment.tsv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["member_index", "post_index", "content"])

    comments_created = 0
    while comments_created < TOTAL_COMMENT_TARGET:
        writer.writerow([
            random.randint(1, MEMBER_COUNT),
            random.randint(1, POST_COUNT),
            random.choice(COMMENTS)
        ])
        comments_created += 1

# =====================================================
# FreeLike CSV
# =====================================================
with open("free_like.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["member_index", "post_index"])

    for post_index in range(1, POST_COUNT + 1):
        liked_members = random.sample(
            range(1, MEMBER_COUNT + 1),
            random.randint(3, 7)
        )
        for m in liked_members:
            writer.writerow([m, post_index])

# =====================================================
# CommentLike CSV
# (likes on random comments, index-based)
# =====================================================
with open("comment_like.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["member_index", "comment_index"])

    # comment_index는 DB에서 auto_increment이므로
    # "대략적인 분포 테스트용"으로만 사용
    for comment_index in random.sample(
        range(1, TOTAL_COMMENT_TARGET + 1),
        min(40, TOTAL_COMMENT_TARGET)
    ):
        writer.writerow([
            random.randint(1, MEMBER_COUNT),
            comment_index
        ])

# =====================================================
# Image CSV (S3 key 기반, FREE post)
# =====================================================
with open("image.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["type", "type_id", "url", "order_num"])

    image_posts = random.sample(range(1, POST_COUNT + 1), 20)
    for post_index in image_posts:
        writer.writerow([
            "FREE",
            post_index,
            f"free/post_{post_index}.jpg",
            1
        ])

print("✅ SAFE dummy data generated (posts, comments, likes, images)")
