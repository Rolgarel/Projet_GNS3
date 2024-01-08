!
!
!
!
!
!
!
! Last configuration change at 00:00:00 UTC Mon Jan 01 2024
!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
!
hostname R24
!
boot-start-marker
boot-end-marker
!
!
!
no aaa new-model
no ip icmp rate-limit unreachable
ip cef
!
!
!
!
!
!
no ip domain lookup
ipv6 unicast-routing
ipv6 cef
!
!
multilink bundle-name authenticated
!
!
!
!
!
!
!
!
!
ip tcp synwait-time 5
!
!
!
!
!
!
!
!
!
!
!
!
interface Loopback0
 no ip address
 negotiation auto
 ipv6 enable
 ipv6 address 2001:100:102:44::1/64
 ipv6 ospf 13 area 0
!
interface FastEthernet0/0
 no ip address
 shutdown
 duplex full
!
interface GigabitEthernet 1/0
 no ip address
 negotiation auto
 ipv6 enable
 ipv6 address 2001:100:102:42::4/64
 ipv6 ospf 13 area 0
!
interface GigabitEthernet 2/0
 no ip address
 negotiation auto
 ipv6 enable
 ipv6 address 2001:100:102:64::4/64
 ipv6 ospf 13 area 0
!
interface GigabitEthernet 3/0
 no ip address
 negotiation auto
 ipv6 enable
 ipv6 address 2001:100:102:43::4/64
 ipv6 ospf 13 area 0
!
interface GigabitEthernet 4/0
 no ip address
 negotiation auto
 ipv6 enable
 ipv6 address 2001:100:102:41::4/64
 ipv6 ospf 13 area 0
!
router bgp 222
 bgp router-id 2.2.2.24
 bgp log-neighbor-changes
 no bgp default ipv4-unicast
 neighbor 2001:100:102:77::1 remote-as 222
 neighbor 2001:100:102:77::1 update-source Loopback0
 neighbor 2001:100:102:11::1 remote-as 222
 neighbor 2001:100:102:11::1 update-source Loopback0
 neighbor 2001:100:102:22::1 remote-as 222
 neighbor 2001:100:102:22::1 update-source Loopback0
 neighbor 2001:100:102:33::1 remote-as 222
 neighbor 2001:100:102:33::1 update-source Loopback0
 neighbor 2001:100:102:55::1 remote-as 222
 neighbor 2001:100:102:55::1 update-source Loopback0
 neighbor 2001:100:102:66::1 remote-as 222
 neighbor 2001:100:102:66::1 update-source Loopback0
 !
 address-family ipv4
 exit-address-family
 !
 address-family ipv4
  network 2001:100:102:44::1/64
  neighbor 2001:100:102:77::1 activate
  neighbor 2001:100:102:11::1 activate
  neighbor 2001:100:102:22::1 activate
  neighbor 2001:100:102:33::1 activate
  neighbor 2001:100:102:55::1 activate
  neighbor 2001:100:102:66::1 activate
 exit-address-family
!
ip forward-protocol nd
!
!
no ip http server
no ip http secure-server
!
ipv6 router ospf 13
 router-id 2.2.2.24
!
!
!
!
control-plane
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line vty 0 4
 login
!
!
end