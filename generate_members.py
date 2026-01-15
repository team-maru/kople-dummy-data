import csv
import random
import uuid
from datetime import datetime, timedelta, date
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

MEMBER_COUNT = 50

# =========================
# 이름 풀 (국적별)
# =========================
NAMES_BY_NATION = {
    "KR": ["minji", "jihoon", "seongmin", "hyunwoo", "jiyoung", "soyoung", "taeyang", "haneul"],
    "US": ["james", "emily", "alex", "lucas", "olivia", "daniel", "chris"],
    "JP": ["haruto", "yuki", "sakura", "ren", "misaki", "takumi"],
    "CN": ["wei", "liang", "jing", "xiaoyu", "chen", "lin"],
    "VN": ["minh", "anh", "quang", "thao", "linh"],
    "FR": ["luc", "emma", "leo", "chloe", "antoine"],
    "DE": ["max", "lena", "felix", "anna", "jonas"]
}

ISO_CODES = list(NAMES_BY_NATION.keys())

# =========================
# 학교 코드
# =========================
UNIVERSITIES = [
    "SEOUL_NU", "YONSEI_U", "KOREA_U", "HANYANG_U", "EWHA_WOMANS_U",
    "SUNGKYUNKWAN_U", "KONKUK_U", "HONGIK_U", "POSTECH", "KAIST",
    "PUSAN_NU", "GYEONGSANG_NU", "CHONNAM_NU", "JEJU_NU",
    "UNIV_OF_SEOUL", "INHA_U", "AJOU_U", "SOONGSIL_U"
]

# =========================
# 관심사 코드
# =========================
INTEREST_ITEMS = [
    "EXPLORING_NEW_CITY", "CAMPUS_EVENTS", "HIKING", "RUNNING",
    "YOGA", "FOOTBALL", "GYM_FITNESS", "MOVIES", "MUSIC", "GAMING",
    "PHOTOGRAPHY", "COOKING", "CAFES", "KPOP", "KDRAMA",
    "KOREAN_LANGUAGE", "LANGUAGE_EXCHANGE", "LOCAL_TRAVEL"
]

# =========================
# ENUM 값
# =========================
GENDERS = ["MALE", "FEMALE"]
STATUSES = [
    "EXCHANGE_STUDENT",
    "INTERNATIONAL_STUDENT",
    "LANGUAGE_SCHOOL_STUDENT",
    "KOREAN_STUDENT"
]

# =========================
# 헬퍼 함수
# =========================
used_nicknames = set()

def generate_nickname(nation):
    base = random.choice(NAMES_BY_NATION[nation])
    suffix = random.choice(["", str(random.randint(90, 99))])
    nickname = f"{base}{suffix}"
    if nickname in used_nicknames or len(nickname) < 3 or len(nickname) > 15:
        return generate_nickname(nation)
    used_nicknames.add(nickname)
    return nickname

def random_birthdate():
    start = date(1990, 1, 1)
    end = date(2005, 12, 31)
    return start + timedelta(days=random.randint(0, (end - start).days))

# =========================
# CSV 생성
# =========================

members = []

with open("member.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "clerk_id", "email", "email_verified",
        "is_registered", "is_suspended",
        "allow_message_notif", "allow_event_notif",
        "allow_gathering_notif", "allow_comment_notif",
        "allow_bookmark_notif", "role", "last_login_at"
    ])

    for i in range(1, MEMBER_COUNT + 1):
        clerk_id = f"user_{uuid.uuid4().hex[:20]}"
        email = f"user{i}@example.com"
        last_login = fake.date_time_between(start_date="-10d", end_date="now")

        writer.writerow([
            clerk_id,
            email,
            True,
            True,
            False,
            True,
            True,
            True,
            True,
            True,
            "USER",
            last_login.strftime("%Y-%m-%d %H:%M:%S")
        ])

        members.append({
            "member_index": i,
            "clerk_id": clerk_id
        })

# -------------------------

with open("profile.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "member_index", "nickname", "birth_date",
        "gender", "nation_code", "university_code",
        "status", "nickname_last_changed_at"
    ])

    for m in members:
        nation = random.choice(ISO_CODES)
        nickname = generate_nickname(nation)

        writer.writerow([
            m["member_index"],
            nickname,
            random_birthdate().isoformat(),
            random.choice(GENDERS),
            nation,
            random.choice(UNIVERSITIES),
            random.choice(STATUSES),
            fake.date_time_between(start_date="-30d", end_date="-15d").strftime("%Y-%m-%d %H:%M:%S")
        ])

# -------------------------

with open("buddy.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "member_index", "bio", "is_active"
    ])

    for m in members:
        writer.writerow([
            m["member_index"],
            fake.sentence(nb_words=12),
            True
        ])

# -------------------------

with open("member_interest.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "member_index", "interest_item_code"
    ])

    for m in members:
        interests = random.sample(INTEREST_ITEMS, random.randint(1, 3))
        for interest in interests:
            writer.writerow([
                m["member_index"],
                interest
            ])

print("✅ CSV dummy data generated successfully.")
