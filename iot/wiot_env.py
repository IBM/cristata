import os
import sys

try:
    WIOT_ORG=os.environ['WIOT_ORG']
    WIOT_KEY=os.environ['WIOT_KEY']
    WIOT_TKN=os.environ['WIOT_TKN']
except:
    print('one or more of the following enviroment variables not set')
    print('WIOT_ORG')
    print('WIOT_KEY')
    print('WIOT_TKN')
    print('see')
    print('bx service key-show cristata-iot credentials')
    sys.exit(1)
