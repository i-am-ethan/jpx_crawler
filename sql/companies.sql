-- テーブル作成
CREATE TABLE IF NOT EXISTS companies (
    id SERIAL PRIMARY KEY,
    listing_date TEXT,
    company_name TEXT,
    market TEXT
);

-- created_at, updated_at, deleted_atカラムを追加
ALTER TABLE companies ADD COLUMN created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE companies ADD COLUMN updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE companies ADD COLUMN deleted_at TIMESTAMPTZ;

-- company_urlカラムを追加
ALTER TABLE companies ADD COLUMN company_url TEXT;
