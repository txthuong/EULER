# Test Name                                     Description
# A_BX_EmbeddedSW_SPP_0003                      Check Syntax of write +SRSPPSND command with valid values, invalid values and values out of range
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
# A_BX_EmbeddedSW_SPP_0003
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_SPP_0003"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Check Syntax of write +SRSPPSND command with valid values, invalid values and values out of range" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: AUX: Query Bluetooth address\n"
    SagSendAT(aux1_com, 'AT+SRBTADDR?\r')
    SagWaitnMatchResp(aux1_com, ['\r\n+SRBTADDR: "%s"\r\n' %aux1_bluetooth_address], 2000)
    SagWaitnMatchResp(aux1_com, ['OK\r\n'], 2000)
    
    print "\nStep 2: AUX: Change Bluetooth state\n"
    SagSendAT(aux1_com, 'AT+SRBTSTATE=1,2\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 3: DUT: Configure SPP connection to AUX\n"
    SagSendAT(uart_com, 'AT+SRSPPCFG=%s\r' %aux1_bluetooth_address)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,0,"%s",SPP,0\r\n' %aux1_bluetooth_address], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 4: DUT: Change Bluetooth state\n"
    SagSendAT(uart_com, 'AT+SRBTSTATE=1,2\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 5: DUT: Activate connection to AUX with valid value\n"
    SagSendAT(uart_com, 'AT+SRSPPCNX=1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTPAIR: "%s",1\r\n' %aux1_bluetooth_address], 3000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRSPPCNX: 1,1,*\r\n'], 4000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 3000)
    
    SagWaitnMatchResp(aux1_com, ['\r\n+SRBTPAIR: "%s",1\r\n' %dut_bluetooth_address], 3000)
    SagWaitnMatchResp(aux1_com, ['\r\n+SRBTCFG: 1,0,"%s",SPP,0\r\n' %dut_bluetooth_address], 4000)
    SagWaitnMatchResp(aux1_com, ['+SRSPPCNX: 1,1,*\r\n'], 4000)
    
    print "\nStep 6: DUT: Send data to AUX with invalid value\n"
    SagSendAT(uart_com, 'AT+SRSPPSND=2,"Hello Euler"\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 910\r\n'], 2000)
    
    print "\nStep 7: DUT: Send data to AUX with invalid value\n"
    SagSendAT(uart_com, 'AT+SRSPPSND=@1,"Hello Euler" \r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 8:DUT: Send data to AUX with out of range value\n"
    SagSendAT(uart_com, 'AT+SRSPPSND=-1,"Hello Euler" \r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
   
    print "\nStep 9: DUT: Send data to AUX with valid value\n"
    SagSendAT(uart_com, 'AT+SRSPPSND=1,"Hello Euler"\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    SagWaitnMatchResp(aux1_com, ['+SRSPP_DATA: 1,11,Hello Euler\r\n'], 2000)
    
    print "\nStep 10: DUT: Send data to AUX with valid values\n"
    SagSendAT(uart_com, 'AT+SRSPPSND=1,"\\30\\31\\32"\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    SagWaitnMatchResp(aux1_com, ['+SRSPP_DATA: 1,3,012\r\n'], 2000)

    print "\nStep 11: DUT: Send data to AUX with valid values\n"
    SagSendAT(uart_com, 'AT+SRSPPSND=1,"/00/01/02/03"\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    SagWaitnMatchResp(aux1_com, ['+SRSPP_DATA: 1,12,/00/01/02/03\r\n'], 2000)

    print "\nStep 12: DUT: Close SPP connection\n"
    SagSendAT(uart_com, 'AT+SRSPPCLOSE=1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRSPPCLOSE: 1,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)

    SagWaitnMatchResp(aux1_com, ['\r\n+SRSPPCLOSE: 1,0\r\n'], 2000)
    
    print "\nStep 13: DUT: Delete SPP connection\n"
    SagSendAT(uart_com, 'AT+SRSPPDEL=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    SagSendAT(aux1_com, 'AT+SRSPPDEL=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
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

# Clear paired list
SagSendAT(uart_com, "AT+SRBTUNPAIR\r")
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
SagSendAT(aux1_com, "AT+SRBTUNPAIR\r")
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

# Restore BT state to default
SagSendAT(uart_com, "AT+SRBTSTATE=0,0\r")
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
SagSendAT(aux1_com, "AT+SRBTSTATE=0,0\r")
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

print "\nAUX: Disable subsystem\n"
SagSendAT(aux1_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

print "\nDUT: Disable subsystem\n"
SagSendAT(uart_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)
# Close AUX1
SagClose(aux1_com)
