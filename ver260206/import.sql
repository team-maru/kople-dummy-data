/* =========================================================
   KOPLE Dummy Data Import Script
   - FK-safe
   - Instant (UTC)
   - Aggregation included
========================================================= */

SET SESSION sql_mode = '';
SET FOREIGN_KEY_CHECKS = 0;
SET UNIQUE_CHECKS = 0;
SET autocommit = 0;

/* =========================
   MEMBER
========================= */
LOAD DATA LOCAL INFILE 'member.csv'
INTO TABLE member
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
IGNORE 1 ROWS
(
  id,
  clerk_id,
  email,
  email_verified,
  is_registered,
  is_suspended,
  @suspended_at,
  allow_message_notif,
  allow_event_notif,
  allow_gathering_notif,
  allow_comment_notif,
  allow_bookmark_notif,
  last_login_at,
  role,
  created_at,
  updated_at,
  @deleted_at
)
SET
  suspended_at = NULLIF(@suspended_at, ''),
  deleted_at   = NULLIF(@deleted_at, '');

/* =========================
   PROFILE
========================= */
LOAD DATA LOCAL INFILE 'profile.csv'
INTO TABLE profile
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
IGNORE 1 ROWS
(
  id,
  member_id,
  nickname,
  nickname_last_changed_at,
  birth_date,
  gender,
  nation_code,
  university_id,
  status,
  created_at,
  updated_at,
  @deleted_at
)
SET deleted_at = NULLIF(@deleted_at, '');

/* =========================
   BUDDY
========================= */
LOAD DATA LOCAL INFILE 'buddy.csv'
INTO TABLE buddy
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
IGNORE 1 ROWS
(
  id,
  member_id,
  bio,
  is_active,
  created_at,
  updated_at
);

/* =========================
   MEMBER_INTEREST
========================= */
LOAD DATA LOCAL INFILE 'member_interest.csv'
INTO TABLE member_interest
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
IGNORE 1 ROWS
(
  member_id,
  interest_item_code
);

/* interest_item.code → id 매핑 */
UPDATE member_interest mi
JOIN interest_item ii
  ON ii.code = mi.interest_item_code
SET mi.interest_item_id = ii.id;

/* 임시 컬럼 제거 */
ALTER TABLE member_interest DROP COLUMN interest_item_code;

/* =========================
   FREE_POST
========================= */
LOAD DATA LOCAL INFILE 'free_post.csv'
INTO TABLE free_post
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
IGNORE 1 ROWS
(
  id,
  member_id,
  title,
  content,
  category,
  like_count,
  comment_count,
  created_at,
  updated_at,
  @deleted_at
)
SET deleted_at = NULLIF(@deleted_at, '');

/* =========================
   COMMENT
========================= */
LOAD DATA LOCAL INFILE 'comment.csv'
INTO TABLE comment
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
IGNORE 1 ROWS
(
  id,
  member_id,
  post_id,
  content,
  @parent_id,
  like_count,
  created_at,
  updated_at,
  @deleted_at
)
SET
  parent_id = NULLIF(@parent_id, ''),
  deleted_at = NULLIF(@deleted_at, '');

/* =========================
   FREE_LIKE
========================= */
LOAD DATA LOCAL INFILE 'free_like.csv'
INTO TABLE free_like
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
IGNORE 1 ROWS
(
  member_id,
  post_id
);

/* =========================
   COMMENT_LIKE (선택)
   - comment_like.csv 생성 시만 사용
========================= */
/*
LOAD DATA LOCAL INFILE 'comment_like.csv'
INTO TABLE comment_like
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
IGNORE 1 ROWS
(
  member_id,
  comment_id
);
*/

/* =========================================================
   AGGREGATION
========================================================= */

/* FREE_POST.like_count */
UPDATE free_post p
LEFT JOIN (
  SELECT post_id, COUNT(*) cnt
  FROM free_like
  GROUP BY post_id
) l ON p.id = l.post_id
SET p.like_count = IFNULL(l.cnt, 0);

/* FREE_POST.comment_count */
UPDATE free_post p
LEFT JOIN (
  SELECT post_id, COUNT(*) cnt
  FROM comment
  WHERE deleted_at IS NULL
  GROUP BY post_id
) c ON p.id = c.post_id
SET p.comment_count = IFNULL(c.cnt, 0);

/* COMMENT.like_count */
UPDATE comment c
LEFT JOIN (
  SELECT comment_id, COUNT(*) cnt
  FROM comment_like
  GROUP BY comment_id
) l ON c.id = l.comment_id
SET c.like_count = IFNULL(l.cnt, 0);

/* =========================
   COMMIT & RESTORE
========================= */
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
SET UNIQUE_CHECKS = 1;
SET autocommit = 1;
