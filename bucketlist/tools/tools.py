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

def doesnt_exist(name):
    return {
        'status': 'fail',
        'message': '{} doesnt exist'.format(name)
    }

def bucketlist_data(bucketlist):
    itemscontent = [item_data(item)
                    for item in bucketlist.items.all()]
    resp = {
        'id': bucketlist.id,
        'name': bucketlist.name,
        'items': itemscontent,
        'date_created': bucketlist.date_created,
        'date_modified': bucketlist.date_modified,
        'created_by': bucketlist.created_by
    }
    return resp

def item_data(item):
    item_content = {'id': item.id,
         'name': item.name,
         'date_created': item.date_created,
         'date_modified': item.date_modified,
         'done': False, }
    return item_content