from flask_restplus import reqparse

paginate_or_search = reqparse.RequestParser()
paginate_or_search.add_argument('page', type=int, required=False, default=1, help='Page number')
paginate_or_search.add_argument('limit', type=int, required=False,
                   default=10, help='Results per page {error_msg}')
paginate_or_search.add_argument('q')
