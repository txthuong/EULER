# Test Name                                     Description
# A_BX_EmbeddedSW_KTCP_DATA_0010                To check TCP data shall be sent and received correctly in server and client with <data mode>=0 when there are multi-client sessions
#
# Requirement
#   2 Euler modules
#
# Author: ptnlam
#
# Jira ticket:
#-----------------------------------------------------------------------------------------------------

# -------------------------- DUT Initialization ----------------------------------

test_environment_ready = "Ready"

try:

    print "\n------------Test Environment check: Begin------------"
    # UART Initialization
    print "\nOpen AT Command port"
    uart_com = SagOpen(uart_com, 115200, 8, "N", 1, "None")
    
    # Display DUT information
    print "\nDisplay DUT information"
    print "\nGet model information"
    SagSendAT(uart_com, 'AT+FMM\r')
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)
    
    print "\nGet serial number"
    SagSendAT(uart_com, 'AT+CGSN\r')
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)
    
    print "\nGet revision information"
    SagSendAT(uart_com, 'ATI3\r')
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)
    
    # DUT Initialization
    print "\nInitiate DUT"
    SagSendAT(uart_com, 'AT\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    # AUX1_UART Initialization
    print "\nOpen AT Command port"
    aux1_com = SagOpen(aux1_com, 115200, 8, "N", 1, "None")
    
    # Display AUX1 information
    print "\nDisplay AUX1 information"
    print "\nGet model information"
    SagSendAT(aux1_com, 'AT+FMM\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)
    
    print "\nGet serial number"
    SagSendAT(aux1_com, 'AT+CGSN\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)
    
    print "\nGet revision information"
    SagSendAT(aux1_com, 'ATI3\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)
    
    # AUX1 Initialization
    print "\nInitiate AUX1"
    SagSendAT(aux1_com, 'AT\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"
    
print "\n------------Test Environment check: End------------"
    
print "\n----- Test Body Start -----\n"
    
# -----------------------------------------------------------------------------------
# A_BX_EmbeddedSW_KTCP_DATA_0010
# -----------------------------------------------------------------------------------
    
test_ID = "A_BX_EmbeddedSW_KTCP_DATA_0010"

#######################################################################################
#   START
#######################################################################################
    
try:
    
    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")
    
    print "***************************************************************************************************************"
    print "%s:To check TCP data shall be sent and received correctly in server and client with <data mode>=0 when there are multi-client sessions" % test_ID
    print "***************************************************************************************************************"
    
    print '\nStep 1: Configure modules work as Station mode\n'
    SagSendAT(uart_com, 'AT+SRWCFG=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    SagSendAT(aux1_com, 'AT+SRWCFG=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
    print '\nStep 2: Connect to the Wi-Fi network\n'
    SagSendAT(uart_com, 'AT+SRWSTACFG="%s","%s"\r' %(wifi_ssid, wifi_password))
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    SagSendAT(aux1_com, 'AT+SRWSTACFG="%s","%s"\r' %(wifi_ssid, wifi_password))
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
    print '\nStep 3: Activate Station connection\n'
    SagSendAT(uart_com, 'AT+SRWSTACON=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    if SagWaitnMatchResp(uart_com, ['*\r\n+SRWSTASTATUS: 1,"%s","%s",*,*\r\n' % (wifi_ssid, wifi_mac_addr)], 20000):
        response1 = SagWaitResp(uart_com, ['\r\n+SRWSTAIP: "%s.*","%s","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway)], 10000)
    else:
        raise Exception("---->Problem: Module cannot connect to Wi-Fi !!!")
        
    SagMatchResp(response1, ['\r\n+SRWSTAIP: "%s.*","%s","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway)])
    uart_tcp_ip=response1.split('"')[1]
    
    SagSendAT(aux1_com, 'AT+SRWSTACON=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    if SagWaitnMatchResp(aux1_com, ['*\r\n+SRWSTASTATUS: 1,"%s","%s",*,*\r\n' % (wifi_ssid, wifi_mac_addr)], 20000):
        response2 = SagWaitResp(aux1_com, ['\r\n+SRWSTAIP: "%s.*","%s","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway)], 10000)
    else:
        raise Exception("---->Problem: Module cannot connect to Wi-Fi !!!")
        
    SagMatchResp(response2, ['\r\n+SRWSTAIP: "%s.*","%s","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway)])
    aux1_tcp_ip=response2.split('"')[1]
    
    print '\nStep 4: DUT: TCP Connection Configuration\n'
    SagSendAT(uart_com, 'AT+KTCPCFG=,1,,1234\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KTCPCFG: 1\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print '\nStep 5: DUT: Start TCP Connection\n'
    SagSendAT(uart_com, 'AT+KTCPCNX=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print '\nStep 6: DUT: Display IP Address of the current connection\n'
    SagSendAT(uart_com, 'AT+SRWSTACON?\r')
    if SagWaitnMatchResp(uart_com, ['*\r\n+SRWSTASTATUS: 1,"%s","%s",*,*\r\n' % (wifi_ssid, wifi_mac_addr)], 20000):
        SagWaitnMatchResp(uart_com, ['\r\n+SRWSTAIP: "%s.*","%s","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway)], 10000)
    else:
        raise Exception("---->Problem: Module cannot connect to Wi-Fi !!!")
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print '\nStep 7: AUX: TCP Client 1 Connection Configuration\n'
    SagSendAT(aux1_com, 'AT+KTCPCFG=,0,"%s",1234,5678\r' %uart_tcp_ip)
    SagWaitnMatchResp(aux1_com, ['\r\n+KTCPCFG: 1\r\n'], 3000)
    SagWaitnMatchResp(aux1_com, ['OK\r\n'], 3000)
    
    print '\nStep 8: AUX: Start TCP Connection\n'
    SagSendAT(aux1_com, 'AT+KTCPCNX=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+KTCP_SRVREQ: 1,*,"%s",*\r\n' %aux1_tcp_ip], 2000)
    
    print '\nStep 9: AUX: Display IP Address of the current connection\n'
    SagSendAT(aux1_com, 'AT+SRWSTACON?\r')
    if SagWaitnMatchResp(aux1_com, ['*\r\n+SRWSTASTATUS: 1,"%s","%s",*,*\r\n' % (wifi_ssid, wifi_mac_addr)], 20000):
        SagWaitnMatchResp(aux1_com, ['\r\n+SRWSTAIP: "%s.*","%s","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway)], 10000)
    else:
        raise Exception("---->Problem: Module cannot connect to Wi-Fi !!!")
    SagWaitnMatchResp(aux1_com, ['OK\r\n'], 2000)
    
    print '\nStep 10: AUX: TCP Client 2 Connection Configuration\n'
    SagSendAT(aux1_com, 'AT+KTCPCFG=,0,"%s",1234,5679\r' %uart_tcp_ip)
    SagWaitnMatchResp(aux1_com, ['\r\n+KTCPCFG: 2\r\n'], 3000)
    SagWaitnMatchResp(aux1_com, ['OK\r\n'], 3000)
    
    print '\nStep 11: AUX: Start TCP Connection\n'
    SagSendAT(aux1_com, 'AT+KTCPCNX=2\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+KTCP_SRVREQ: 1,*,"%s",*\r\n' %aux1_tcp_ip], 2000)
    
    print '\nStep 12: AUX: TCP Client 3 Connection Configuration\n'
    SagSendAT(aux1_com, 'AT+KTCPCFG=,0,"%s",1234,5680\r' %uart_tcp_ip)
    SagWaitnMatchResp(aux1_com, ['\r\n+KTCPCFG: 3\r\n'], 3000)
    SagWaitnMatchResp(aux1_com, ['OK\r\n'], 3000)
    
    print '\nStep 13: AUX: Start TCP Connection\n'
    SagSendAT(aux1_com, 'AT+KTCPCNX=3\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+KTCP_SRVREQ: 1,*,"%s",*\r\n' %aux1_tcp_ip], 2000)
    
    print '\nStep 14: AUX: TCP Client 4 Connection Configuration\n'
    SagSendAT(aux1_com, 'AT+KTCPCFG=,0,"%s",1234,5681\r' %uart_tcp_ip)
    SagWaitnMatchResp(aux1_com, ['\r\n+KTCPCFG: 4\r\n'], 3000)
    SagWaitnMatchResp(aux1_com, ['OK\r\n'], 3000)
    
    print '\nStep 15: AUX: Start TCP Connection\n'
    SagSendAT(aux1_com, 'AT+KTCPCNX=4\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+KTCP_SRVREQ: 1,*,"%s",*\r\n' %aux1_tcp_ip], 2000)
    
    print '\nStep 16: AUX Send data to SERVER\n'
    SagSendAT(aux1_com, 'AT+KTCPSND=1,"From A_BX_EmbeddedSW_KTCP_DATA_0010 Client 1"\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+KTCP_DATA: 2,44,From A_BX_EmbeddedSW_KTCP_DATA_0010 Client 1\r\n'], 2000)
    
    SagSendAT(aux1_com, 'AT+KTCPSND=2,"From A_BX_EmbeddedSW_KTCP_DATA_0010 Client 2"\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+KTCP_DATA: 3,44,From A_BX_EmbeddedSW_KTCP_DATA_0010 Client 2\r\n'], 2000)
    
    SagSendAT(aux1_com, 'AT+KTCPSND=3,"From A_BX_EmbeddedSW_KTCP_DATA_0010 Client 3"\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+KTCP_DATA: 4,44,From A_BX_EmbeddedSW_KTCP_DATA_0010 Client 3\r\n'], 2000)
    
    SagSendAT(aux1_com, 'AT+KTCPSND=4,"From A_BX_EmbeddedSW_KTCP_DATA_0010 Client 4"\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+KTCP_DATA: 5,44,From A_BX_EmbeddedSW_KTCP_DATA_0010 Client 4\r\n'], 2000)
    
    print '\nStep 17: AUX: Close created session\n'
    SagSendAT(aux1_com, 'AT+KTCPCLOSE=1,1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+KTCP_NOTIF: 2,4\r\n'], 2000)
    
    SagSendAT(aux1_com, 'AT+KTCPCLOSE=2,1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+KTCP_NOTIF: 3,4\r\n'], 2000)
    
    SagSendAT(aux1_com, 'AT+KTCPCLOSE=3,1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+KTCP_NOTIF: 4,4\r\n'], 2000)
    
    SagSendAT(aux1_com, 'AT+KTCPCLOSE=4,1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+KTCP_NOTIF: 5,4\r\n'], 2000)
    
    print '\nStep 18: DUT: Close created session\n'
    SagSendAT(uart_com, 'AT+KTCPCLOSE=1,0\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print '\nStep 19: DUT: Delete TCP Connection after closing it\n'
    SagSendAT(uart_com, 'AT+KTCPDEL=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(uart_com, 'AT+KTCPDEL=2\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(uart_com, 'AT+KTCPDEL=3\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(uart_com, 'AT+KTCPDEL=4\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(uart_com, 'AT+KTCPDEL=5\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print '\nStep 20: AUX: Delete TCP Connection after closing it\n'
    SagSendAT(aux1_com, 'AT+KTCPDEL=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(aux1_com, 'AT+KTCPDEL=2\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(aux1_com, 'AT+KTCPDEL=3\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(aux1_com, 'AT+KTCPDEL=4\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

    print "\nTest Steps completed\n"
except Exception, err_msg :
    VarGlobal.statOfItem = "NOK"
    print Exception, err_msg
    SagSendAT(uart_com, 'AT&F\r')
    SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 2000)
    SagSendAT(aux1_com, 'AT&F\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nREADY\r\n'], 2000)

#Print test result
PRINT_TEST_RESULT(test_ID, VarGlobal.statOfItem)

# -----------------------------------------------------------------------------------

print "\n----- Test Body End -----\n"

print "-----------Restore Settings---------------"

# Disconnect to configured Access Point
SagSendAT(uart_com, 'AT+SRWSTACON=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
SagWaitnMatchResp(uart_com, ['\r\n+SRWSTASTATUS: 0,8\r\n'], 2000)

SagSendAT(aux1_com, 'AT+SRWSTACON=0\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
SagWaitnMatchResp(aux1_com, ['\r\n+SRWSTASTATUS: 0,8\r\n'], 2000)

# Restore station connection information to default
SagSendAT(uart_com, 'AT+SRWSTACFG="","",1\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

SagSendAT(aux1_com, 'AT+SRWSTACFG="","",1\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

# Restore Wi-Fi mode to default
SagSendAT(uart_com, 'AT+SRWCFG=3\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

SagSendAT(aux1_com, 'AT+SRWCFG=3\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)
SagClose(aux1_com)