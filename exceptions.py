class KBZBAdminBackBaseException(Exception):
    '''Базовое исключение софта'''
    status_code = 400


class AuthorizationException(KBZBAdminBackBaseException):
    '''Исключение при авторизации'''
    status_code = 401
