from rolepermissions.roles import AbstractUserRole


class Developer(AbstractUserRole):
    available_permissions = {
        # Profiles
        'create_server_profile': True,
        'read_server_profile': True,
        'update_server_profile': True,
        'delete_server_profile': True,
        # Parameters
        'create_server_parameter': True,
        'read_server_parameter': True,
        'update_server_parameter': True,
        'delete_server_parameter': True,
        # Keywords
        'create_keyword': True,
        'read_keyword': True,
        'update_keyword': True,
        'delete_keyword': True,
        # Test Cases
        'create_test_case': True,
        'read_test_case': True,
        'update_test_case': True,
        'delete_test_case': True,
        # Test suites
        'create_test_suite': True,
        'read_test_suite': True,
        'update_test_suite': True,
        'delete_test_suite': True,
        # Imported Script
        'create_imported_script': True,
        'read_imported_script': True,
        'update_imported_script': True,
        'delete_imported_script': True,
        # Collection
        'create_collection': True,
        'read_collection': True,
        'update_collection': True,
        'delete_collection': True,
        # Scripts
        'run_scripts': True,
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
