# Test Name                                     Description
# A_BX_EmbeddedSW_APmode_0005                   Use command +SRWAPNETCFG to configure IP address lease time. Verify module should release IP address after that lease time.
#
# Requirement
# 2 Euler modules
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
# A_BX_EmbeddedSW_APmode_0005
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_APmode_0005"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready":
        VarGlobal.statOfItem = "NOK"
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    wifi_ssid = 'euler_testing'
        
    print "*****************************************************************************************************************"
    print "%s: Use command +SRWAPNETCFG to configure IP address lease time. Verify module should release IP address after that lease time" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: Enable module A as Access Point mode\n"
    SagSendAT(uart_com, 'AT+SRWCFG=2\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 2: 'Setup Access Point mode\n"
    SagSendAT(uart_com, 'AT+SRWAPCFG="%s","%s",4,1,0,100\r' %(wifi_ssid,wifi_password))
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 3: Query current AP configurations\n"
    SagSendAT(uart_com, 'AT+SRWAPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRWAPCFG: "%s","%s",4,1,0,100\r\n' %(wifi_ssid,wifi_password)], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 4: Execute command to enable DHCP with valid values \n"
    SagSendAT(uart_com, 'AT+SRWAPNETCFG=1,"%s","%s.2","%s.2",1\r' %(wifi_dhcp_gateway, return_subnet(wifi_dhcp_gateway), return_subnet(wifi_dhcp_gateway)))
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 5: Execute command to query current DHCP setting\n"
    SagSendAT(uart_com, 'AT+SRWAPNETCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRWAPNETCFG: 1,"%s","%s.2","%s.2",1\r\n' %(wifi_dhcp_gateway, return_subnet(wifi_dhcp_gateway), return_subnet(wifi_dhcp_gateway))], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 6: Use another module to connect to this Access Point\n"
    SagSendAT(aux1_com, 'AT+SRWCFG=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(aux1_com, 'AT+SRWSTACFG="%s","%s",1\r' %(wifi_ssid,wifi_password))
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 7: Use AUX module to connect to this Access Point\n"
    SagSendAT(aux1_com, 'AT+SRWCFG=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(aux1_com, 'AT+SRWSTACON=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    if SagWaitnMatchResp(aux1_com, ['*\r\n+SRWSTASTATUS: 1,"%s","%s",*,*\r\n' % (wifi_ssid, dut_mac_address)], 20000):
        SagWaitnMatchResp(aux1_com, ['\r\n+SRWSTAIP: "%s.*","%s","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway)], 10000)
    else:
        raise Exception("---->Problem: Module cannot connect to Wi-Fi !!!")
    SagWaitnMatchResp(uart_com, ['\r\n+SRWAPSTA: 1,"%s"\r\n' % aux1_mac_address_sta], 2000)
    
    print "\nStep 8: Change DHCP settings \n"
    SagSendAT(uart_com, 'AT+SRWAPNETCFG=1,"10.0.0.1","10.0.0.2","10.0.0.101",1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    time.sleep(75)
    SagWaitnMatchResp(aux1_com, ['\r\n+SRWSTAIP: "10.0.0.*","%s","10.0.0.1"\r\n' %wifi_dhcp_subnet_mask], 2000)
    
    print "\nStep 9: Execute command to query current IP\n"
    SagSendAT(aux1_com, 'AT+SRWSTACON?\r')
    SagWaitnMatchResp(aux1_com, ['\r\n+SRWSTASTATUS: 1,"%s","%s",1,3\r\n' % (wifi_ssid, dut_mac_address)], 2000 )
    SagWaitnMatchResp(aux1_com, ['+SRWSTAIP: "10.0.0.*","%s","10.0.0.1"\r\n' % wifi_dhcp_subnet_mask], 2000)
    SagWaitnMatchResp(aux1_com, ['OK\r\n'], 2000)
    
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

#Disable DHCP
SagSendAT(uart_com, 'AT+SRWAPNETCFG=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

#Disconnect
SagSendAT(aux1_com, 'AT+SRWSTACFG="%s","%s",0\r' %(wifi_ssid,wifi_password))
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

SagSendAT(aux1_com, 'AT+SRWSTACON=0\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
SagWaitnMatchResp(aux1_com, ['\r\n+SRWSTASTATUS: 0,8\r\n'], 2000)
SagWaitnMatchResp(uart_com, ['\r\n+SRWAPSTA: 0,"%s"\r\n' % aux1_mac_address_sta], 2000 )

# Restore DUT
SagSendAT(uart_com, 'AT+SRWCFG=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

SagSendAT(aux1_com, 'AT+SRWCFG=0\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)
SagClose(aux1_com)
