# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

# Vars

SERVICE_PACKAGES = (
    (0, 'Free'),
    (1, 'Trial'),
    (2, '1 Year'),
)

DEVICE_MODELS = (
    (0, 'TL-WR703N'),
    (1, 'FWR171-3G'),
)

SERVERS = (
    (0, 'Esther'),
    (1, 'Isaiah'),
    (2, 'Daniel'),
)

OVPN_FAILED_ISSUES = (
    (0, 'NOT_CONNECTED'),
    (1, 'UNSTABLE'),
    (2, 'SLOW'),
)

# Models

class Customer(models.Model):
    """
    Model: Customer

    """

    owner_name          = models.CharField("Nickname", max_length=32)
    owner_email         = models.EmailField("Email")
    service_plan        = models.SmallIntegerField("Current plan", default=0, choices=SERVICE_PACKAGES)
    created_at          = models.DateTimeField("Created", auto_now_add=True)

    def __unicode__(self):
        return self.owner_name

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Customer'

class OVPNConfig(models.Model):
    """
    Model: OVPNConfig

    """

    config_name         = models.CharField("Config Name", unique=True, max_length=32)
    config_host         = models.SmallIntegerField("OVPN Host", default=0, choices=SERVERS)
    config_note         = models.TextField("Description")
    config_file         = models.FileField("File storage", upload_to='ovpn-configs')
    online_status       = models.BooleanField("Is online", default=True)
    updated_at          = models.DateTimeField("Last updated", auto_now=True)

    def __unicode__(self):
        return self.config_name

    class Meta:
        verbose_name = 'Config'
        verbose_name_plural = 'OVPN Config'

class RootfsConfig(models.Model):
    """
    Model: RootfsConfig

    """

    release_ver         = models.CharField("Release Version", db_index=True, max_length=32)
    relesae_hw          = models.CharField("Hardware Compatible", max_length=200)
    relesae_note        = models.TextField("Relesae Notes")
    release_file        = models.FileField("File storage", upload_to='rootfs-releases')
    created_at          = models.DateTimeField("Created time", auto_now_add=True)

    def __unicode__(self):
        return self.release_ver

    class Meta:
        verbose_name = 'Release'
        verbose_name_plural = 'RootFS Release'

class Device(models.Model):
    """
    Model: Device

    """

    mac_addr            = models.CharField("Device MAC-Addr", max_length=17)
    mac_hash            = models.CharField("MAC-Addr hash", max_length=32, unique=True)
    model               = models.SmallIntegerField("Device Model", choices=DEVICE_MODELS)
    sn    	            = models.CharField("Device Factory S/N", max_length=18)
    wifi_psk            = models.CharField("Wireless PSK", max_length=16)
    root_pass           = models.CharField("System root pwd", max_length=16)
    holder      	    = models.ForeignKey(Customer, verbose_name="Holder profile")
    ovpn_config         = models.ForeignKey(OVPNConfig, verbose_name="OpenVPN Server Config")
    issue_date          = models.DateField("Device issued")
    last_ovpn_update    = models.DateTimeField("Last ovpn update", blank=True, null=True)
    last_rootfs_update  = models.DateTimeField("Last device update", blank=True, null=True)
    last_status_report  = models.DateTimeField("Last status report", blank=True, null=True)
    last_network_report = models.DateTimeField("Last network report", blank=True, null=True)

    def __unicode__(self):
        return u'%s(%s)' % (self.mac_addr, self.holder)

    class Meta:
        verbose_name = 'Router'
        verbose_name_plural = 'Device'

class StatusReport(models.Model):
    """
    Model: StatusReport

    """

    device              = models.ForeignKey(Device, verbose_name="Device")
    online              = models.BooleanField("Online")
    vpn_online          = models.BooleanField("VPN Connected")
    openwrt_ver         = models.CharField("Openwrt version", max_length=16)
    rootfs_ver          = models.CharField("RootFS version", max_length=16)
    ovpn_config         = models.CharField("OVPN config name", max_length=32)
    ip_addr             = models.IPAddressField("From IP", default='0.0.0.0')
    reported_at         = models.DateTimeField("Report time", auto_now_add=True)

    class Meta:
        verbose_name = 'Report'
        verbose_name_plural = 'Status Report'

class NetworktReport(models.Model):
    """
    Model: NetworktReport

    """

    device              = models.ForeignKey(Device, verbose_name="Device")
    speed_mb            = models.DecimalField("Speed in MB/s", max_digits=4, decimal_places=2)
    tun_read            = models.DecimalField("Traffic in/MB", max_digits=6, decimal_places=1)
    tun_write           = models.DecimalField("Traffic out/MB", max_digits=6, decimal_places=1)
    reported_at         = models.DateTimeField("Report time", auto_now_add=True)

    class Meta:
        verbose_name = 'Report'
        verbose_name_plural = 'Networkt Report'

class ClientLog(models.Model):
    """
    Model: ClientLog

    """

    device              = models.ForeignKey(Device, verbose_name="Device")
    logfile             = models.FilePathField("Log filename", path="/home/dkhvpn/ap-logs/")
    reported_at         = models.DateTimeField("Report time", auto_now_add=True)

    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Client Log'

class NodeTestPool(models.Model):
    """
    Model: NodeTestPool

    """

    device              = models.ForeignKey(Device, verbose_name="Device", unique=True)
    current_result      = models.CharField("Test Results", max_length=400)
    updated_at         = models.DateTimeField("Updated time", auto_now_add=True)

    class Meta:
        verbose_name = 'Test'
        verbose_name_plural = 'Node Test Pool'

class FailedOVPNPool(models.Model):
    """
    Model: FailedOVPNPool

    """

    device              = models.ForeignKey(Device, verbose_name="Device")
    ovpn_config         = models.ForeignKey(OVPNConfig, verbose_name="OVPN-Config")
    issue               = models.SmallIntegerField("Failed Issue", choices=OVPN_FAILED_ISSUES)
    reported_by         = models.IPAddressField("Report from IP")
    reported_at         = models.DateTimeField("Report time", auto_now_add=True)

    class Meta:
        verbose_name = 'Ovpn'
        verbose_name_plural = 'Failed Ovpn Pool'