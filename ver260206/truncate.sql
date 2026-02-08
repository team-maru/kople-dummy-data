-- =====================================================
-- truncate.sql
-- 목적: 더미 데이터 전체 초기화
-- =====================================================

SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE comment_like;
TRUNCATE TABLE free_like;
TRUNCATE TABLE comment;
TRUNCATE TABLE free_post;
TRUNCATE TABLE member_interest;
TRUNCATE TABLE buddy;
TRUNCATE TABLE profile;
TRUNCATE TABLE member;

SET FOREIGN_KEY_CHECKS = 1;
