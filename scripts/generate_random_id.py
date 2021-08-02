import uuid


def generate_id():
	uid = uuid.uuid4().hex[:6].upper()
	return uid