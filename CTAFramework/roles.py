from rolepermissions.roles import AbstractUserRole


class Developer(AbstractUserRole):
    available_permissions = {
        'create_server_profile': True,
        'read_server_profile': True,
        'update_server_profile': True,
        'delete_server_profile': True,
        'create_server_parameter': True,
        'read_server_parameter': True,
        'update_server_parameter': True,
        'delete_server_parameter': True,
    }


class Tester(AbstractUserRole):
    available_permissions = {

    }


class Auditor(AbstractUserRole):
    available_permissions = {
        'create_server_profile': True,
    }


class Owner(AbstractUserRole):
    available_permissions = {
        'create_server_profile': True,
    }
