#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/20 17:23
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
from .crypt_main import MortalCryptMain


class MortalCrypt(MortalCryptMain):
    """
    MortalCrypt 类提供了多种加密和解密方法的封装，包括 AES、Base64、DES、MD5、RSA、SHA 等算法。
    所有方法均为类方法，可以直接通过类名调用。
    """

    def aes_ecb_encrypt(self, value, key):
        """
        使用 AES ECB 模式对数据进行加密。

        :param value: 需要加密的数据。
        :param key: 加密使用的密钥。
        :return: 加密后的数据。
        """
        return self._aes_ecb_encrypt(value, key)

    def aes_ecb_decrypt(self, value, key):
        """
        使用 AES ECB 模式对数据进行解密。

        :param value: 需要解密的数据。
        :param key: 解密使用的密钥。
        :return: 解密后的数据。
        """
        return self._aes_ecb_decrypt(value, key)

    def aes_cbc_encrypt(self, value, key, iv):
        """
        使用 AES CBC 模式对数据进行加密。

        :param value: 需要加密的数据。
        :param key: 加密使用的密钥。
        :param iv: 初始化向量。
        :return: 加密后的数据。
        """
        return self._aes_cbc_encrypt(value, key, iv)

    def aes_cbc_decrypt(self, value, key, iv):
        """
        使用 AES CBC 模式对数据进行解密。

        :param value: 需要解密的数据。
        :param key: 解密使用的密钥。
        :param iv: 初始化向量。
        :return: 解密后的数据。
        """
        return self._aes_cbc_decrypt(value, key, iv)

    def base64_encrypt(self, value):
        """
        使用 Base64 编码对数据进行加密。

        :param value: 需要加密的数据。
        :return: Base64 编码后的数据。
        """
        return self._base64_encrypt(value)

    def base64_decrypt(self, value):
        """
        使用 Base64 解码对数据进行解密。

        :param value: 需要解密的数据。
        :return: 解码后的数据。
        """
        return self._base64_decrypt(value)

    def des_encrypt(self, value, key):
        """
        使用 DES 算法对数据进行加密。

        :param value: 需要加密的数据。
        :param key: 加密使用的密钥。
        :return: 加密后的数据。
        """
        return self._des_encrypt(value, key)

    def des_decrypt(self, value, key):
        """
        使用 DES 算法对数据进行解密。

        :param value: 需要解密的数据。
        :param key: 解密使用的密钥。
        :return: 解密后的数据。
        """
        return self._des_decrypt(value, key)

    def md5_encrypt(self, value, fmt=None):
        """
        使用 MD5 算法对数据进行加密。

        :param value: 需要加密的数据。
        :param fmt: 输出格式，默认为 None。
        :return: MD5 加密后的数据。
        """
        return self._md5_encrypt(value, fmt)

    def md5_hmac_encrypt(self, value, key, fmt=None):
        """
        使用 HMAC-MD5 算法对数据进行加密。

        :param value: 需要加密的数据。
        :param key: 加密使用的密钥。
        :param fmt: 输出格式，默认为 None。
        :return: HMAC-MD5 加密后的数据。
        """
        return self._md5_hmac_encrypt(value, key, fmt)

    def php_encrypt(self, value, key, iv, base64s=False):
        """
        使用 PHP 风格的加密算法对数据进行加密。

        :param value: 需要加密的数据。
        :param key: 加密使用的密钥。
        :param iv: 初始化向量。
        :param base64s: 是否使用 Base64 编码，默认为 False。
        :return: 加密后的数据。
        """
        return self._php_encrypt(value, key, iv, base64s)

    def php_decrypt(self, value, key, iv, base64s=False):
        """
        使用 PHP 风格的解密算法对数据进行解密。

        :param value: 需要解密的数据。
        :param key: 解密使用的密钥。
        :param iv: 初始化向量。
        :param base64s: 是否使用 Base64 解码，默认为 False。
        :return: 解密后的数据。
        """
        return self._php_decrypt(value, key, iv, base64s)

    def rsa_keys(self):
        """
        生成 RSA 公钥和私钥对。

        :return: 包含公钥和私钥的元组。
        """
        return self._rsa_keys()

    def rsa_encrypt(self, value, pub_key=None, hexs=False):
        """
        使用 RSA 算法对数据进行加密。

        :param value: 需要加密的数据。
        :param pub_key: 公钥，默认为 None。
        :param hexs: 是否使用十六进制编码，默认为 False。
        :return: 加密后的数据。
        """
        return self._rsa_encrypt(value, pub_key, hexs)

    def rsa_decrypt(self, value, pri_key, hexs=False):
        """
        使用 RSA 算法对数据进行解密。

        :param value: 需要解密的数据。
        :param pri_key: 私钥。
        :param hexs: 是否使用十六进制解码，默认为 False。
        :return: 解密后的数据。
        """
        return self._rsa_decrypt(value, pri_key, hexs)

    def sha1_encrypt(self, value, fmt=None):
        """
        使用 SHA1 算法对数据进行加密。

        :param value: 需要加密的数据。
        :param fmt: 输出格式，默认为 None。
        :return: SHA1 加密后的数据。
        """
        return self._sha1_encrypt(value, fmt)

    def sha256_encrypt(self, value, fmt=None):
        """
        使用 SHA256 算法对数据进行加密。

        :param value: 需要加密的数据。
        :param fmt: 输出格式，默认为 None。
        :return: SHA256 加密后的数据。
        """
        return self._sha256_encrypt(value, fmt)

    def sha384_encrypt(self, value, fmt=None):
        """
        使用 SHA384 算法对数据进行加密。

        :param value: 需要加密的数据。
        :param fmt: 输出格式，默认为 None。
        :return: SHA384 加密后的数据。
        """
        return self._sha384_encrypt(value, fmt)

    def sha512_encrypt(self, value, fmt=None):
        """
        使用 SHA512 算法对数据进行加密。

        :param value: 需要加密的数据。
        :param fmt: 输出格式，默认为 None。
        :return: SHA512 加密后的数据。
        """
        return self._sha512_encrypt(value, fmt)

    def token_encrypt(self, data, key, exp_time=86400, issuer=None):
        """
        生成加密的 Token。

        :param data: 需要加密的数据。
        :param key: 加密使用的密钥。
        :param exp_time: Token 的有效期，默认为 86400 秒（1 天）。
        :param issuer: Token 的发行者，默认为 None。
        :return: 加密后的 Token。
        """
        return self._token_encrypt(data, key, exp_time, issuer)

    def token_decrypt(self, token, key, issuer=None):
        """
        解密 Token 并获取原始数据。

        :param token: 需要解密的 Token。
        :param key: 解密使用的密钥。
        :param issuer: Token 的发行者，默认为 None。
        :return: 解密后的数据。
        """
        return self._token_decrypt(token, key, issuer)
