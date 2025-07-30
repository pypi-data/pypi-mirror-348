import base64
from typing import Optional, Dict, List

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa


def load_public_key(public_key_str: str) -> rsa.RSAPublicKey:
    """
    从Base64编码字符串加载X.509格式公钥

    参数:
        public_key_str: Base64编码的公钥字符串（需符合X.509 SubjectPublicKeyInfo结构）

    返回:
        RSAPublicKey对象

    异常:
        ValueError: 密钥格式错误时抛出
        TypeError: 密钥类型不匹配时抛出
    """
    try:
        # Base64解码
        der_data = base64.b64decode(public_key_str.encode('utf-8'))

        # 加载DER格式公钥
        public_key = serialization.load_der_public_key(
            der_data,
            backend=default_backend()
        )

        # 类型验证
        if not isinstance(public_key, rsa.RSAPublicKey):
            raise TypeError("密钥不是有效的RSA公钥")

        return public_key
    except Exception as e:
        # 更精确的错误处理
        if isinstance(e, ValueError):
            raise ValueError(f"公钥格式错误: {str(e)}") from e
        elif isinstance(e, TypeError):
            raise TypeError(f"密钥类型错误: {str(e)}") from e
        else:
            raise RuntimeError(f"加载公钥失败: {str(e)}") from e


def load_private_key(private_key_str: str) -> rsa.RSAPrivateKey:
    """
    从Base64编码字符串加载X.509格式公钥

    参数:
        private_key_str: Base64编码的私钥字符串（需符合X.509 SubjectPublicKeyInfo结构）

    返回:
        RSAPrivateKey对象

    异常:
        ValueError: 密钥格式错误时抛出
        TypeError: 密钥类型不匹配时抛出
    """
    try:
        # Base64解码
        der_data = base64.b64decode(private_key_str.encode('utf-8'))

        # 加载DER格式公钥
        pri_key = serialization.load_der_private_key(
            der_data,
            password=None,
            backend=default_backend()
        )

        # 类型验证
        if not isinstance(pri_key, rsa.RSAPrivateKey):
            raise TypeError("密钥不是有效的RSA私钥")

        return pri_key
    except Exception as e:
        # 更精确的错误处理
        if isinstance(e, ValueError):
            raise ValueError(f"私钥格式错误: {str(e)}") from e
        elif isinstance(e, TypeError):
            raise TypeError(f"密钥类型错误: {str(e)}") from e
        else:
            raise RuntimeError(f"加载公钥失败: {str(e)}") from e


def rsa_encrypt(message: bytes, public_key: rsa.RSAPublicKey) -> Optional[bytes]:
    """
    RSA分段加密实现（兼容Java BouncyCastle行为）

    参数:
        message: 原始字节数据
        public_key_str: Base64编码的X.509公钥字符串

    返回:
        加密后的字节数据，失败返回None
    """
    # 空值检查
    if not message or not public_key:
        return None

    try:
        # 加载公钥
        # public_key = load_public_key(public_key_str)  # 使用之前实现的加载方法

        # 验证密钥类型
        if not isinstance(public_key, rsa.RSAPublicKey):
            raise TypeError("Invalid RSA public key type")

        # 计算分段大小
        key_size = public_key.key_size
        chunk_size = key_size // 8 - 11  # PKCS1v1.5的填充长度

        # 分段加密
        encrypted_chunks = []
        for i in range(0, len(message), chunk_size):
            chunk = message[i:i + chunk_size]
            encrypted_chunk = public_key.encrypt(
                chunk,
                padding.PKCS1v15()
            )
            encrypted_chunks.append(encrypted_chunk)

        # 合并结果
        return b''.join(encrypted_chunks)

    except Exception as e:
        # 这里可以添加日志记录（需替换为实际日志模块）
        print(f"Encryption failed. Message: {message[:16]}..., Key: {public_key[:16]}..., Error: {str(e)}")
        return None


