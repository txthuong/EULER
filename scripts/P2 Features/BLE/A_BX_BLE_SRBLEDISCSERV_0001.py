# Test Name                                     Description
# A_BX_BLE_SRBLEDISCSERV_0001                   Check syntax for AT+SRBLEDISCSERV command
# 
# Requirement
# 2 Euler modules
#    
# Author: ptnlam
#
# Jira ticket:
#-----------------------------------------------------------------------------------------------------

# -------------------------- DUT Initialization ----------------------------------
import string
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
# A_BX_BLE_SRBLEDISCSERV_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_BLE_SRBLEDISCSERV_0001"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Check syntax for AT+SRBLEDISCSERV command" % test_ID
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
    SagWaitnMatchResp(uart_com, ['*\r\n+SRBLE_IND: 1,1\r\n*'], 5000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBLEMTU: 1,23\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBLEMTU: 1,23\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBCSMART: 1,1,1\r\n'], 2000)
    
    print "\nStep 4: AUX: Notification form module 1\n"
    SagWaitnMatchResp(aux1_com, ['\r\n+SRBLECFG: 1,0,"%s",23\r\n' %dut_bluetooth_addr], 5000)
    SagWaitnMatchResp(aux1_com, ['*+SRBLE_IND: 1,1\r\n*'], 5000)
    SagWaitnMatchResp(aux1_com, ['+SRBLEMTU: 1,23\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['+SRBLEMTU: 1,23\r\n'], 2000)
    
    print "\nStep 5: DUT: Check +SRBLEDISCSERV test command\n"
    SagSendAT(uart_com, 'AT+SRBLEDISCSERV?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 6: DUT: Check +SRBLEDISCSERV execute command\n"
    SagSendAT(uart_com, 'AT+SRBLEDISCSERV\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 7: DUT: Check +SRBLEDISCSERV read command\n"
    SagSendAT(uart_com, 'AT+SRBLEDISCSERV?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 8: DUT: Check +SRBLEDISCSERV write command with valid parameter\n"
    SagSendAT(uart_com, 'AT+SRBLEDISCSERV=1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLEDISCSERV: 1,"1801",1,1,5\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBLEDISCSERV: 1,"1800",1,20,28\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBLEDISCSERV: 1,"bc2f4cc6-aaef-4351-9034-d66268e328f0",1,40,65535\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 9: DUT: Check +SRBLEDISCSERV write command\n"
    SagSendAT(uart_com, 'AT+SRBLEDISCSERV=1,"1800"\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLEDISCSERV: 1,"1800",1,20,28\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 10: DUT: Check +SRBLEDISCSERV write command with out range and not configured session\n"
    for i in ('-1','0','2','65'):
        SagSendAT(uart_com, 'AT+SRBLEDISCSERV=%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 910\r\n'], 2000)
    
    print "\nStep 11: DUT: Check +SRBLEDISCSERV write command with invalid session\n"
    for i in ('a','1F','*','/'):
        SagSendAT(uart_com, 'AT+SRBLEDISCSERV=%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 910\r\n'], 2000)

    print "\nStep 12: DUT: Check +SRBLEDISCSERV in the case missing parameter\n"
    SagSendAT(uart_com, 'AT+SRBLEDISCSERV=\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    
    print "\nStep 13: DUT: Check +SRBLEDISCSERV with extra parameter\n"
    SagSendAT(uart_com, 'AT+SRBLEDISCSERV=1,123145,2\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)
    
    print "\nStep 14: DUT: Check +SRBLEDISCSERV with extra parameter\n"
    SagSendAT(uart_com, 'AT+SRBLEDISCSERV=1,123488,2,a\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)

    print "\nStep 15: DUT: Clear bonded devices information\n"
    SagSendAT(uart_com, 'AT+SRBLESECCLEAR= "%s"\r' %aux1_bluetooth_addr)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLE_IND: 1,0,22\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLE_ERROR: 1\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['\r\n+SRBLE_IND: 1,0,19\r\n'], 2000)
    
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


# Close UART
SagClose(uart_com)
SagClose(aux1_com)