def get_user(auth_token):
    from bucketlist.models import User

    if auth_token:
        user_id = User.decode_auth_token(auth_token)

        if not isinstance(user_id, str):
            user = User.query.filter_by(id=user_id).first()
            return user
        return {
            'status': 'fail',
            'message': user_id
        }
    return {
        'status': 'fail',
        'message': 'Provide a valid auth token'
    }

def bucket_content(bucketlist):
    items = [item for item in bucketlist.items.all()]
    response = {
        'id': bucketlist.id,
        'name': bucketlist.name,
        'items': items,
        'date_created': bucketlist.date_created,
        'date_modified': bucketlist.date_modified,
        'created_by': bucketlist.created_by
    }
    return response

def invalid_email(email):
    if '@' not in email:
        return True
    split_email = email.split('@')
    if len(split_email) > 2:
        return True
    if '.' not in split_email[1]:
        return True
    return False
