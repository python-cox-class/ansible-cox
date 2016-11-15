#!/usr/bin/env python

import sys
import json
import getpass
from novaclient import client


def main(progname, *args):
    passwd = getpass.getpass('OpenStack Admin password?')
    nt = client.Client(
        '2.0', 'admin', passwd, 'demo',
        auth_url='http://159.203.94.195/identity_admin/v2.0/')
    nt.authenticate()

    listing = get_listing(nt)
    if args[0] == '--list':
        return listing
    elif args[0] == '--host':
        return listing['_meta']['hostvars'][args[1]]
    assert False, 'Unknown options: {}'.format(args)


def get_listing(nt):
    result = []
    hostvars = {}
    for svr in nt.servers.list():
        for a in svr.addresses['private']:
            if a['version'] == 4:
                break
        else:
            assert False, 'Could not find ipv4 addr'
        hostvars[svr.name] = dict(ansible_host=a['addr'])
        result.append(svr.name)
    return {'cox-stack': result, '_meta': {'hostvars': hostvars}}


if __name__ == '__main__':
    print json.dumps(main(*sys.argv))
