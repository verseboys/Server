# coding: utf-8

from django.contrib.auth.hashers import BasePasswordHasher
from django.contrib.auth.hashers import OrderedDict, mask_hash, constant_time_compare, force_bytes, _

import hashlib

class MediecoMD5PasswordHasher(BasePasswordHasher):
    """
    以下代码抄自 django.contrib.auth.hashers，只是将 salt + password 修改为 password + salt
    """
    algorithm = "medieco_md5"

    def encode(self, password, salt):
        assert password is not None
        assert salt and '$' not in salt
        hash = hashlib.md5(force_bytes(password + salt)).hexdigest()
        return "%s$%s$%s" % (self.algorithm, salt, hash)

    def verify(self, password, encoded):
        algorithm, salt, hash = encoded.split('$', 2)
        assert algorithm == self.algorithm
        encoded_2 = self.encode(password, salt)
        return constant_time_compare(encoded, encoded_2)

    def safe_summary(self, encoded):
        algorithm, salt, hash = encoded.split('$', 2)
        assert algorithm == self.algorithm
        return OrderedDict([
            (_('algorithm'), algorithm),
            (_('salt'), mask_hash(salt, show=2)),
            (_('hash'), mask_hash(hash)),
        ])

    def harden_runtime(self, password, encoded):
        pass
