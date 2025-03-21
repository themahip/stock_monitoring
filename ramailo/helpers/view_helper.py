def get_auth_token(request):
    token = ""
    auth_header = request.META.get('HTTP_AUTHORIZATION', None)
    if auth_header is not None:
        parts = auth_header.split()
        if len(parts) == 2 and parts[0].lower() == 'bearer':
            token = parts[1]
    return token
