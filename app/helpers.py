def clean_dict(request_dict):
	for i in request_dict:
		if request_dict[i] is '' or request_dict[i] is None:
			return False, i
	return True,
