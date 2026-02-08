# 🧪KOPLE 더미 데이터 생성 & 삽입 가이드 (운영/스테이징 공용)

> **이 문서는 무엇을 위한 건가요?**
> 
> - 운영 / 스테이징 DB에서 **실제 서비스와 유사한 데이터 환경**을 재현하기 위함
> - 커뮤니티, 추천, 검색, 관리자 페이지, 성능 테스트에 사용
> - **더미 생성 → 삽입 → 집계 → 초기화** 전 과정을 표준화
>     
>     cf. image는 없음. 대댓글 없음. 내 로컬 폴더 path 그대로 샘플에 넣어둠(수정해서 사용할 것)
>     

---

## 📌 이 문서를 봐야 하는 사람

- 백엔드 개발자
- 프론트엔드 개발자 (API 테스트용)
- 운영/기획자 (관리자 페이지 검증)
- 신규 팀원 온보딩

---

## 🧭 전체 프로세스 한눈에 보기

```
1. Python으로 더미 CSV 생성
2. SSH 터널로 RDS 접속
3. LOAD DATA로 CSV 삽입
4. 좋아요 / 댓글 수 집계
5. 분포 리포트로 품질 확인
6. 필요 시 더미 초기화
```

---

## 📁 더미 데이터 디렉토리 규칙

```
kople-dummy-data/
 └ verYYYYMMDD/
    ├ generate_member_profile.py
    ├ generate_interest.py
    ├ generate_community.py
    ├ member.csv
    ├ profile.csv
    ├ buddy.csv
    ├ member_interest.csv
    ├ free_post.csv
    ├ comment.csv
    ├ free_like.csv
    ├ comment_like.csv
    ├ load_data.sql
    ├ aggregate.sql
    └ truncate.sql
```

> 🔒 **원칙**
> 
> - 더미는 반드시 `ver날짜` 디렉토리로 관리
> - 운영 데이터와 섞이지 않게 **항상 버전 고정**

---

## 👤 회원 / 프로필 더미 규칙

### 회원 수

- `MEMBER_COUNT` 기준 (기본: 50)

### status 분포

- 🎓 **학생 계열 85%**
- 🧳 **비학생 계열 15%**

### status별 제약 조건

| status | university_id | nation_code |
| --- | --- | --- |
| EXCHANGE_STUDENT | 1~145 | KR 제외 랜덤 |
| INTERNATIONAL_STUDENT | 1~145 | KR 제외 랜덤 |
| LANGUAGE_SCHOOL_STUDENT | 1~145 | KR 제외 랜덤 |
| KOREAN_STUDENT | 1~145 | **KR 고정** |
| KOREAN_WORKER | NULL | KR 위주 |
| TOURIST | NULL | 랜덤 |
| FOREIGN_RESIDENT | NULL | 랜덤 |
| OTHER | NULL | 랜덤 |

---

## 🎯 관심사(member_interest) 규칙

- 각 유저당 **1~3개**
- interest_item_id: **1 ~ 41**
- `(member_id, interest_item_id)` UNIQUE 보장
- code ❌ → **id 기준으로만 저장**

---

## 🤝 Buddy 규칙

- 모든 member는 **buddy 1개**
- is_active = true

---

## 📝 커뮤니티 게시글 규칙 (FreePost)

### 제목

- 최대 **80자**
- 질문 / 후기 / 모집 / 경험 공유 톤 섞기

### 본문

- 최대 **1000자**
- 2~3 문단 구성
- 경험 + 질문 구조

### 카테고리

- `CAMPUS`
- `DAILY_TIPS`
- `EATS`
- `ACTIVITY`
- `QNA`

---

## 💬 댓글(Comment) 규칙

- 최대 **500자**
- post_id 랜덤 매핑
- 현재는 parent_id = NULL
    
    (대댓글 구조 확장 가능)
    

---

## ❤️ 좋아요(Like) 규칙

