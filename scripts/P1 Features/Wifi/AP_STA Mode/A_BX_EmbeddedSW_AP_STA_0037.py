# Test Name                                     Description
# A_BX_EmbeddedSW_AP_STA_0037                   Use command +SRWSTACFG and +SRWSTACON to configure connection to another BX module that play a role as AP
#
# Requirement
# 1 Euler module  
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
    
except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_EmbeddedSW_AP_STA_0037
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_AP_STA_0037"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")
    
    print "*****************************************************************************************************************"
    print "%s:Use command +SRWSTACFG and +SRWSTACON to configure connection to another BX module that play a role as AP" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: Query default Operating Mode of module A\n"
    SagSendAT(uart_com, 'AT+SRWCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRWCFG: 0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 2: Configure Operating Mode of module A as AP and STA concurrent mode\n"
    SagSendAT(uart_com, 'AT+SRWCFG=3\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 3: Query default Operating Mode of module A\n"
    SagSendAT(uart_com, 'AT+SRWCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRWCFG: 3,0,"%s","%s"\r\n' %(dut_mac_address_sta, dut_mac_address)], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 4: 'Configure module A connection\n"
    SagSendAT(uart_com, 'AT+SRWSTACFG="%s","%s"\r' %(wifi_ssid, wifi_password))
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 5: Query current station configuration\n"
    SagSendAT(uart_com, 'AT+SRWSTACFG?\r' )
    SagWaitnMatchResp(uart_com, ['\r\n+SRWSTACFG: "%s","%s",0\r\n' %(wifi_ssid, wifi_password)], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 6: Connect to the access point from module B\n"
    SagSendAT(uart_com, 'AT+SRWSTACON=1\r' )
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['*+SRWSTASTATUS: 1,"%s","%s",*,3\r\n' %(wifi_ssid, wifi_mac_addr)], 20000)
    SagWaitnMatchResp(uart_com, ['+SRWSTAIP: "%s.*","%s","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway)], 3000)
    
    print "\nStep 7: Check details of the current connection\n"
    SagSendAT(uart_com, 'AT+SRWSTACON?\r' )
    SagWaitnMatchResp(uart_com, ['\r\n+SRWSTASTATUS: 1,"%s","%s",*,3\r\n' %(wifi_ssid, wifi_mac_addr)], 2000)
    SagWaitnMatchResp(uart_com, ['+SRWSTAIP: "%s.*","%s","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway)], 3000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nTest Steps completed\n"
    
except Exception, err_msg :
    VarGlobal.statOfItem = "NOK"
    print Exception, err_msg
    SagSendAT(uart_com, 'AT&F\r') 
    SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 2000)

#Print test result
PRINT_TEST_RESULT(test_ID, VarGlobal.statOfItem)

# -----------------------------------------------------------------------------------

print "\n----- Test Body End -----\n"

print "-----------Restore Settings---------------"

# Disconnect to configured Access Point
SagSendAT(uart_com, 'AT+SRWSTACON=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
SagWaitnMatchResp(uart_com, ['\r\n+SRWSTASTATUS: 0,8\r\n'], 2000)

# Restore station connection information to default
SagSendAT(uart_com, 'AT+SRWSTACFG="","",1\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Restore Wi-Fi mode to default
SagSendAT(uart_com, 'AT+SRWCFG=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)
