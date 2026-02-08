-- =====================================================
-- load_data.sql
-- 목적: 더미 CSV 데이터를 DB에 삽입
-- 주의: FK 순서 절대 변경 금지, 반드시 mysql --local-infile=1 로 접속한 상태에서 실행
-- =====================================================

-- member
LOAD DATA LOCAL INFILE 'C:/Users/semin/dev/kople-dummy-data/ver260206/member.csv'
INTO TABLE member
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- profile (university_id NULL 처리)
LOAD DATA LOCAL INFILE 'C:/Users/semin/dev/kople-dummy-data/ver260206/profile.csv'
INTO TABLE profile
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
 id,
 member_id,
 nickname,
 nickname_last_changed_at,
 birth_date,
 gender,
 nation_code,
 @university_id,
 status,
 created_at,
 updated_at,
 deleted_at
)
SET university_id = NULLIF(@university_id, '');

-- buddy
LOAD DATA LOCAL INFILE 'C:/Users/semin/dev/kople-dummy-data/ver260206/buddy.csv'
INTO TABLE buddy
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- member_interest (interest_item_id 기준)
LOAD DATA LOCAL INFILE 'C:/Users/semin/dev/kople-dummy-data/ver260206/member_interest.csv'
INTO TABLE member_interest
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
 member_id,
 interest_item_id
);

-- free_post
LOAD DATA LOCAL INFILE 'C:/Users/semin/dev/kople-dummy-data/ver260206/free_post.csv'
INTO TABLE free_post
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- comment (parent_id NULL 처리)
LOAD DATA LOCAL INFILE 'C:/Users/semin/dev/kople-dummy-data/ver260206/comment.csv'
INTO TABLE comment
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
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
 deleted_at
)
SET parent_id = NULLIF(@parent_id, '');

-- free_like (게시글 좋아요)
LOAD DATA LOCAL INFILE 'C:/Users/semin/dev/kople-dummy-data/ver260206/free_like.csv'
INTO TABLE free_like
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
 member_id,
 post_id
);

-- comment_like (댓글 좋아요)
LOAD DATA LOCAL INFILE 'C:/Users/semin/dev/kople-dummy-data/ver260206/comment_like.csv'
INTO TABLE comment_like
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
 member_id,
 comment_id
);