def rsa_decrypt(message: bytes, private_key: rsa.RSAPrivateKey) -> Optional[bytes]:
    """
    RSA分段加密实现（兼容Java BouncyCastle行为）

    参数:
        message: 原始字节数据
        public_key_str: Base64编码的X.509公钥字符串

    返回:
        加密后的字节数据，失败返回None
    """
    # 空值检查
    if not message or not private_key:
        return None

    try:
        # 加载公钥
        # public_key = load_public_key(public_key_str)  # 使用之前实现的加载方法

        # 验证密钥类型
        if not isinstance(private_key, rsa.RSAPrivateKey):
            raise TypeError("Invalid RSA private key type")

        # 计算分段大小
        key_size = private_key.key_size
        chunk_size = 1024 // 8  # PKCS1v1.5的填充长度

        # 分段加密
        decrypted_chunks = []
        for i in range(0, len(message), chunk_size):
            chunk = message[i:i + chunk_size]
            encrypted_chunk = private_key.decrypt(
                chunk,
                padding.PKCS1v15()
            )
            decrypted_chunks.append(encrypted_chunk)

        # 合并结果
        return b''.join(decrypted_chunks)

    except Exception as e:
        # 这里可以添加日志记录（需替换为实际日志模块）
        print(f"Encryption failed. Message: {message[:16]}..., Key: {private_key[:16]}..., Error: {str(e)}")
        return None


def encrypt_data(data_str, public_key_str):
    """RSA/None/PKCS1Padding加密"""
    public_key = load_public_key(public_key_str)
    return encrypt_data_key(data_str, public_key)


def encrypt_data_key(data_str, public_key: rsa.RSAPublicKey) -> str:
    """RSA/None/PKCS1Padding加密"""
    encrypted = rsa_encrypt(data_str.encode("utf-8"), public_key)
    return base64.b64encode(encrypted).decode("utf-8")


def decrypt_data(data_str: str, private_key_str: str) -> str:
    """RSA/None/PKCS1Padding加密"""
    private_key = load_private_key(private_key_str)
    return decrypt_data_key(data_str, private_key)


def decrypt_data_key(data_str: str, private_key: rsa.RSAPrivateKey) -> str:
    """RSA/None/PKCS1Padding加密"""
    decrypted = rsa_decrypt(base64.b64decode(data_str.encode("utf-8")), private_key)
    return decrypted.decode("utf-8")


def get_sign_src_skip_null(sec_map: Dict[str, str], is_use_key: bool, split: str) -> str:
    """
    生成签名字符串（跳过空值和sign字段）

    参数:
        sec_map (Dict[str, str]): 待签名的参数字典
        is_use_key (bool): 是否拼接键名
        split (str): 参数分隔符

    返回:
        str: 拼接后的签名字符串
    """
    content_parts: List[str] = []

    # 1. 对键进行排序
    sorted_keys = sorted(sec_map.keys())

    for key in sorted_keys:
        # 2. 跳过sign字段
        if key == "sign":
            continue

        value = sec_map[key]

        # 3. 跳过空字符串值
        if not isinstance(value, str) or not value.strip():
            continue

        # 4. 根据标识决定拼接格式
        if is_use_key:
            part = f"{key}={value}"
        else:
            part = value

        content_parts.append(part)

    # 5. 拼接最终字符串
    return split.join(content_parts)


def rsa_sign(message: str, private_key: rsa.RSAPrivateKey) -> Optional[str]:
    """
    使用 RSA 私钥进行 SHA1withRSA 签名

    参数:
        message: 要签名的原始字符串
        private_key: 已加载的 RSA 私钥对象

    返回:
        Base64 编码的签名字符串，失败时返回 None
    """
    try:
        # 验证密钥类型
        if not isinstance(private_key, rsa.RSAPrivateKey):
            raise TypeError("无效的 RSA 私钥类型")

        # 将消息转换为 UTF-8 字节
        message_bytes = message.encode('utf-8')

        # 使用 SHA1 哈希算法和 PKCS1v1.5 填充
        signature_bytes = private_key.sign(
            message_bytes,
            padding.PKCS1v15(),
            hashes.SHA1()
        )

        # Base64 编码并转换为字符串
        return base64.b64encode(signature_bytes).decode('utf-8')

    except Exception as e:
        # 这里可以替换为实际日志记录
        print(f"签名失败 - 消息: {message[:20]}..., 错误: {str(e)}")
        return None


def rsa_sign_str(message: str, private_key_str: str) -> Optional[str]:
    pri_key = load_private_key(private_key_str)
    return rsa_sign(message, pri_key)


