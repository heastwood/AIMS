netsh advfirewall firewall add rule name="Neopost_IMOS_AIMS_Ports" dir=in action=allow protocol=TCP localport=2002-2007
netsh advfirewall firewall add rule name="Neopost_IMOS_AIMS_Ports" dir=out action=allow protocol=TCP remoteport=2002-2007
netsh advfirewall firewall add rule name="Neopost_IMOS_Integrate_Ports" dir=in action=allow protocol=TCP localport=10102
netsh advfirewall firewall add rule name="Neopost_AIMS_Front_End" dir=in action=allow protocol=TCP localport=80,443
netsh advfirewall firewall add rule name="Neopost_AIMS_Front_End" dir=out action=allow protocol=TCP remoteport=80,443
netsh advfirewall firewall add rule name="Neopost_DEP" dir=in action=allow protocol=TCP localport=13008
netsh advfirewall firewall add rule name="Neopost_DEP" dir=out action=allow protocol=TCP remoteport=13008
netsh advfirewall firewall add rule name="Neopost_File_Transfer" dir=in action=allow protocol=TCP localport=445
netsh advfirewall firewall add rule name="Neopost_File_Transfer" dir=out action=allow protocol=TCP remoteport=445
netsh advfirewall firewall add rule name="Neopost_DNS_UDP" dir=in action=allow protocol=UDP localport=53
netsh advfirewall firewall add rule name="Neopost_DNS_UDP" dir=out action=allow protocol=UDP remoteport=53
netsh advfirewall firewall add rule name="Neopost_DNS_TCP" dir=in action=allow protocol=TCP localport=53
netsh advfirewall firewall add rule name="Neopost_DNS_TCP" dir=out action=allow protocol=TCP remoteport=53
netsh advfirewall firewall add rule name="Neopost_ICMP_V4_Ping_Echo_Request" protocol=icmpv4:8,any dir=in action=allow
netsh advfirewall firewall add rule name="Neopost_ICMP_V4_Ping_Echo_Request" protocol=icmpv4:8,any dir=out action=allow
netsh advfirewall firewall add rule name="Neopost_Remote_Desktop_UDP" dir=in action=allow protocol=UDP localport=3389
netsh advfirewall firewall add rule name="Neopost_Remote_Desktop_UDP" dir=out action=allow protocol=UDP remoteport=3389
netsh advfirewall firewall add rule name="Neopost_Remote_Desktop_TCP" dir=in action=allow protocol=TCP localport=3389
netsh advfirewall firewall add rule name="Neopost_Remote_Desktop_TCP" dir=out action=allow protocol=TCP remoteport=3389
netsh advfirewall firewall add rule name="ICMP Allow incoming V4 echo request" protocol=icmpv4:8,any dir=in action=allow
netsh advfirewall firewall add rule name="ICMP Allow incoming V4 echo request" protocol=icmpv4:8,any dir=out action=allow