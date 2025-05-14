CREATE TABLE IF NOT EXISTS s2sinfo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    public_ip VARCHAR(45),
    computer_name VARCHAR(255),
    mac_address VARCHAR(17),
    country VARCHAR(2),
    system_info JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);