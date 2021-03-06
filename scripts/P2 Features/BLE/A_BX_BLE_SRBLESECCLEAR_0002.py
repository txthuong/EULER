# Test Name                                     Description
# A_BX_BLE_SRBLESECCLEAR_0002                   Check syntax of +SRBLESECCLEAR command with invalid values
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
    
    # AUX1 Initialization
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
    
    #Get bluetooth address
    SagSendAT(uart_com, 'AT+SRBTADDR?\r')
    res = SagWaitResp(uart_com, ['\r\n+SRBTADDR: "*"\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    dut_bluetooth_addr = res.split ('"')[1]
    print dut_bluetooth_addr
    
    SagSendAT(aux1_com, 'AT+SRBTADDR?\r')
    res = SagWaitResp(aux1_com, ['\r\n+SRBTADDR: "*"\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['OK\r\n'], 2000)
    aux1_bluetooth_addr = res.split ('"')[1]
    print aux1_bluetooth_addr
    
    print "\nAUX: Enable subsystem\n"
    SagSendAT(aux1_com, 'AT+SRBTSYSTEM=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
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
# A_BX_BLE_SRBLESECCLEAR_0002
# -----------------------------------------------------------------------------------

test_ID = "A_BX_BLE_SRBLESECCLEAR_0002"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Check syntax of +SRBLESECCLEAR command with invalid values" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: AUX: Start advertising\n"
    SagSendAT(aux1_com, 'AT+SRBLEADV=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 2: DUT: Module 1 connects to Module 2 (advertising)\n"
    SagSendAT(uart_com, 'AT+SRBLECFG=%s\r' %aux1_bluetooth_addr)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLECFG: 1,0,"%s",23\r\n' %aux1_bluetooth_addr], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 3: DUT: Initiate connection to device B\n"
    SagSendAT(uart_com, 'AT+SRBLECNX=1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLE_IND: 1,1\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBLEMTU: 1,23\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBLEMTU: 1,23\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBCSMART: 1,1,1\r\n'], 2000)
    
    print "\nStep 4: AUX: Notification form module 1\n"
    SagWaitnMatchResp(aux1_com, ['\r\n+SRBLECFG: 1,0,"%s",23\r\n' %dut_bluetooth_addr], 2000)
    SagWaitnMatchResp(aux1_com, ['+SRBLE_IND: 1,1\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['+SRBLEMTU: 1,23\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['+SRBLEMTU: 1,23\r\n'], 2000)
    
    print "\nStep 5: DUT: Set the IO capability and the authorization request type\n"
    SagSendAT(uart_com, 'AT+SRBLESECPARAMS=3,4\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 6: AUX: Set the IO capability and the authorization request type\n"
    SagSendAT(aux1_com, 'AT+SRBLESECPARAMS=3,4\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 7: Send out the secure bonding request\n"
    SagSendAT(uart_com, 'AT+SRBLESECBOND=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 8: AUX1: Receive the secure bonding request\n"
    SagWaitnMatchResp(aux1_com, ['+SRBLESECBONDREQ: 1\r\n'], 5000)

    print "\nStep 9: AUX1: Accept the bonding request\n"
    SagSendAT(aux1_com, 'AT+SRBLESECBOND=1,1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 10: Bonding success\n"
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLESECBOND: 1,1\r\n'], 3000)
    SagWaitnMatchResp(aux1_com, ['\r\n+SRBLESECBOND: 1,1\r\n'], 3000)
    
    print "\nStep 11: Checking SRBLESECCLEAR write command with missing parameter\n"
    SagSendAT(uart_com, 'AT+SRBLESECCLEAR=\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    
    print "\nStep 12: Checking SRBLESECCLEAR write command with extra parameter\n"
    SagSendAT(uart_com, 'AT+SRBLESECCLEAR=%s,1\r' %aux1_bluetooth_addr)
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)
    
    print "\nStep 13: Checking SRBLESECCLEAR write command with extra parameter\n"
    SagSendAT(uart_com, 'AT+SRBLESECCLEAR=%s,1,1\r' %aux1_bluetooth_addr)
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)
    
    print "\nStep 14: Checking SRBLESECCLEAR write command with invalid parameter\n"
    for i in ('-11:22:-33:AA:BB:CC', 'GG:HH:11:22:FF:33', 'FF:FF:FF::FF:FF', '11:22:33:44:55:666', '11:22:#:44:55:66', 'AA:BB:CC', 'GG:HH:11:22:FF:33:44'):
        SagSendAT(uart_com, 'AT+SRBLESECCLEAR=%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 15: Checking SRBLESECCLEAR execute command\n"
    SagSendAT(uart_com, 'AT+SRBLESECCLEAR\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 16: AUX1: Stop advertising\n"
    SagSendAT(aux1_com, 'AT+SRBLEADV=0\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 17: Delete the BLE configure\n"
    SagSendAT(uart_com, 'AT+SRBLEDEL=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    SagSendAT(aux1_com, 'AT+SRBLEDEL=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 3000)

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

SagSendAT(uart_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

SagSendAT(aux1_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)
SagClose(aux1_com)