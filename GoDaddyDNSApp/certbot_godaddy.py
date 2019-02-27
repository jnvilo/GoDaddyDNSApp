#!/bin/env python
#Key
#9ELgAwGRufU_M6qcGSa8Y1pdMn8K85QnA1
#Secret
#M6qkxMm9NFtcyX5CKxyRPB

import os
from godaddypy import Client, Account
from godaddypy.client import BadResponse 


"CERTBOT_DOMAIN"
"CERTBOT_VALIDATION"
"CERTBOT_TOKEN"

PUBLIC_KEY="9ELgAwGRufU_ToMQ5A8qwim9Vz1qP9yJpN"
SECRET_KEY="ToMT6uRLhxsXR6ZFHEdSS2"


#_acme-challenge.registry.lnxsystems.com


def put_txt(domain, host):

    my_acct = Account(api_key=PUBLIC_KEY, api_secret=SECRET_KEY)
    client = Client(my_acct)

    #Search and delete any old records. 
    res = self.client.get_records(domain, record_type='TXT', name = host)
    for entry in res:
        self.client.delete_records(self.domain, name=self.host)


    #domain: lnxsystems.com
    #host: www
    #data: what o point to 
    client.add_record( domain, {'name':  host , 
                                                'ttl': int(self.ttl), 
                                                'data': self.data, 
                                                'type': 'TXT'})

def cleanup(value):
    pass


def main():
    
    print(os.environ['CERTBOT_DOMAIN'])
    print(os.environ['CERTBOT_VALIDATION'])
    #print(os.environ['CERTBOT_TOKEN'])

    
    
if __name__ == "__main__":
    main()
    