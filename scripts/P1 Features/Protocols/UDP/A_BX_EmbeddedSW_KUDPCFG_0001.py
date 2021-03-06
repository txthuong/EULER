# Test Name                                     Description
# A_BX_EmbeddedSW_KUDPCFG_0001                  To check syntax and input range for the AT command "+KUDPCFG", UDP Connection Configuration
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
# A_BX_EmbeddedSW_KUDPCFG_0001
# -----------------------------------------------------------------------------------
    
test_ID = "A_BX_EmbeddedSW_KUDPCFG_0001"
    
#######################################################################################
#   START
#######################################################################################
    
try:
    
    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")
    
    print "***************************************************************************************************************"
    print "%s:To check syntax and input range for the AT command +KUDPCFG, UDP Connection Configuration" % test_ID
    print "***************************************************************************************************************"
    
    print '\nStep 1: Check test command\n'
    SagSendAT(uart_com, 'AT+KUDPCFG=?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print '\nStep 2: Check read command\n'
    SagSendAT(uart_com, 'AT+KUDPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print '\nStep 3: Check execute command\n'
    SagSendAT(uart_com, 'AT+KUDPCFG\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print '\nStep 4: Check write command with <udp_port> = 1234\n'
    SagSendAT(uart_com, 'AT+KUDPCFG=,1,1234\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KUDPCFG: 1\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print '\nStep 5: Check write command with invalid mode = [2,-1] [a,*,%] \n'
    for i in (2,-1):
        SagSendAT(uart_com, 'AT+KUDPCFG=,%s,1234\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    for i in ('a','*','%'):
        SagSendAT(uart_com, 'AT+KUDPCFG=,%s,1234\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print '\nStep 6: Query UDP configured\n'
    SagSendAT(uart_com, 'AT+KUDPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KUDPCFG: 1,,1,1234,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print '\nStep 7: Check write command with invalid <udp_port> = [65536,-1] [a,*,%] \n'
    for i in (65536,-1):
        SagSendAT(uart_com, 'AT+KUDPCFG=,1,%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    for i in ('a','*','%'):
        SagSendAT(uart_com, 'AT+KUDPCFG=,1,%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print '\nStep 8: Query UDP configured\n'
    SagSendAT(uart_com, 'AT+KUDPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KUDPCFG: 1,,1,1234,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print '\nStep 9: Check write command with <data mode> = 0\n'
    SagSendAT(uart_com, 'AT+KUDPCFG=,1,2242,0\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KUDPCFG: 2\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print '\nStep 10: Check write command with invalid <data_mode> = [2,-1] [a,*,%] \n'
    for i in (2,-1):
        SagSendAT(uart_com, 'AT+KUDPCFG=,1,5678,%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    for i in ('a','*','%'):
        SagSendAT(uart_com, 'AT+KUDPCFG=,1,5678,%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print '\nStep 11: Close created session\n'
    SagSendAT(uart_com, 'AT+KUDPCLOSE=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(uart_com, 'AT+KUDPCLOSE=2\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print '\nStep 12: Delete UDP Connection after closing it\n'
    SagSendAT(uart_com, 'AT+KUDPDEL=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(uart_com, 'AT+KUDPDEL=2\r')
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
SagWaitnMatchResp(uart_com, ['+SRWSTASTATUS: 0,8\r\n'], 2000)

# Restore station connection information to default
SagSendAT(uart_com, 'AT+SRWSTACFG="","",1\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Restore Wi-Fi mode to default
SagSendAT(uart_com, 'AT+SRWCFG=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)