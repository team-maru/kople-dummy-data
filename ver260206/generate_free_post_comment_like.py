import csv
import random
from datetime import datetime, timedelta, timezone

START_MEMBER_ID = 31
MEMBER_COUNT = 50

POST_COUNT = 80
COMMENT_COUNT = 160

CATEGORIES = ["CAMPUS", "DAILY_TIPS", "EATS", "ACTIVITY", "QNA"]

POST_TITLES = [
    "Any good places near campus?",
    "혼자 가기 좋은 카페 추천?",
    "Things I learned after one month in Korea",
    "한국 생활하면서 제일 놀랐던 점",
    "Looking for people to join this weekend",
    "주말에 뭐 하면 좋을까요?",
    "Best budget food spots around here",
    "수업 들으면서 알게 된 꿀팁"
]

POST_BODIES = [
    "I have been staying in Korea for a while and wanted to share my experience. "
    "It has been really interesting to see how daily life works here.\n\n"
    "요즘 한국 생활에 조금 익숙해졌는데, 생각보다 재밌는 점이 많아요. "
    "다른 분들은 어떤 경험을 하고 계신지 궁금합니다.",

    "This is something I noticed recently and thought it might be helpful. "
    "Please feel free to share your thoughts.\n\n"
    "혹시 비슷한 경험 있으신 분들 계시면 댓글로 알려주세요!",

    "I am still getting used to everything, but overall it has been a great experience.\n\n"
    "아직 낯선 부분도 많지만, 천천히 적응해가고 있는 중이에요."
]

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

def random_time(days=20):
    return (datetime.now(timezone.utc) - timedelta(
        days=random.randint(0, days),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )).isoformat().replace("+00:00", "Z")

# =========================
# FreePost
# =========================
with open("free_post.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "id", "member_id", "title", "content",
        "category", "like_count", "comment_count",
        "created_at", "updated_at", "deleted_at"
    ])

    for post_id in range(1, POST_COUNT + 1):
        writer.writerow([
            post_id,
            random.randint(START_MEMBER_ID, START_MEMBER_ID + MEMBER_COUNT - 1),
            random.choice(POST_TITLES),
            random.choice(POST_BODIES),
            random.choice(CATEGORIES),
            0,
            0,
            random_time(),
            random_time(),
            ""
        ])

# =========================
# Comment
# =========================
with open("comment.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "id", "member_id", "post_id",
        "content", "parent_id",
        "like_count", "created_at",
        "updated_at", "deleted_at"
    ])

    for cid in range(1, COMMENT_COUNT + 1):
        writer.writerow([
            cid,
            random.randint(START_MEMBER_ID, START_MEMBER_ID + MEMBER_COUNT - 1),
            random.randint(1, POST_COUNT),
            random.choice(COMMENTS),
            "",
            0,
            random_time(),
            random_time(),
            ""
        ])

# =========================
# FreeLike
# =========================
with open("free_like.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["member_id", "post_id"])

    for post_id in range(1, POST_COUNT + 1):
        likers = random.sample(
            range(START_MEMBER_ID, START_MEMBER_ID + MEMBER_COUNT),
            random.randint(3, 7)
        )
        for member_id in likers:
            writer.writerow([member_id, post_id])

print("✅ free_post / comment / free_like CSV generated")
