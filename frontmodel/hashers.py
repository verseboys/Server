#coding:utf-8

import hashlib
import configs

#密码加盐
def make_password(raw_password,salt=None):
	if not salt:
		salt = configs.PASSWORD_SALT
	
	hash_password = hashlib.md5(raw_password+salt).hexdigest()
	return hash_password

#检查密码
def check_password(raw_password,hash_password):
	if not raw_password:
		return False
	tmp_password = make_password(raw_password)
	if tmp_password == hash_password:
		return True
	else:
		return False