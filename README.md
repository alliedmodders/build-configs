buildbot-configs
================

Buildbot configuration files for AM CI. To deploy:

 * Create a master.
 * `ln -s build-configs/masters am`
 * `ln -s build-configs/masters/<project>/master.cfg master.cfg`
 * Create a `changehook.passwd` and `<project>.yml` file.

The `changehook.passwd` file should have one line, like:
```
username:password
```

The `.yml` file should look roughly like:
```
global:
  url-path: /project/
  slave-password: ***

  master-admins:
    - guy@guy.com

  slave-admins:
    - guy@guy.com

  mail:
    from: whatever@local
    to:
      - gal@gal.com

  ldap:
    host: ldap://19.28.30.103/
    basedn: ou=People,dc=crabs,dc=org
    groupdn: cn=whateves,ou=Group,dc=crabs,dc=org
    search: (mail=%s)

  web:
    port: ***
    github: changehook.passwd
```
