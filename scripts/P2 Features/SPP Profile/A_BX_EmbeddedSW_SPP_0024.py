# Test Name                                     Description
# A_BX_EmbeddedSW_SPP_0024                      Verify module can establish concurrent two SPP connections to other devices
# 
# Requirement
# 3 Euler modules
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
    
    # AUX2_UART Initialization
    print "\nOpen AT Command port"
    aux2_com = SagOpen(aux2_com, 115200, 8, "N", 1, "None")

    # Display AUX1 information
    print "\nDisplay AUX1 information"
    print "\nGet model information"
    SagSendAT(aux2_com, 'AT+FMM\r')
    SagWaitnMatchResp(aux2_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet serial number"
    SagSendAT(aux2_com, 'AT+CGSN\r')
    SagWaitnMatchResp(aux2_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet revision information"
    SagSendAT(aux2_com, 'ATI3\r')
    SagWaitnMatchResp(aux2_com, ['*\r\nOK\r\n'], 2000)

    # AUX1 Initialization
    print "\nInitiate AUX1"
    SagSendAT(aux2_com, 'AT\r')
    SagWaitnMatchResp(aux2_com, ['\r\nOK\r\n'], 2000)
    
    print "\nAUX: Enable subsystem\n"
    SagSendAT(aux1_com, 'AT+SRBTSYSTEM=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
    print "\nDUT: Enable subsystem\n"
    SagSendAT(uart_com, 'AT+SRBTSYSTEM=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nAUX2: Enable subsystem\n"
    SagSendAT(aux2_com, 'AT+SRBTSYSTEM=1\r')
    SagWaitnMatchResp(aux2_com, ['\r\nOK\r\n'], 2000)

except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_EmbeddedSW_SPP_0024
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_SPP_0024"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s:  Verify module can establish concurrent two SPP connections to other devices" % test_ID
    print "*****************************************************************************************************************"

    print "\nStep 1: AUX1: Query Bluetooth address\n"
    SagSendAT(aux1_com, 'AT+SRBTADDR?\r')
    SagWaitnMatchResp(aux1_com, ['\r\n+SRBTADDR: "%s"\r\n' %aux1_bluetooth_address], 2000)
    SagWaitnMatchResp(aux1_com, ['OK\r\n'], 2000)
    
    print "\nStep 2: AUX1: Change Bluetooth state\n"
    SagSendAT(aux1_com, 'AT+SRBTSTATE=1,2\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 3: AUX2: Query Bluetooth address\n"
    SagSendAT(aux2_com, 'AT+SRBTADDR?\r')
    SagWaitnMatchResp(aux2_com, ['\r\n+SRBTADDR: "%s"\r\n' %aux2_bluetooth_address], 2000)
    SagWaitnMatchResp(aux2_com, ['OK\r\n'], 2000)
    
    print "\nStep 4: AUX2: Change Bluetooth state\n"
    SagSendAT(aux2_com, 'AT+SRBTSTATE=1,2\r')
    SagWaitnMatchResp(aux2_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 5: DUT: Configure SPP connection 1 to AUX1\n"
    SagSendAT(uart_com, 'AT+SRSPPCFG=%s\r' %aux1_bluetooth_address)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,0,"%s",SPP,0\r\n' %aux1_bluetooth_address], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 6: DUT: Configure SPP connection 2 to AUX2\n"
    SagSendAT(uart_com, 'AT+SRSPPCFG=%s\r' %aux2_bluetooth_address)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 2,0,"%s",SPP,0\r\n' %aux2_bluetooth_address], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 7: DUT: Activate SPP connection 1\n"
    SagSendAT(uart_com, 'AT+SRSPPCNX=1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTPAIR: "%s",1\r\n' %aux1_bluetooth_address], 3000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRSPPCNX: 1,1,*\r\n'], 5000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 5000)
    
    SagWaitnMatchResp(aux1_com, ['\r\n+SRBTPAIR: "%s",1\r\n' %dut_bluetooth_address], 3000)
    SagWaitnMatchResp(aux1_com, ['\r\n+SRBTCFG: 1,0,"%s",SPP,0\r\n' %dut_bluetooth_address], 5000)
    SagWaitnMatchResp(aux1_com, ['+SRSPPCNX: 1,1,*\r\n'], 5000)

    print "\nStep 8: DUT: Send data to AUX1\n"
    SagSendAT(uart_com, 'AT+SRSPPSND=1,"Hello DUT"\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 5000)
    
    SagWaitnMatchResp(aux1_com, ['+SRSPP_DATA: 1,9,Hello DUT\r\n'], 2000)
    
    print "\nStep 9: DUT: Activate SPP connection 2\n"
    SagSendAT(uart_com, 'AT+SRSPPCNX=2\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTPAIR: "%s",1\r\n' %aux2_bluetooth_address], 3000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRSPPCNX: 2,1,*\r\n'], 5000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 5000)
    
    SagWaitnMatchResp(aux2_com, ['\r\n+SRBTPAIR: "%s",1\r\n' %dut_bluetooth_address], 3000)
    SagWaitnMatchResp(aux2_com, ['\r\n+SRBTCFG: 1,0,"%s",SPP,0\r\n' %dut_bluetooth_address], 5000)
    SagWaitnMatchResp(aux2_com, ['+SRSPPCNX: 1,1,*\r\n'], 5000)
    
    print "\nStep 10: DUT: Send data to AUX2\n"
    SagSendAT(uart_com, 'AT+SRSPPSND=2,"Hello DUT"\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 5000)
    
    SagWaitnMatchResp(aux2_com, ['+SRSPP_DATA: 1,9,Hello DUT\r\n'], 2000)
    
    print "\nStep 11: DUT: Query current SPP connections\n"
    SagSendAT(uart_com, 'AT+SRSPPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,1,"%s",SPP,*\r\n' %aux1_bluetooth_address], 3000)
    SagWaitnMatchResp(uart_com, ['+SRBTCFG: 2,1,"%s",SPP,*\r\n' %aux2_bluetooth_address], 3000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 5000)
    
    print "\nStep 12: DUT: Close SPP connection\n"
    SagSendAT(uart_com, 'AT+SRSPPCLOSE=1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRSPPCLOSE: 1,0\r\n'], 5000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 5000)
    
    SagWaitnMatchResp(aux1_com, ['\r\n+SRSPPCLOSE: 1,0\r\n'], 5000)
    
    SagSendAT(uart_com, 'AT+SRSPPCLOSE=2\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRSPPCLOSE: 2,0\r\n'], 5000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 5000)
    
    SagWaitnMatchResp(aux2_com, ['\r\n+SRSPPCLOSE: 1,0\r\n'], 5000)
    
    print "\nStep 13: DUT: Delete SPP connection\n"
    SagSendAT(uart_com, 'AT+SRSPPDEL=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 5000)
    
    SagSendAT(uart_com, 'AT+SRSPPDEL=2\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 5000)
    
    print "\nTest Steps completed\n"
  
except Exception, err_msg :
    VarGlobal.statOfItem = "NOK"
    print Exception, err_msg
    SagSendAT(uart_com, 'AT&F\r')
    SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 2000)
    SagSendAT(aux1_com, 'AT&F\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nREADY\r\n'], 2000)
    SagSendAT(aux2_com, 'AT&F\r')
    SagWaitnMatchResp(aux2_com, ['*\r\nREADY\r\n'], 2000)
#Print test result
PRINT_TEST_RESULT(test_ID, VarGlobal.statOfItem)

# -----------------------------------------------------------------------------------

print "\n----- Test Body End -----\n"

print "-----------Restore Settings---------------"

# Clear paired list
SagSendAT(uart_com, "AT+SRBTUNPAIR\r")
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
SagSendAT(aux1_com, "AT+SRBTUNPAIR\r")
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
SagSendAT(aux2_com, "AT+SRBTUNPAIR\r")
SagWaitnMatchResp(aux2_com, ['\r\nOK\r\n'], 2000)

# Restore BT state to default
SagSendAT(uart_com, "AT+SRBTSTATE=0,0\r")
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
SagSendAT(aux1_com, "AT+SRBTSTATE=0,0\r")
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
SagSendAT(aux2_com, "AT+SRBTSTATE=0,0\r")
SagWaitnMatchResp(aux2_com, ['\r\nOK\r\n'], 2000)

print "\nAUX: Disable subsystem\n"
SagSendAT(aux1_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

print "\nDUT: Disable subsystem\n"
SagSendAT(uart_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

print "\nDUT: Disable subsystem\n"
SagSendAT(aux2_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(aux2_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)
# Close AUX1
SagClose(aux1_com)
# Close AUX2
SagClose(aux2_com)

