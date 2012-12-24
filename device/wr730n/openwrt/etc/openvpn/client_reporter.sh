#!/bin/bash

API_HOST='http://ap-ws.dkhvpn.com:8080/api/report'

WIFIMAC=$(ifconfig eth0 | awk '/HWaddr/ {print $5}')
MAC_MD5=$(echo -n $WIFIMAC | md5sum - | cut -c1-32)
OPENWRT_VER=$(cat /etc/openwrt_version)
ROOTFS_VER=$(cat /etc/config/rootfs_ver)
OVPN_CONFIG=$(cat /etc/openvpn/current_ovpn)

api=${1:-'status'}

case $api in 
     'status' )
     API_PATH=status
     ping -q -w 1 -c 1 10.8.0.1 > /dev/null && VPNCONNECTED=1 || VPNCONNECTED=0
     wget --quiet --output-document=/dev/null "$API_HOST/$API_PATH/$MAC_MD5/1/$VPNCONNECTED/$OPENWRT_VER/$ROOTFS_VER/$OVPN_CONFIG"
     ;;

     'network' )
     API_PATH=network
     READ=$(cat /tmp/openvpn-status.log | grep 'TUN/TAP read bytes' | cut -c20-)
     WRITE=$(cat /tmp/openvpn-status.log | grep 'TUN/TAP write bytes' | cut -c21-)
     (time -p wget --quiet --output-document=/dev/null "http://speedtest.sjc01.softlayer.com/speedtest/speedtest/random750x750.jpg") 2>&1 | grep real > /tmp/.dltest
     DLTIME=$(cat /tmp/.dltest | cut -c6-) && rm /tmp/.dltest
     wget --quiet --output-document=/dev/null "$API_HOST/$API_PATH/$MAC_MD5/$DLTIME/$READ/$WRITE"
     ;;

     'client_log' )
     API_PATH=client_log
     LOG_SVR_HOST=ap-ws.dkhvpn.com
     LOG_SVR_PORT=30022
     LOG_SVR_KEY=/root/.ssh/id_rsa
     LOG_SVR_LOGIN=dkhvpn
     LOG_SVR_PATH=/home/dkhvpn/ap-logs
     DATETIME=`date +%Y%m%d%H`
     LOG_SAVED_AS="$DATETIME-$MAC_MD5-openvpn.log"
     
     scp -P $LOG_SVR_PORT -i $LOG_SVR_KEY /tmp/openvpn.log $LOG_SVR_LOGIN@$LOG_SVR_HOST:$LOG_SVR_PATH/$LOG_SAVED_AS && wget --quiet --output-document=/dev/null "$API_HOST/$API_PATH/$MAC_MD5/$LOG_SAVED_AS"
     ;;

     *)
          echo "please run this script with a parameter..."
     ;;
esac
