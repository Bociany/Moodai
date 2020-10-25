from pymemcache.client.base import Client
import secrets
import hashlib

memcached_client = Client(("localhost", 11211))
TOKEN_EXPIRATION = 60*60*24

print("auth: memcached hot token cache backend started!")

# Generates a new token for a user
def generate_token(id):
	token = secrets.token_urlsafe(32)
	memcached_client.set(token, id, expire=TOKEN_EXPIRATION)
	return token

def remove_token(token):
	if (token_exists(token)):
		memcached_client.delete(token)

def token_exists(token):
	return memcached_client.get(token) is not None

# Verifies if a token is proper
def verify_token(token):
	cached_id = memcached_client.get(token)
	if cached_id is not None:
		return cached_id

def hash_multiple(arr):
	hash = hashlib.sha3_256()
	for obj in arr:
		hash.update(obj.encode('utf-8'))

	return hash.hexdigest()
