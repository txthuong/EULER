# Test Name                                     Description
# A_BX_BLE_SRBLE_0001                           Check syntax of +SRBLE command with valid values, invalid values and values out of range
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
    
    # Check BT name
    SagSendAT(uart_com, 'AT+SRBTNAME?\r')
    res = SagWaitResp(uart_com, ['\r\n+SRBTNAME: "*"\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    bt_name = res.split ('"')[1]
    print bt_name
    
    print "\nDUT: Enable subsystem\n"
    SagSendAT(uart_com, 'AT+SRBTSYSTEM=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_BLE_SRBLE_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_BLE_SRBLE_0001"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Check syntax of +SRBLE command with valid values, invalid values and values out of range" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: Check +SRBLE test command\n"
    SagSendAT(uart_com, 'AT+SRBLE=?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 2: Checking +SRBLE execute command\n"
    SagSendAT(uart_com, 'AT+SRBLE\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 3: Checking +SRBLE read command\n"
    SagSendAT(uart_com, 'AT+SRBLE?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLE: "%s",23,1,0\r\n' %bt_name], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 4: Checking +SRBLE write command\n"
    SagSendAT(uart_com, 'AT+SRBLE="myName", 50, 1,128\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 5: Query: AT+SRBLE?\n"
    SagSendAT(uart_com, 'AT+SRBLE?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLE: "myName",50,1,128\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 6: Disable BC Smart profile support\n"
    SagSendAT(uart_com, 'AT+SRBLE="Name",100, 0\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 7: Query: AT+SRBLE?\n"
    SagSendAT(uart_com, 'AT+SRBLE?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLE: "Name",100,0,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 8: Check write command with missing parameter\n"
    SagSendAT(uart_com, 'AT+SRBLE=\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)

    print "\nStep 9: Check write command with extra parameter\n"
    SagSendAT(uart_com, 'AT+SRBLE="myName", 50, 1,64,1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)
    
    print "\nStep 9: Check write command with invalid parameter\n"
    for i in ('a','*','#','@'):
        SagSendAT(uart_com, 'AT+SRBLE="myName", %s, 1,64\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nTest Steps completed\n"

except Exception, err_msg :
    VarGlobal.statOfItem = "NOK"
    print Exception, err_msg
    SagSendAT(uart_com, 'AT&F\r')
    SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 2000)
    SagSendAT(uart_com, 'AT&F\r')
    SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 2000)

#Print test result
PRINT_TEST_RESULT(test_ID, VarGlobal.statOfItem)

# -----------------------------------------------------------------------------------

print "\n----- Test Body End -----\n"

print "-----------Restore Settings---------------"

# Restore BT name to default
SagSendAT(uart_com, 'AT+SRBLE="%s",23,1,0\r' %bt_name)
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

SagSendAT(uart_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)