from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',

    # APIs for update/
    url(r'update/get-lastest-rootfs/(?P<mac_hash>\w+)/(?P<current_rootfs>\w+)$', Api_GetLastestRootfs,
        name='Api_GetLastestRootfs'),
    url(r'update/get-lastest-ovpn-name/(?P<mac_hash>\w+)$', Api_GetLastestOvpnName,
        name='Api_GetLastestOvpnName'),
    url(r'update/get-ovpn-config-by-name/(?P<mac_hash>\w+)/(?P<config_name>\w+)$', Api_GetOvpnConfigByName,
        name='Api_GetOvpnConfigByName'),
    url(r'update/change-ovpn-config/(?P<mac_hash>\w+)/(?P<current_ovpnconfig>\w+)/(?P<issue>\w+)$', Api_ChangeOvpnConfig,
        name='Api_ChangeOvpnConfig'),

    # APIs for report/
    url(r'report/status/(?P<mac_hash>\w+)/(?P<online>\w+)/(?P<vpn_online>\w+)/(?P<openwrt_ver>\w+)/(?P<rootfs_ver>\w+)/(?P<ovpn_config>\w+)$',
        Api_Status, name='Api_Status'),
    url(r'report/network/(?P<mac_hash>\w+)/(?P<speedtest>\d+\.\d+)/(?P<tun_read>\w+)/(?P<tun_write>\w+)$',
        Api_Network, name='Api_Network'),
    url(r'report/client_log/(?P<mac_hash>\w+)/(?P<filename>.*)$',
        Api_ClientLog, name='Api_ClientLog'),
    url(r'report/node_test/(?P<mac_hash>\w+)/(?P<result>.*)$',
        Api_NodeTest, name='Api_NodeTest'),
)