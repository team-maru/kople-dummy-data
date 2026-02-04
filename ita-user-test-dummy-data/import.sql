-- CSV import 안정성 설정
SET SESSION sql_mode = '';
SET FOREIGN_KEY_CHECKS = 0;
SET UNIQUE_CHECKS = 0;
SET autocommit = 0;

-- member
LOAD DATA LOCAL INFILE 'member.csv'
INTO TABLE member
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
IGNORE 1 ROWS
(
  clerk_id,
  email,
  email_verified,
  is_registered,
  is_suspended,
  allow_message_notif,
  allow_event_notif,
  allow_gathering_notif,
  allow_comment_notif,
  allow_bookmark_notif,
  role,
  last_login_at
);

-- profile
LOAD DATA LOCAL INFILE 'profile.csv'
INTO TABLE profile
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
IGNORE 1 ROWS
(
  @member_index,
  nickname,
  birth_date,
  gender,
  nation_code,
  @university_code,
  status,
  nickname_last_changed_at
)
SET member_id = @member_index;

-- university 매핑
UPDATE profile p
JOIN university u
  ON u.code = p.university_code
SET p.university_id = u.id;

ALTER TABLE profile DROP COLUMN university_code;


-- buddy
LOAD DATA LOCAL INFILE 'buddy.csv'
INTO TABLE buddy
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
IGNORE 1 ROWS
(
  @member_index,
  bio,
  is_active
)
SET member_id = @member_index;

-- MEMBER_INTEREST
LOAD DATA LOCAL INFILE 'member_interest.csv'
INTO TABLE member_interest
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
IGNORE 1 ROWS
(
  @member_index,
  @interest_code
)
SET member_id = @member_index;

UPDATE member_interest mi
JOIN interest_item ii
  ON ii.code = mi.interest_code
SET mi.interest_item_id = ii.id;

ALTER TABLE member_interest DROP COLUMN interest_code;

-- FREE_POST
LOAD DATA LOCAL INFILE 'free_post.csv'
INTO TABLE free_post
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
IGNORE 1 ROWS
(
  @member_index,
  title,
  content,
  category
)
SET member_id = @member_index;

-- COMMENT (SAFE: 댓글만)
LOAD DATA LOCAL INFILE 'comment.csv'
INTO TABLE comment
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
IGNORE 1 ROWS
(
  @member_index,
  @post_index,
  content
)
SET
  member_id = @member_index,
  post_id   = @post_index;


-- FREE_LIKE
LOAD DATA LOCAL INFILE 'free_like.csv'
INTO TABLE free_like
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
IGNORE 1 ROWS
(
  @member_index,
  @post_index
)
SET
  member_id = @member_index,
  post_id   = @post_index;

-- COMMENT_LIKE
LOAD DATA LOCAL INFILE 'comment_like.csv'
INTO TABLE comment_like
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
IGNORE 1 ROWS
(
  @member_index,
  @comment_index
)
SET
  member_id  = @member_index,
  comment_id = @comment_index;

-- IMAGE (S3 key 기반)
LOAD DATA LOCAL INFILE 'image.csv'
INTO TABLE image
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
IGNORE 1 ROWS
(
  type,
  @type_id,
  url,
  order_num
)
SET type_id = @type_id;

-- 집계 컬럼(좋아요/댓굴수) 업데이트
UPDATE free_post p
LEFT JOIN (
  SELECT post_id, COUNT(*) cnt
  FROM free_like
  GROUP BY post_id
) l ON p.id = l.post_id
SET p.like_count = IFNULL(l.cnt, 0);

UPDATE free_post p
LEFT JOIN (
  SELECT post_id, COUNT(*) cnt
  FROM comment
  GROUP BY post_id
) c ON p.id = c.post_id
SET p.comment_count = IFNULL(c.cnt, 0);

UPDATE comment c
LEFT JOIN (
  SELECT comment_id, COUNT(*) cnt
  FROM comment_like
  GROUP BY comment_id
) l ON c.id = l.comment_id
SET c.like_count = IFNULL(l.cnt, 0);

-- 커밋 & 설정 복구
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
SET UNIQUE_CHECKS = 1;
SET autocommit = 1;

