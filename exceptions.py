class KBZBAdminBackBaseException(Exception):
    '''Базовое исключение софта'''
    status_code = 400


class AuthorizationException(KBZBAdminBackBaseException):
    '''Исключение при авторизации'''
    status_code = 401


class AccessExceptiom(KBZBAdminBackBaseException):
    '''Исключение при недостаточных правах'''
    status_code = 403


class NotFoundException(KBZBAdminBackBaseException):
    '''Исключение если не данные не найдены'''
    status_code = 404
