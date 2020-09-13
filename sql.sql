create database douban charset utf8mb4;
CREATE TABLE rent
(
    id           INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    group_id     BIGINT UNSIGNED  NOT NULL DEFAULT 0 COMMENT '组id',
    title        VARCHAR(255)     NOT NULL COMMENT '帖子标题',
    a_id         BIGINT UNSIGNED  NOT NULL COMMENT '帖子id',
    a_created_at DATETIME         NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '帖子创建时间',
    a_updated_at DATETIME         NOT NULL DEFAULT '1970-01-01 00:00:00' COMMENT '帖子更新时间',
    is_del       TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '',
    created_at   TIMESTAMP        NOT NULL DEFAULT current_timestamp,
    updated_at   TIMESTAMP        NOT NULL DEFAULT current_timestamp ON UPDATE current_timestamp,
    UNIQUE a_id (a_id),
    KEY a_up (a_updated_at)
)