# -*- coding: utf-8 -*-
import datetime

from decimal import Decimal
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from models import Device, OVPNConfig, RootfsConfig, NetworktReport, \
    StatusReport, NodeTestPool, ClientLog, FailedOVPNPool


# Views

def Api_GetLastestRootfs(request,
                         mac_hash,
                         current_rootfs):
    """
    View: api.views.Api_GetLastestRootfs

    """

    device = get_object_or_404(Device, mac_hash=mac_hash)
    latest_rootfs = RootfsConfig.objects.order_by('-id')[0]

    if current_rootfs == latest_rootfs.release_ver:
        return HttpResponse("")
    else:
        device.last_rootfs_update=datetime.datetime.now()
        device.save()
        return HttpResponseRedirect(latest_rootfs.release_file.url)

def Api_GetLastestOvpnName(request,
                         mac_hash):
    """
    View: api.views.Api_GetLastestOvpnName

    """

    device = get_object_or_404(Device, mac_hash=mac_hash)
    last_status = device.statusreport_set.order_by('-id')[0]            # performance problem here

    return HttpResponse(last_status.ovpn_config)

def Api_GetOvpnConfigByName(request,
                            mac_hash,
                            config_name):
    """
    View: api.views.Api_GetOvpnConfigByName

    """

    device = get_object_or_404(Device, mac_hash=mac_hash)
    config = get_object_or_404(OVPNConfig, config_name=config_name)

    device.last_ovpn_update = datetime.datetime.now()
    device.save()

    return HttpResponseRedirect(config.config_file.url)

def Api_ChangeOvpnConfig(request,
                         mac_hash,
                         current_ovpnconfig,
                         issue):
    """
    View: api.views.Api_ChangeOvpnConfig

    """

    device = get_object_or_404(Device, mac_hash=mac_hash)
    curent_config = get_object_or_404(OVPNConfig, config_name=current_ovpnconfig)

    # saving in failed pool
    p = FailedOVPNPool(device=device,
        ovpn_config=curent_config,
        issue=issue) # 0|1|2
    p.save()

    # finding a new ovpn config based on test history and ISP connectivity


    # random return a new online config
    online_ovpn = OVPNConfig.objects.filter(online_status=True).exclude(id=curent_config.id)

    if online_ovpn:
        # saving as ovpn update
        device.last_ovpn_update = datetime.datetime.now()
        device.save()
        return HttpResponseRedirect(online_ovpn[0].config_file.url)

    return HttpResponse("1")    # 1 - No availible config

def Api_Status(request,
               mac_hash,
               online,
               vpn_online,
               openwrt_ver,
               rootfs_ver,
               ovpn_config):
    """
    View: api.views.Api_Status

    """

    device = get_object_or_404(Device, mac_hash=mac_hash)

    # get device public IP addr
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = None
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    # saving status
    status = StatusReport(device=device,
        online=online > 0,
        vpn_online=vpn_online > 0,
        openwrt_ver=openwrt_ver,
        rootfs_ver=rootfs_ver,
        ovpn_config=ovpn_config,
        ip_addr=ip)
    status.save()

    return HttpResponse("")

def Api_Network(request,
               mac_hash,
               speedtest,
               tun_read,
               tun_write):
    """
    View: api.views.Api_Network

    """

    SPEEDTEST_FILESIZE = 1.12 # in MB (http://speedtest.sjc01.softlayer.com/speedtest/speedtest/random750x750.jpg)

    device = get_object_or_404(Device, mac_hash=mac_hash)

    # saving status
    speed = round(SPEEDTEST_FILESIZE/float(speedtest), 2)  # standard: MB/s
    net_read = round(float(tun_read)/1048576, 1) # standard: MB
    net_write = round(float(tun_write)/1048576, 1) # standard: MB

    status = NetworktReport(
        device=device,
        speed_mb=Decimal(str(speed)),
        tun_read=Decimal(str(net_read)),
        tun_write=Decimal(str(net_write)))
    status.save()

    return HttpResponse("")

def Api_ClientLog(request,
                  mac_hash,
                  filename):
    """
    View: api.views.Api_ClientLog

    """

    device = get_object_or_404(Device, mac_hash=mac_hash)

    r = ClientLog(device=device,
        logfile=filename)
    r.save()

    return HttpResponse("")

def Api_NodeTest(request,
                 mac_hash,
                 result):
    """
    View: api.views.Api_NodeTest

    """

    device = get_object_or_404(Device, mac_hash=mac_hash)

    if device.nodetestpool_set.all():
        test = NodeTestPool.objects.get(device=device)
        test.current_result = result
        test.save()
    else:
        n = NodeTestPool(device=device,
            current_result=result)
        n.save()

    return HttpResponse("")