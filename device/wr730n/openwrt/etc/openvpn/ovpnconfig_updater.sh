#!/bin/bash

# waiting for wan/internet connected
IPADDR=$( ifconfig eth0 | awk '/inet addr/ {print $2}' | cut -c6- )
while [ $IPADDR == "" ]; do
    sleep 5
done

API_HOST="http://ap-ws.dkhvpn.com:8080/api/update"
WIFIMAC=$(ifconfig eth0 | awk '/HWaddr/ {print $5}')
MAC_MD5=$(echo -n $WIFIMAC | md5sum - | cut -c1-32)
OVPN_CONFIG=$(cat /etc/openvpn/current_ovpn)

triger=${1:-'connectivity'}

# update ovpn-config if having latest
case $triger in 
     # update ovpn-config if connectivity is bad
     'connectivity' )
     API_PATH=change-ovpn-config
     WORK_FOLDER=/etc/openvpn

     # if disconnected for 3 mins, change ovpn-config
     TLSERORRS=$(tail -180 /tmp/openvpn.log | grep 'TLS Error' | wc -l)
     if [ $TLSERORRS -gt 150 ] ;
     then
          cd $WORK_FOLDER; wget --quiet --output-document=ovpn.tar "$API_HOST/$API_PATH/$MAC_MD5/$OVPN_CONFIG/0"; getfs=$( wc -c ovpn.tar  | awk '/ / {print $1}' )
          if [ $getfs -gt 1000 ] ; 
          then
               cd $WORK_FOLDER; tar -xvf ovpn.tar; rm ovpn.tar
               /etc/init.d/openvpn restart
               sleep 5
               exit 0
          else
               cd $WORK_FOLDER; rm ovpn.tar
          fi
     fi

     # if ping VPN server failed for 7/10, change ovpn-config
     PING_SUCC=$( ping -c 10 10.8.0.1 | grep 'time=' | wc -l );echo $PING_SUCC
     if [ $PING_SUCC -lt 4 ] ;
     then
          cd $WORK_FOLDER; wget --quiet --output-document=ovpn.tar "$API_HOST/$API_PATH/$MAC_MD5/$OVPN_CONFIG/1"; getfs=$( wc -c ovpn.tar  | awk '/ / {print $1}' )
          if [ $getfs -gt 1000 ] ; 
          then
               cd $WORK_FOLDER; tar -xvf ovpn.tar; rm ovpn.tar
               /etc/init.d/openvpn restart
               sleep 5
               exit 0
          else
               cd $WORK_FOLDER; rm ovpn.tar
          fi
     fi
     ;;

     *)
          echo "please run this script with a parameter..."
     ;;
esac
