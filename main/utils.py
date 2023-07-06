def generate_random_string(length):
    import django
    import string
    # '#abcdefghilkmnopqrstuvwxyz0123456789'
    return \
        django.utils.crypto.get_random_string(
            length, string.ascii_lowercase + string.digits + string.punctuation.replace(
                '|\'"`\\', '') + string.ascii_lowercase + string.digits)
    # import secrets
    # return secrets.token_hex(length)  # this guy duplicates the length
