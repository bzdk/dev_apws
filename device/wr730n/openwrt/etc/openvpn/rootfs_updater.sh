#!/bin/bash

# skip on development device
WIFIMAC=$(ifconfig eth0 | awk '/HWaddr/ {print $5}')
if [ $WIFIMAC = "EC:17:2F:D6:57:38" ] ;
then
     exit 0
fi

# waiting for wan/internet connected
IPADDR=$( ifconfig eth0 | awk '/inet addr/ {print $2}' | cut -c6- )
while [ $IPADDR == "" ]; do
    sleep 5
done

# run at booting or uptime > 24h
GETUPTIME=$(cat /proc/uptime)
UPTIME=${GETUPTIME%%.*}
if [ $UPTIME -lt 86400 ] ; 
then
     if [ $UPTIME -gt 300 ] ;
     then
          exit 0
     fi
fi

API_HOST="http://ap-ws.dkhvpn.com:8080/api/update"
WIFIMAC=$(ifconfig eth0 | awk '/HWaddr/ {print $5}')
MAC_MD5=$(echo -n $WIFIMAC | md5sum - | cut -c1-32)
ROOTFS_VER=$(cat /etc/config/rootfs_ver)
OVPN_CONFIG=$(cat /etc/openvpn/current_ovpn)

# update rootfs version

API_PATH=get-lastest-rootfs
WORK_FOLDER=/tmp

#cd $WORK_FOLDER; wget --quiet --output-document=rootfs_data.bin "$API_HOST/$API_PATH/$MAC_MD5/$ROOTFS_VER"; getfs=$( wc -c rootfs_data.bin  | awk '/ / {print $1}' )

#if [ $getfs -gt 500000 ] ;
#then
#     cd $WORK_FOLDER; mtd -r write rootfs_data.bin rootfs_data
#else
#     cd $WORK_FOLDER; rm rootfs_data.bin
#fi

cd $WORK_FOLDER; wget --quiet "$API_HOST/$API_PATH/$MAC_MD5/$ROOTFS_VER"
# validate image by hash
cd $WORK_FOLDER; ls -a *.bin && getfn=$( ls -a *.bin )
if [ -f $getfn ] ;
then
     gethash=$( md5sum $WORK_FOLDER/$getfn | cut -c1-32)
     if [ $gethash == ${getfn:0:32} ] ;
     then
          cd $WORK_FOLDER; mtd -r write $getfn rootfs_data
     else
          cd $WORK_FOLDER; rm $getfn
     fi
fi

# customizing device with SSID/PSK

MAC_SHORT=$( ifconfig eth0 | awk '/HWaddr/ {print $5}' |sed 's/://g' )
WIFI_SSID="DKHVPNAP-"${MAC_SHORT:8:12}
WIFI_PSK=$MAC_SHORT
WIFI_CFG=/etc/config/wireless

if [ $( cat $WIFI_CFG | grep DKHVPN-AP | awk '/DKHVPN-AP/ {print $3}' ) != "" ] ;
then
     sed "s/DKHVPN-AP/$WIFI_SSID/" $WIFI_CFG | sed "s/GodIsLove/$WIFI_PSK/" > /tmp/wireless.conf
     mv /tmp/wireless.conf /etc/config/wireless
     /etc/init.d/network restart
fi
