# Test Name                                     Description
# A_BX_EmbeddedSW_AP_STA_0032                   Use command +SRWAPNETCFG to configure the start and end assigned IP address with Class A (Ex: 10.0.0.2 - 10.0.0.101). The IP address pool size should be 101
#
# Requirement
# 1 Euler module
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

except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_EmbeddedSW_AP_STA_0032
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_AP_STA_0032"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s:Use command +SRWAPNETCFG to configure the start and end assigned IP address with Class A (Ex: 10.0.0.2 - 10.0.0.101). The IP address pool size should be 101" % test_ID
    print "*****************************************************************************************************************"
    
    wifi_dhcp_gateway = '10.0.0.1'

    print "\nStep 1: Query default Operating Mode of module\n"
    SagSendAT(uart_com, 'AT+SRWCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRWCFG: 0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 2: Configure Operating Mode of module as AP and STA concurrent mode\n"
    SagSendAT(uart_com, 'AT+SRWCFG=3\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 3: Query current Operating Mode of module \n"
    SagSendAT(uart_com, 'AT+SRWCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRWCFG: 3,0,"%s","%s"\r\n' %(dut_mac_address_sta, dut_mac_address)], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 4: Enable DHCP with valid values\n"
    SagSendAT(uart_com, 'AT+SRWAPNETCFG=1,"%s","%s.2","%s.101",720\r' % (wifi_dhcp_gateway, return_subnet(wifi_dhcp_gateway), return_subnet(wifi_dhcp_gateway)))
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 5: Query network configuration\n"
    SagSendAT(uart_com, 'AT+SRWAPNETCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRWAPNETCFG: 1,"%s","%s.2","%s.101",720\r\n' % (wifi_dhcp_gateway, return_subnet(wifi_dhcp_gateway), return_subnet(wifi_dhcp_gateway))], 3000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 6: Re-configure DHCP with invalid values  (more than 100 IP address in DHCP IP pool)\n"
    SagSendAT(uart_com, 'AT+SRWAPNETCFG=1,"%s","%s.2","%s.103",720\r' % (wifi_dhcp_gateway, return_subnet(wifi_dhcp_gateway), return_subnet(wifi_dhcp_gateway)))
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 7: Query network configuration\n"
    SagSendAT(uart_com, 'AT+SRWAPNETCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRWAPNETCFG: 1,"%s","%s.2","%s.101",720\r\n' % (wifi_dhcp_gateway, return_subnet(wifi_dhcp_gateway), return_subnet(wifi_dhcp_gateway))], 3000)
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

# Restore NET configuration to default
SagSendAT(uart_com, 'AT+SRWAPNETCFG=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Restore Wi-Fi mode to default
SagSendAT(uart_com, 'AT+SRWCFG=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)