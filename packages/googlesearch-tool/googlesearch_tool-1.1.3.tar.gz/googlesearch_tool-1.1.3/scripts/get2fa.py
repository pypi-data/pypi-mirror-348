#!/usr/bin/env python3
import pyotp

key = '5WTUTZUEFLQ2OMVF54BEVQL4TE3CWO7Q'
totp = pyotp.TOTP(key)
print(totp.now())
