from rolepermissions.roles import AbstractUserRole


class Developer(AbstractUserRole):
    available_permissions = {
        # Tags
        'access_server': True,
        'access_testing': True,
        'access_sources': True,
        'access_admin': False,
        # Templates
        'create_server_template': False,
        'read_server_template': False,
        'update_server_template': False,
        'delete_server_template': False,
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
        # Sources - Robot
        'create_robot': True,
        'read_robot': True,
        'update_robot': True,
        'delete_robot': True,
        # Sources - Libraries
        'create_libraries': True,
        'read_libraries': True,
        'update_libraries': True,
        'delete_libraries': True,
        # Sources - Product
        'create_product': False,
        'read_product': False,
        'update_product': False,
        'delete_product': False,
        # Phases
        'create_phases': False,
        'read_phases': False,
        'update_phases': False,
        'delete_phases': False,
        # Commands
        'create_commands': True,
        'read_commands': True,
        'update_commands': True,
        'delete_commands': True,
        # Users
        'create_users': False,
        'read_users': False,
        'update_users': False,
        'delete_users': False,
        # Arguments
        'create_argument': True,
        'read_argument': True,
        'update_argument': True,
        'delete_argument': True,
    }


class Tester(AbstractUserRole):
    available_permissions = {
        # Tags
        'access_server': False,
        'access_testing': True,
        'access_sources': False,
        'access_admin': False,
        # Test Case
        'read_test_case': True,
        # Test Suite
        'read_test_suite': True,
        # Collection
        'read_collection': True,
        # Imported Script
        'read_imported_script': True,
        # Scripts
        'run_scripts': True,
    }


class Auditor(AbstractUserRole):
    available_permissions = {
        # Tags
        'access_server': True,
        'access_testing': True,
        'access_sources': True,
        'read_server_template': True,
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
        'read_keyword': True,
        # Test Case
        'read_test_case': True,
        # Test Suite
        'read_test_suite': True,
        # Collection
        'read_collection': True,
        # Imported Script
        'read_imported_script': True,
        # Sources - Robot
        'read_robot': True,
        # Sources - Libraries
        'read_libraries': True,
        # Sources - Product
        'read_product': True,
        # Commands
        'read_commands': True,
        # Phases
        'read_phases': True,
    }


class Owner(AbstractUserRole):
    available_permissions = {
        # Tags
        'access_server': True,
        'access_testing': True,
        'access_sources': True,
        'access_admin': False,
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
        # Sources - Robot
        'create_robot': True,
        'read_robot': True,
        'update_robot': True,
        'delete_robot': True,
        # Sources - Libraries
        'create_libraries': True,
        'read_libraries': True,
        'update_libraries': True,
        'delete_libraries': True,
        # Commands
        'create_commands': True,
        'read_commands': True,
        'update_commands': True,
        'delete_commands': True,
    }
