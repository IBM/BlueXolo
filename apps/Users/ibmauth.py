from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES

# Define the ldap-server Bluegpage IBM
AUTH_LDAP_SERVER = 'bluepages.ibm.com'


class LDAPBackend():
    """Class to verify and authetificate the user"""

    def check_user(self, email):
        server = Server(AUTH_LDAP_SERVER, get_info=ALL)
        connect = Connection(server)
        base = "ou=bluepages,o=ibm.com"
        auth_filters = "(&(objectclass=person) (mail={0}))".format(email)

        try:
            connect.bind()
            result = connect.search(base, auth_filters, attributes=ALL_ATTRIBUTES)
            if result:
                connect.search(base, auth_filters, attributes=ALL_ATTRIBUTES)
                name = connect.entries[0].givenName[0]
                last = connect.entries[0].sn[0]
                connect.unbind()
                return result, name, last
            else:
                return True, None
        except Exception as e:
            print("Check that VPN connection")
            return False, None

    def authetification_ibm_user(self, email, passwd):
        server = Server(AUTH_LDAP_SERVER, get_info=ALL)
        connect = Connection(server)
        base = "ou=bluepages,o=ibm.com"
        auth_filters = "(&(objectclass=person) (mail=%s))" % email

        if not connect.bind():
            print("Check that VPN connection")
            return False
        else:
            connect.search(base, auth_filters, attributes=ALL_ATTRIBUTES)
            uid = connect.entries[0].uid
            c = connect.entries[0].c
            user_dn = "uid=" + uid + ",c=" + c + "," + base
            auth = Connection(server, user=user_dn, password=passwd)
            if not auth.bind():
                return False
            else:
                auth.unbind()
                return True
