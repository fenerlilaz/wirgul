import ldap
import ldap.modlist as modlist
from django.conf import settings
from web.models import FirstTimeUser

class LdapHandler:

    def __init__(self):
        self.servername = "".join(["ldap://",settings.LDAP_SERVER])  # 127.0.0.1
        self.admin_dn = settings.LDAP_ADMIN_DN  # dn
        self.admin_passwd = settings.LDAP_PASSWORD  # passwd

    def connect(self):
        self.server = ldap.initialize(self.servername)  # ldap.open()
        self.server.protocol_version = ldap.VERSION3

    def bind(self):
        self.server.bind_s(self.admin_dn, self.admin_passwd)

    def unbind(self):
        self.server.unbind_s()

    def add(self,name,middle_name,surname,email,passwd):
        attrs = {}
        if email.find("@gmail.com") != -1:
                mail_adr = email.split("@")
                email = mail_adr[0]
                dn= "".join(["mail=",email,"@comu.edu.tr,ou=personel,ou=people,dc=comu,dc=edu,dc=tr"])
                attrs['mail'] = "".join([email,"@comu.edu.tr"])
        else:
            dn="mail="+email+"comu.edu.tr,ou=personel,ou=people,dc=comu,dc=edu,dc=tr"
            attrs['mail'] = email
        attrs['objectclass'] = ['organizationalPerson','person','inetOrgPerson']
        attrs['givenName'] = " ".join([name,middle_name])
        attrs['sn'] = surname
        attrs['cn'] = " ".join([name,middle_name,surname])
        attrs['userPassword'] = passwd
        ldif = modlist.addModlist(attrs)
        self.server.add_s(dn,ldif)

    def search(self,email):
        base_dn = "ou=people,dc=comu,dc=edu,dc=tr"
        if email.find("@gmail.com") != -1:
            mail_adr = email.split("@")
            email = mail_adr[0]
        filter = "".join(['mail=',email])
        self.results = self.server.search_s(base_dn,ldap.SCOPE_SUBTREE,filter)
        return self.results

