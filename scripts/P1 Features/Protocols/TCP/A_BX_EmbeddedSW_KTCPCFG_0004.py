# Test Name                                     Description
# A_BX_EmbeddedSW_KTCPCFG_0004                  To set <URC-ENDTCP-enable> =1: Display <data> in URC
#
# Requirement
#   1 Euler module
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
    
    # Display DUT Information
    print "\nDisplay DUT information"
    print "\nGet model information"
    SagSendAT(uart_com, 'AT+FMM\r')
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)
    
    print "\nGet serial number"
    SagSendAT(uart_com, 'AT+CGSN\r')
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)
    
    print "\nGet revision information"
    SagSendAT(uart_com, 'ATI3\r')
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'] , 2000)
    
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
# A_BX_EmbeddedSW_KTCPCFG_0004
# -----------------------------------------------------------------------------------
    
test_ID = "A_BX_EmbeddedSW_KTCPCFG_0004"
    
#######################################################################################
#   START
#######################################################################################
    
try:
    
    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")
    
    print "***************************************************************************************************************"
    print "%s:To set <URC-ENDTCP-enable> =1: Display <data> in URC" % test_ID
    print "***************************************************************************************************************"
    
    print '\nStep 1: Configure modules work as Station mode\n'
    SagSendAT(uart_com, 'AT+SRWCFG=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print '\nStep 2: Connect to the Wi-Fi network\n'
    SagSendAT(uart_com, 'AT+SRWSTACFG="%s","%s"\r' %(wifi_ssid, wifi_password))
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print '\nStep 3: Activate Station connection\n'
    SagSendAT(uart_com, 'AT+SRWSTACON=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    if SagWaitnMatchResp(uart_com, ['*\r\n+SRWSTASTATUS: 1,"%s","%s",*,*\r\n' % (wifi_ssid, wifi_mac_addr)], 20000):
        SagWaitnMatchResp(uart_com, ['\r\n+SRWSTAIP: "%s.*","%s","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway)], 10000)
    else:
        raise Exception("---->Problem: Module cannot connect to Wi-Fi !!!")
    
    print '\nStep 4: TCP Configure without <URC-ENDTCP-enable> =1\n'
    SagSendAT(uart_com, 'AT+KTCPCFG=,0,"server",1111,1,1,1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KTCPCFG: 1\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print '\nStep 5: Checking +KTCPCFG\n'
    SagSendAT(uart_com, 'AT+KTCPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KTCPCFG: 1,0,,0,"server",1111,1,1,1\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print '\nStep 6: TCP Configure with <URC-ENDTCP-enable>=1\n'
    SagSendAT(uart_com, 'AT+KTCPCFG=,0,"server",2222,1,1,1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KTCPCFG: 2\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print '\nStep 7: Checking +KTCPCFG\n'
    SagSendAT(uart_com, 'AT+KTCPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KTCPCFG: 1,0,,0,"server",1111,1,1,1\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+KTCPCFG: 2,0,,0,"server",2222,1,1,1\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print '\nStep 8: TCP Configure with <URC-ENDTCP-enable>=1\n'
    SagSendAT(uart_com, 'AT+KTCPCFG=,0,"server",3333,1,1,1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KTCPCFG: 3\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print '\nStep 9: Checking +KTCPCFG\n'
    SagSendAT(uart_com, 'AT+KTCPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KTCPCFG: 1,0,,0,"server",1111,1,1,1\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+KTCPCFG: 2,0,,0,"server",2222,1,1,1\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+KTCPCFG: 3,0,,0,"server",3333,1,1,1\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print '\nStep 10: Delete the TCP configuration\n'
    SagSendAT(uart_com, 'AT+KTCPDEL=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    SagSendAT(uart_com, 'AT+KTCPDEL=2\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    SagSendAT(uart_com, 'AT+KTCPDEL=3\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print '\nStep 9: Checking +KTCPCFG\n'
    SagSendAT(uart_com, 'AT+KTCPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

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
SagSendAT(uart_com, 'AT+SRWCFG=3\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)