def verify_sign(message: str, sign_str: str, public_key: rsa.RSAPublicKey) -> bool:
    """
      使用 RSA 公钥进行 SHA1withRSA 验签

      参数:
          message: 前面信息
          private_key: 已加载的 RSA 公钥对象

      返回:
          是否验签通过
      """
    try:
        # 验证密钥类型
        if not isinstance(public_key, rsa.RSAPublicKey):
            raise TypeError("无效的 RSA 公钥类型")

        # 准备数据
        message_bytes = message.encode('utf-8')
        signature = base64.b64decode(sign_str)

        # 使用 SHA1 哈希算法和 PKCS1v1.5 填充
        public_key.verify(
            signature,
            message_bytes,
            padding.PKCS1v15(),
            hashes.SHA1()
        )
        return True
    except InvalidSignature as e:
        print("签名验证失败", e)
        return False
    except (ValueError, TypeError) as e:
        print("参数格式错误: %s", str(e))
        return False
    except Exception as e:
        print("验证过程中发生意外错误: %s", str(e))
        return False


def verify_sign_str(message: str, sign_str: str, public_key_str: str) -> bool:
    """
      使用 RSA 公钥进行 SHA1withRSA 验签

      参数:
          message: 前面信息
          private_key: 已加载的 RSA 公钥对象

      返回:
          是否验签通过
      """
    public_key = load_public_key(public_key_str)
    return verify_sign(message, sign_str, public_key)

# sign_str = "aaaaaa"
# sign = rsa_sign_str(sign_str, MER_PRI_KEY)
# res = verify_sign(sign_str, sign, load_public_key(MER_PUB_KEY))
# print(res)

# payload = {"order_no": "20250517212505000001",
#            "total_amount": "1",
#            "pay_scene": "0",
#            "account_type": "ALIPAY,WECHAT,UQRCODEPAY",
#            "mer_no": "M00000004"}
# payload_json = json.dumps(payload)
# print("payload_json:", payload_json)
# req_enc = encrypt_data(payload_json, MOSS_PUB_KEY)
# print("req_enc:", req_enc)
# print("=" * 30)
#
# api_heard = {
#     "businessChannel": "MCPSERVER",
#     "channelId": "API",
#     "requestTime": "20250517232801",
#     "serviceId": "lfops.moss.order.pay",
#     "serviceSn": "11a5b82e11ee4dfba40bbad702c54f05",
#     "versionId": "1.0"
# }
#
# # 请求头排序
# req_head_tree_map = OrderedDict(sorted(api_heard.items(), key=lambda item: item[0]))
# req_head_tree_map_json = json.dumps(req_head_tree_map)
# print("req_head_tree_map_json:", req_head_tree_map_json)
#
# sign_map = {
#     "head": req_head_tree_map_json,
#     "requestEncrypted": req_enc
# }
#
# sign_str = get_sign_src_skip_null(sign_map, True, "&")
# print("sign_str:", sign_str)
# sign = rsa_sign_str(sign_str, MER_PRI_KEY)
# print("sign:", sign)
#
# request = {
#     "head": req_head_tree_map,
#     "requestEncrypted": req_enc,
#     "sign": sign
# }
# req_json = json.dumps(request)
# print("request:", request)
#
#
# print("=" * 30)
# head_tree_map = OrderedDict(sorted(api_heard.items(), key=lambda item: item[0]))
# head_tree_map_json = json.dumps(head_tree_map)
# print("head_tree_map_json:", head_tree_map_json)
#
# resSignMap = {
#     "head": head_tree_map_json,
#     "requestEncrypted": req_enc
# }
#
# resSignStr = get_sign_src_skip_null(resSignMap, True, "&")
# print("sign_str:", resSignStr)
# res = verify_sign(sign_str, sign, load_public_key(MER_PUB_KEY))
# print(res)


# import hashlib
# data_bytes = "刘航".encode("utf-8")
# hash_python = hashlib.sha256(data_bytes).digest()
# print(base64.b64encode(hash_python).decode('utf-8'))
#
# import hashlib
# hash_python = hashlib.sha256(data_bytes).hexdigest()
# print("Python哈希:", hash_python)
