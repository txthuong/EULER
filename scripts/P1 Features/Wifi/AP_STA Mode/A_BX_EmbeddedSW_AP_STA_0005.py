# Test Name                                     Description
# A_BX_EmbeddedSW_AP_STA_0005                   Use command +SRWAPCFG to configure SSID with various characters
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
# A_BX_EmbeddedSW_AP_STA_0005
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_AP_STA_0005"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s:Use command +SRWAPCFG to configure SSID with various characters" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: Query default Operating Mode of module\n"
    SagSendAT(uart_com, 'AT+SRWCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRWCFG: 0"\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 2: Configure Operating Mode of module as AP and STA concurrent mode\n"
    SagSendAT(uart_com, 'AT+SRWCFG=3\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 3: Query current Operating Mode of module \n"
    SagSendAT(uart_com, 'AT+SRWCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRWCFG: 3,0,"%s","%s"\r\n' %(dut_mac_address_sta, dut_mac_address)], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)

    # wifi_ssid has 40 characters
    wifi_ssid_str = 'abcdefghij0123456789abcdefghij0123456789'

    for i in range (1, len(wifi_ssid_str)):
        wifi_ssid = wifi_ssid_str[0:i]
        if i <= 32:
            print "\nStep 4: Setup Access Point with SSID has %s characters\n" % len(wifi_ssid)
            SagSendAT(uart_com, 'AT+SRWAPCFG="%s","%s",4,5,0,100\r' % (wifi_ssid, wifi_password))
            SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

            print "\nStep 5: Execute command to query current AP configurations\n"
            SagSendAT(uart_com, 'AT+SRWAPCFG?\r')
            SagWaitnMatchResp(uart_com, ['\r\n+SRWAPCFG: "%s","%s",4,5,0,100\r\n' % (wifi_ssid, wifi_password)],2000)
            SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
        else:
            print "\nStep 4: Setup Access Point with SSID has %s characters\n" % len(wifi_ssid)
            SagSendAT(uart_com, 'AT+SRWAPCFG="%s","%s",4,5,0,100\r' % (wifi_ssid, wifi_password))
            SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nTest Steps completed"
    
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

# Restore Wi-Fi mode to default
SagSendAT(uart_com, 'AT+SRWCFG=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)