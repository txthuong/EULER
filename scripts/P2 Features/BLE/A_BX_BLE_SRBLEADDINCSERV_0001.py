# Test Name                                     Description
# A_BX_BLE_SRBLEADDINCSERV_0001                 Check syntax for AT+SRBLEADDINCSERV command
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
# A_BX_BLE_SRBLEADDINCSERV_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_BLE_SRBLEADDINCSERV_0001"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Check syntax for AT+SRBLEADDINCSERV command" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: Add a primary service\n"
    SagSendAT(uart_com, 'AT+SRBLEADDSERV=1234\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLEADDSERV: 50\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 2: Add another service\n"
    SagSendAT(uart_com, 'AT+SRBLEADDSERV=5678\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLEADDSERV: 150\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 3: Check +SRBLEADDINCSERV test command\n"
    SagSendAT(uart_com, 'AT+SRBLEADDINCSERV=?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 4: Check +SRBLEADDINCSERV execute command\n"
    SagSendAT(uart_com, 'AT+SRBLEADDINCSERV\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 5: Check +SRBLEADDINCSERV read command\n"
    SagSendAT(uart_com, 'AT+SRBLEADDINCSERV?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 6: Check +SRBLEADDINCSERV write command with valid parameters\n"
    SagSendAT(uart_com, 'AT+SRBLEADDINCSERV=50,150\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 7: Check +SRBLEADDINCSERV write command with invalid parameter\n"
    for i in ('a','%','!','#','/'):
        SagSendAT(uart_com, 'AT+SRBLEADDINCSERV=%s,150\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
        
    print "\nStep 8: Check +SRBLEADDINCSERV write command with invalid parameter\n"
    for i in ('a','%','@','#','/'):
        SagSendAT(uart_com, 'AT+SRBLEADDINCSERV=50,%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
     
    print "\nStep 9: Check +SRBLEADDINCSERV write command with missing parameters\n"
    SagSendAT(uart_com, 'AT+SRBLEADDINCSERV=\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)

    print "\nStep 10: Check +SRBLEADDINCSERV write command with missing parameter\n"
    SagSendAT(uart_com, 'AT+SRBLEADDINCSERV=50\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
     
    print "\nStep 11: Check +SRBLEADDINCSERV write command with extra parameter\n"
    SagSendAT(uart_com, 'AT+SRBLEADDINCSERV=50,150,250\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)
     
    print "\nStep 12: Check +SRBLEADDINCSERV write command with extra parameter\n"
    SagSendAT(uart_com, 'AT+SRBLEADDINCSERV=50,150,250,a\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)
    
    print "\nStep 13: Delete a primary service\n"
    SagSendAT(uart_com, 'AT+SRBLEDELSERV=50\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 14: Delete a primary service\n"
    SagSendAT(uart_com, 'AT+SRBLEDELSERV=150\r')
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

SagSendAT(uart_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)