# Test Name                                     Description
# A_BX_BLE_SRBLEADDCHARDESCR_0002               Check +SRBLEADDCHARDESCR with not existing <service_handle> and <characteristic handle>
# 
# Requirement
# 1 Euler module
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
    
    #Get bluetooth address
    SagSendAT(uart_com, 'AT+SRBTADDR?\r')
    res = SagWaitResp(uart_com, ['\r\n+SRBTADDR: "*"\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    dut_bluetooth_addr = res.split ('"')[1]
    print dut_bluetooth_addr
    
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
# A_BX_BLE_SRBLEADDCHARDESCRDESCR_0002
# -----------------------------------------------------------------------------------

test_ID = "A_BX_BLE_SRBLEADDCHARDESCRDESCR_0002"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Check +SRBLEADDCHARDESCR with not existing <service_handle> and <characteristic handle>" % test_ID
    print "*****************************************************************************************************************"

    print "\nStep 1: Add a characteristic descriptor into a not existing <service handle>\n"
    SagSendAT(uart_com, 'AT+SRBLEADDCHARDESCR=50, "2902", 17\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 2: Add a primary service\n"
    SagSendAT(uart_com, 'AT+SRBLEADDSERV=1234\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLEADDSERV: 50\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 3: Add a characteristic descriptor without adding a characteristic to a service\n"
    SagSendAT(uart_com, 'AT+SRBLEADDCHARDESCR=50, "2902", 17\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 4: Add a characteristic into the service\n"
    SagSendAT(uart_com, 'AT+SRBLEADDCHAR=50, "2A37", 10, 11\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLEADDCHAR: 52\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 5: Add a characteristic descriptor\n"
    SagSendAT(uart_com, 'AT+SRBLEADDCHARDESCR=50, "2902", 17\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLEADDCHARDESCR: 53\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 6: Delete the service\n"
    SagSendAT(uart_com, 'AT+SRBLEDELSERV=50\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 7: Try to add a characteristic descriptor again\n"
    SagSendAT(uart_com, 'AT+SRBLEADDCHARDESCR=50, "2902", 17\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

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

SagSendAT(uart_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)