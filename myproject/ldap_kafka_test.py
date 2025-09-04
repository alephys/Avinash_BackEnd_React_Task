#ldap_kafka_test.py
from ldap3 import Server, Connection, ALL
from ldap_config import LDAP_SERVER_URL, GROUP_BASE, USER_BASE, BIND_DN, BIND_PASSWORD

# Connect to LDAP
server = Server(LDAP_SERVER_URL, get_info=ALL)
conn = Connection(server, user=BIND_DN, password=BIND_PASSWORD, auto_bind=True)

print("Connected to LDAP successfully!")

# Search for users with additional attributes
conn.search(USER_BASE, "(objectClass=inetOrgPerson)", attributes=['uid', 'cn', 'userPassword'])
print("Users found with details:")
for entry in conn.entries:
    print(f"DN: {entry.entry_dn}, uid: {entry.uid}, cn: {entry.cn}, password: {entry.userPassword}")

# Fetch groups (optional, unchanged)
conn.search(GROUP_BASE, "(objectClass=posixGroup)", attributes=['cn', 'memberUid'])
print("\nGroups found:")
for entry in conn.entries:
    print(entry.cn, "members:", entry.memberUid)

conn.unbind()