import csv
import random
import uuid
from datetime import datetime, timedelta, date, timezone
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

# =====================
# CONFIG
# =====================
START_ID = 31
MEMBER_COUNT = 50

# ISO2 nation codes
NATION_CODES = ["KR", "US", "JP", "FR", "DE", "VN"]

# university.id values already in DB (예시)
UNIVERSITY_IDS = [
    1, 9, 12, 44, 54, 66, 73, 85, 91, 112
]

GENDERS = ["MALE", "FEMALE"]
STATUSES = [
    "EXCHANGE_STUDENT",
    "INTERNATIONAL_STUDENT",
    "LANGUAGE_SCHOOL_STUDENT",
    "FOREIGN_RESIDENT",
    "KOREAN_STUDENT"
]

used_nicknames = set()

# =====================
# HELPERS
# =====================
def utc_now():
    return datetime.now(timezone.utc)

def random_recent_time(days=30):
    return utc_now() - timedelta(
        days=random.randint(0, days),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )

def random_birthdate():
    start = date(1995, 1, 1)
    end = date(2004, 12, 31)
    return start + timedelta(days=random.randint(0, (end - start).days))

def generate_nickname():
    while True:
        base = fake.user_name().replace(".", "").replace("_", "")
        suffix = random.choice(["", str(random.randint(10, 99))])
        nickname = (base + suffix)[:15]
        if 3 <= len(nickname) <= 15 and nickname not in used_nicknames:
            used_nicknames.add(nickname)
            return nickname

# =====================
# CSV: MEMBER
# =====================
with open("member.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "id", "clerk_id", "email", "email_verified",
        "is_registered", "is_suspended", "suspended_at",
        "allow_message_notif", "allow_event_notif",
        "allow_gathering_notif", "allow_comment_notif",
        "allow_bookmark_notif",
        "last_login_at", "role",
        "created_at", "updated_at", "deleted_at"
    ])

    for i in range(MEMBER_COUNT):
        member_id = START_ID + i
        created_at = random_recent_time(40)
        updated_at = random_recent_time(5)
        last_login = random_recent_time(7)

        writer.writerow([
            member_id,
            f"clerk_{uuid.uuid4().hex[:20]}",
            f"user{member_id}@example.com",
            True,
            True,
            False,
            "",
            True, True, True, True, True,
            last_login.isoformat().replace("+00:00", "Z"),
            "USER",
            created_at.isoformat().replace("+00:00", "Z"),
            updated_at.isoformat().replace("+00:00", "Z"),
            ""
        ])

# =====================
# CSV: PROFILE
# =====================
with open("profile.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "id", "member_id", "nickname",
        "nickname_last_changed_at",
        "birth_date", "gender",
        "nation_code", "university_id",
        "status",
        "created_at", "updated_at", "deleted_at"
    ])

    for i in range(MEMBER_COUNT):
        pid = START_ID + i
        created_at = random_recent_time(40)
        updated_at = random_recent_time(5)

        writer.writerow([
            pid,
            pid,
            generate_nickname(),
            (created_at + timedelta(days=3)).isoformat().replace("+00:00", "Z"),
            random_birthdate().isoformat(),
            random.choice(GENDERS),
            random.choice(NATION_CODES),
            random.choice(UNIVERSITY_IDS),
            random.choice(STATUSES),
            created_at.isoformat().replace("+00:00", "Z"),
            updated_at.isoformat().replace("+00:00", "Z"),
            ""
        ])

# =====================
# CSV: BUDDY
# =====================
with open("buddy.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "id", "member_id", "bio",
        "is_active", "created_at", "updated_at"
    ])

    for i in range(MEMBER_COUNT):
        bid = START_ID + i
        created_at = random_recent_time(40)
        updated_at = random_recent_time(5)

        writer.writerow([
            bid,
            bid,
            fake.sentence(nb_words=12),
            True,
            created_at.isoformat().replace("+00:00", "Z"),
            updated_at.isoformat().replace("+00:00", "Z")
        ])

print("✅ member / profile / buddy CSV generated successfully")
