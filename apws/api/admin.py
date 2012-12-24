from django.contrib import admin
from models import *

# Admin models
class CustomerAdmin(admin.ModelAdmin):
    list_display        = ('id', 'owner_name', 'owner_email', 'service_plan', 'created_at',)
    list_display_links  = ('owner_name',)
    list_filter         = ('service_plan',)
    ordering            = ('id',)
    search_fields       = ('owner_name', 'owner_email',)

class OVPNConfigAdmin(admin.ModelAdmin):
    list_display        = ('id', 'config_name', 'config_host', 'online_status', 'updated_at',)
    list_display_links  = ('config_name',)
    list_filter         = ('config_host',)
    ordering            = ('id',)
    search_fields       = ('config_name',)

class RootfsConfigAdmin(admin.ModelAdmin):
    list_display        = ('id', 'release_ver', 'relesae_hw', 'created_at',)
    list_display_links  = ('release_ver',)
    ordering            = ('id',)
    search_fields       = ('release_ver', 'relesae_hw', 'relesae_note',)

class DeviceAdmin(admin.ModelAdmin):
    list_display        = ('id', 'mac_addr', 'mac_hash', 'model', 'sn', 'wifi_psk', 'root_pass', 'holder', 'ovpn_config', 'issue_date', 'last_ovpn_update', 'last_rootfs_update', 'last_status_report', 'last_network_report',)
    list_display_links  = ('mac_addr',)
    list_filter         = ('model',)
    ordering            = ('id',)
    search_fields       = ('mac_addr', 'mac_hash',)

class StatusReportAdmin(admin.ModelAdmin):
    list_display        = ('id', 'device', 'online', 'vpn_online', 'openwrt_ver', 'rootfs_ver', 'ovpn_config', 'ip_addr', 'reported_at',)
    list_display_links  = ('id',)
    list_filter         = ('device',)
    ordering            = ('-id',)

class NetworktReportAdmin(admin.ModelAdmin):
    list_display        = ('id', 'device', 'speed_mb', 'tun_read', 'tun_write', 'reported_at',)
    list_display_links  = ('id',)
    list_filter         = ('device',)
    ordering            = ('-id',)

class ClientLogAdmin(admin.ModelAdmin):
    list_display        = ('id', 'device', 'logfile', 'reported_at',)
    list_display_links  = ('id',)
    list_filter         = ('device',)
    ordering            = ('-id',)

class NodeTestPoolAdmin(admin.ModelAdmin):
    list_display        = ('device', 'current_result', 'updated_at',)
    list_display_links  = ('device',)
    search_fields       = ('device',)
    ordering            = ('-id',)

class FailedOVPNPoolAdmin(admin.ModelAdmin):
    list_display        = ('id', 'device', 'ovpn_config', 'issue', 'reported_at',)
    list_display_links  = ('id',)
    list_filter         = ('ovpn_config',)
    ordering            = ('-id',)

# Models registration
admin.site.register(Customer, CustomerAdmin)
admin.site.register(OVPNConfig, OVPNConfigAdmin)
admin.site.register(RootfsConfig, RootfsConfigAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(StatusReport, StatusReportAdmin)
admin.site.register(NetworktReport, NetworktReportAdmin)
admin.site.register(ClientLog, ClientLogAdmin)
admin.site.register(FailedOVPNPool, FailedOVPNPoolAdmin)
admin.site.register(NodeTestPool, NodeTestPoolAdmin)