### 게시글 좋아요 (free_like)

- 게시글당 **3~7명**

### 댓글 좋아요 (comment_like)

- 댓글당 **0~5명**
- `(comment_id, member_id)` UNIQUE

---

## 🔐 RDS 접속 방법 (CMD)

```bash
ssh -i maru-ec2.pem -L 3307:RDS_ENDPOINT:3306 ubuntu@EC2_PUBLIC_DNS
```

```bash
mysql --local-infile=1 -h 127.0.0.1 -P 3307 -u maru -p
```

```sql
SHOW VARIABLES LIKE 'local_infile';
-- ON 이어야 함
```

---

## 📥 CSV 삽입 (LOAD DATA)

### 공통 경로 예시

```
C:/Users/semin/dev/kople-dummy-data/ver260206/
```

### ⚠️ 삽입 순서 (중요)

1. member
2. profile
3. buddy
4. member_interest
5. free_post
6. comment
7. free_like
8. comment_like

> FK 에러 대부분은 **순서 문제**
> 

---

## 🔄 좋아요 / 댓글 수 집계 (aggregate.sql)

> CSV 삽입 후 **반드시 실행**
> 

```sql
START TRANSACTION;

-- 게시글 댓글 수
UPDATE free_post p
LEFT JOIN (
    SELECT post_id, COUNT(*) cnt
    FROM comment
    WHERE deleted_at IS NULL
    GROUP BY post_id
) c ON p.id = c.post_id
SET p.comment_count = IFNULL(c.cnt, 0);

-- 게시글 좋아요
UPDATE free_post p
LEFT JOIN (
    SELECT post_id, COUNT(*) cnt
    FROM free_like
    GROUP BY post_id
) l ON p.id = l.post_id
SET p.like_count = IFNULL(l.cnt, 0);

-- 댓글 좋아요
UPDATE comment c
LEFT JOIN (
    SELECT comment_id, COUNT(*) cnt
    FROM comment_like
    GROUP BY comment_id
) l ON c.id = l.comment_id
SET c.like_count = IFNULL(l.cnt, 0);

COMMIT;

```

📌 집계가 안 되면:

- 메인 화면 정렬
- 인기글
- 관리자 통계
    
    전부 왜곡됨
    

---

## 📊 더미 데이터 품질 체크 (리포트 쿼리)

### status 분포

```sql
SELECT status, COUNT(*) FROM profile GROUP BY status;
```

### 관심사 개수 분포

```sql
SELECT interest_count, COUNT(*)
FROM (
  SELECT member_id, COUNT(*) interest_count
  FROM member_interest
  GROUP BY member_id
) t
GROUP BY interest_count;
```

### 카테고리 분포

```sql
SELECT category, COUNT(*) FROM free_post GROUP BY category;
```

---

## 🧹 더미 초기화 (truncate.sql)

> ⚠️ **절대 운영 실데이터에서 실행 금지**
> 

```sql
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE ...
SET FOREIGN_KEY_CHECKS = 1;
```

📌 TRUNCATE는 **롤백 불가**

---

## ♻️ 더미 재사용 가이드

### ✔ 원칙

- CSV 생성 → Python
- 삽입 / 집계 / 초기화 → SQL 파일
- 환경별로 **경로만 변경**

### ✔ 추천 실행 순서

```
1. python generate_*.py
2. mysql < truncate.sql
3. mysql < load_data.sql
4. mysql < aggregate.sql
5. 리포트 쿼리로 검증
```

### ✔ 실행 방법 정리

```bash
# 1. 더미 초기화
mysql --local-infile=1 -h 127.0.0.1 -P 3307 -u maru -p < truncate.sql

# 2. CSV 삽입
mysql --local-infile=1 -h 127.0.0.1 -P 3307 -u maru -p < load_data.sql

# 3. 집계 반영
mysql --local-infile=1 -h 127.0.0.1 -P 3307 -u maru -p < aggregate.sql
```

---
