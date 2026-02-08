-- =====================================================
-- aggregate.sql
-- 목적: like_count / comment_count 집계 반영
-- =====================================================

START TRANSACTION;

-- 게시글 댓글 수 집계
UPDATE free_post p
LEFT JOIN (
    SELECT post_id, COUNT(*) AS cnt
    FROM comment
    WHERE deleted_at IS NULL
    GROUP BY post_id
) c ON p.id = c.post_id
SET p.comment_count = IFNULL(c.cnt, 0);

-- 게시글 좋아요 수 집계
UPDATE free_post p
LEFT JOIN (
    SELECT post_id, COUNT(*) AS cnt
    FROM free_like
    GROUP BY post_id
) l ON p.id = l.post_id
SET p.like_count = IFNULL(l.cnt, 0);

-- 댓글 좋아요 수 집계
UPDATE comment c
LEFT JOIN (
    SELECT comment_id, COUNT(*) AS cnt
    FROM comment_like
    GROUP BY comment_id
) l ON c.id = l.comment_id
SET c.like_count = IFNULL(l.cnt, 0);

COMMIT;
