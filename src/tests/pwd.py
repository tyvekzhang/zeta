import hashlib

# 1. 定义输入和盐值（使用代码中的默认值）
plain_password = "Admin1"
salt = "default_salt_placeholder"

# 2. 拼接密码和盐值
data_to_hash = (plain_password + salt).encode('utf-8')

# 3. 使用 SHA-256 计算哈希值
calculated_hash = hashlib.sha256(data_to_hash).hexdigest()

# 结果
print(calculated_hash)