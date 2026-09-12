CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS papers (
    id SERIAL PRIMARY KEY,
    paper_id VARCHAR(50) NOT NULL UNIQUE,
    title VARCHAR(500) NOT NULL,
    authors VARCHAR(500) NOT NULL,
    institution VARCHAR(300) NOT NULL,
    publication VARCHAR(300) NOT NULL,
    publication_date DATE NOT NULL,
    abstract TEXT NOT NULL,
    keywords VARCHAR(500) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_papers_title ON papers(title);
CREATE INDEX IF NOT EXISTS idx_papers_authors ON papers(authors);
CREATE INDEX IF NOT EXISTS idx_papers_publication ON papers(publication);
CREATE INDEX IF NOT EXISTS idx_papers_publication_date ON papers(publication_date);
