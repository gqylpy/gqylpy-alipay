DROP TABLE resources;
CREATE TABLE resources
(
  id             INT PRIMARY KEY AUTO_INCREMENT,
  name           VARCHAR(1024) UNIQUE          NOT NULL,
  archive        CHAR(40) UNIQUE               NOT NULL, -- 归档, uuid4.zip
  download_count BIGINT UNSIGNED DEFAULT 0     NOT NULL,
  price          DECIMAL(65, 2)  DEFAULT 1.99  NOT NULL,
  buy_count      BIGINT UNSIGNED DEFAULT 0     NOT NULL,
  password       CHAR(7)                       NOT NULL,
  jianshu        TEXT(40960),
  cnblog         TEXT(40960),
  images         VARCHAR(10240),
  create_date    DATETIME        DEFAULT NOW() NOT NULL
);

DROP TABLE orders;
CREATE TAbLE orders
(
  id           INT PRIMARY KEY AUTO_INCREMENT,
  status       TINYINT(1) DEFAULT 0     NOT NULL, -- -1:支付失败 0:待支付 1:支付成功
  rid          INT                      NOT NULL,
  total_amount DECIMAL(65, 2)           NOT NULL, -- 总金额
  trade_no     VARCHAR(128) UNIQUE,               -- 订单号（流水号）
  out_trade_no CHAR(36) UNIQUE          NOT NULL, -- 商家订单号
  buyer_id     VARCHAR(128),                      -- 买方id
  seller_id    VARCHAR(32),                       -- 卖方id
  app_id       VARCHAR(32)              NOT NULL,
  payment_date DATETIME,                          -- 付款时间
  create_date  DATETIME   DEFAULT NOW() NOT NULL, -- 下单日期
  CONSTRAINT fk_orders_resources FOREIGN KEY (rid) REFERENCES resources (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

DROP TABLE mood;
CREATE TABLE mood
(
  id          INT PRIMARY KEY AUTO_INCREMENT,
  name        VARCHAR(1024) UNIQUE   NOT NULL,
  content     TEXT(40960)            NOT NULL,
  create_date DATETIME DEFAULT NOW() NOT NULL
);

DROP TABLE user_cnblog;
CREATE TABLE user_cnblog
(
  id             INT PRIMARY KEY AUTO_INCREMENT,
  is_ok          TINYINT(1) UNSIGNED DEFAULT 1     NOT NULL,
  total_disposed BIGINT UNSIGNED     DEFAULT 0     NOT NULL,
  now_bid        BIGINT UNSIGNED     DEFAULT 0     NOT NULL,
  cookie         VARCHAR(2048)                     NOT NULL,
  home           VARCHAR(128),
  username       VARCHAR(32) UNIQUE                NOT NULL,
  password       VARCHAR(32)                       NOT NULL,
  remark         VARCHAR(128)                      NOT NULL,
  email          VARCHAR(64) UNIQUE                NOT NULL,
  email_pwd      VARCHAR(64)                       NOT NULl,
  phone          CHAR(11)                          NOT NULL,
  create_date    DATETIME            DEFAULT NOW() NOT NULL
);

DROP TABLE archive_cnblog;
CREATE TABLE archive_cnblog
(
  id          INT PRIMARY KEY AUTO_INCREMENT,
  link        VARCHAR(128) UNIQUE    NOT NULL,
  uid         INT                    NOT NULL,
  create_date DATETIME DEFAULT NOW() NOT NULL,
  CONSTRAINT fk_ac_nc FOREIGN KEY (uid) REFERENCES user_cnblog (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

DROP TABLE user_jianshu;
CREATE TABLE user_jianshu
(
  id             INT PRIMARY KEY AUTO_INCREMENT,
  is_ok          TINYINT(1) UNSIGNED DEFAULT 1     NOT NULL,
  total_disposed TINYINT(1) UNSIGNED DEFAULT 0     NOT NULL,
  now_bid        BIGINT UNSIGNED     DEFAULT 0     NOT NULL,
  cookie         VARCHAR(2048)                     NOT NULL,
  notebook_id    CHAR(8) UNIQUE                    NOT NULL, -- 分类id
  home           VARCHAR(128),
  username       VARCHAR(32) UNIQUE                NOT NULL,
  password       VARCHAR(32)                       NOT NULL,
  remark         VARCHAR(128)                      NOT NULL,
  phone          CHAR(11)                          NOT NULL,
  create_date    DATETIME            DEFAULT NOW() NOT NULL
);

DROP TABLE archive_jianshu;
CREATE TABLE archive_jianshu
(
  id          INT PRIMARY KEY AUTO_INCREMENT,
  link        VARCHAR(128) UNIQUE    NOT NULL,
  uid         INT                    NOT NULL,
  create_date DATETIME DEFAULT NOW() NOT NULL,
  CONSTRAINT fk_aj_uj FOREIGN KEY (uid) REFERENCES user_jianshu (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE comment
(
  id          INT PRIMARY KEY AUTO_INCREMENT,
  content     VARCHAR(300) UNIQUE    NOT NULL,
  create_date DATETIME DEFAULT NOW() NOT NULL
);
