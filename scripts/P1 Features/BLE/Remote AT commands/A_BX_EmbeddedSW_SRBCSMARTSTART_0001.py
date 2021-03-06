# Test Name                                Description
# A_BX_EmbeddedSW_SRBCSMARTSTART_0001      Check syntax of command AT+SRBCSMARTSTART
#
# Requirement
#   2 Euler module
#
# Author: txthuong
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
    SagSendAT(uart_com, "AT+FMM\r")
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet serial number"
    SagSendAT(uart_com, "AT+CGSN\r")
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet revision information"
    SagSendAT(uart_com, "ATI3\r")
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet BlueTooth address"
    SagSendAT(uart_com, "AT+SRBTADDR?\r")
    resp = SagWaitResp(uart_com, ['*\r\nOK\r\n'], 2000)
    SagMatchResp(resp, ['*\r\nOK\r\n'])
    dut_bluetooth_address = resp.split('"')[1]

    print "\nGet BLE configure"
    SagSendAT(uart_com, "AT+SRBLE?\r")
    resp = SagWaitResp(uart_com, ['*\r\nOK\r\n'], 2000)
    dut_bt_name = resp.split('"')[1]
    dut_max_mtu = resp.split(',')[1]

    # AUX1 Initialization
    print "\nOpen AT Command port"
    aux1_com = SagOpen(aux1_com, 115200, 8, "N", 1, "None")

    # Display AUX1 information
    print "\nDisplay AUX1 information"
    print "\nGet model information"
    SagSendAT(aux1_com, "AT+FMM\r")
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet serial number"
    SagSendAT(aux1_com, "AT+CGSN\r")
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet revision information"
    SagSendAT(aux1_com, "ATI3\r")
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet BlueTooth address"
    SagSendAT(aux1_com, "AT+SRBTADDR?\r")
    resp = SagWaitResp(aux1_com, ['*\r\nOK\r\n'], 2000)
    SagMatchResp(resp, ['*\r\nOK\r\n'])
    aux1_bluetooth_address = resp.split('"')[1]

    print "\nGet BLE configure"
    SagSendAT(aux1_com, "AT+SRBLE?\r")
    resp = SagWaitResp(aux1_com, ['*\r\nOK\r\n'], 2000)
    aux1_bt_name = resp.split('"')[1]
    aux1_max_mtu = resp.split(',')[1]

except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_EmbeddedSW_SRBCSMARTSTART_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_SRBCSMARTSTART_0001"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***********************************************************************************************************************"
    print "%s: Check syntax of command AT+SRBCSMARTSTART" % test_ID
    print "***********************************************************************************************************************"

    print '\nOn AUX1...'
    print 'Step 1: Start BLE advertising'
    SagSendAT(aux1_com, "AT+SRBLEADV=1\r")
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

    print '\nOn DUT...'
    print 'Step 2: Configure an BLE connection to AUX1'
    SagSendAT(uart_com, 'AT+SRBLECFG=%s\r' % aux1_bluetooth_address)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLECFG: 1,0,"%s",%s\r\n' % (aux1_bluetooth_address, dut_max_mtu)], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)

    mtu = min (aux1_max_mtu, dut_max_mtu)

    print '\nStep 3: Active BLE connection to AUX1'
    SagSendAT(uart_com, 'AT+SRBLECNX=1\r')
    if not SagWaitnMatchResp(uart_com, ['\r\n+SRBLE_IND: 1,1\r\nOK\r\n'], 5000):
        raise Exception("---->Problem: DUT cannot connect to AUX1 properly !!!")
    SagWaitnMatchResp(uart_com, ['+SRBLEMTU: 1,%s\r\n' % mtu], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBLEMTU: 1,%s\r\n+SRBCSMART: 1,1,1\r\n' % mtu,'+SRBCSMART: 1,1,1\r\n+SRBLEMTU: 1,%s\r\n' % mtu], 2000)
    SagWaitnMatchResp(aux1_com, ['\r\n+SRBLECFG: 1,0,"%s",%s\r\n' % (dut_bluetooth_address, mtu)], 2000)
    SagWaitnMatchResp(aux1_com, ['+SRBLE_IND: 1,1\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['+SRBLEMTU: 1,%s\r\n' % mtu], 2000)
    SagWaitnMatchResp(aux1_com, ['+SRBLEMTU: 1,%s\r\n' % mtu], 2000)
    #SagWaitnMatchResp(aux1_com, ['+SRBLEMTU: 1,%s\r\n\r\n+SRBCSMART: 1,1,1\r\n' % mtu,'\r\n+SRBCSMART: 1,1,1\r\n+SRBLEMTU: 1,%s\r\n' % mtu], 2000)

    print '\nStep 4: Check +SRBCSMARTSTART test command'
    SagSendAT(uart_com, 'AT+SRBCSMARTSTART=?\r')
    if not SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000):
        print '----> Problem: Failed to test error case !!!'
        SagSendAT(uart_com, '+++')
        if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000):
            SagSendAT(uart_com, '\r')
            SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000)

    print '\nStep 5: Check +SRBCSMARTSTART execute command'
    SagSendAT(uart_com, 'AT+SRBCSMARTSTART\r')
    if not SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000):
        print '----> Problem: Failed to test error case !!!'
        SagSendAT(uart_com, '+++')
        if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000):
            SagSendAT(uart_com, '\r')
            SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000)

    print '\nStep 6: Check +SRBCSMARTSTART read command'
    SagSendAT(uart_com, 'AT+SRBCSMARTSTART?\r')
    if not SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000):
        print '----> Problem: Failed to test error case !!!'
        SagSendAT(uart_com, '+++')
        if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000):
            SagSendAT(uart_com, '\r')
            SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000)

    data = 'Data from DUT'

    print '\nStep 7: Check +SRBCSMARTSTART write command with invalid parameter <session id>'
    session_id = ['a', 'A', '*', '#']
    for session in session_id:
        SagSendAT(uart_com, 'AT+SRBCSMARTSTART=%s,0\r' % session)
        if not SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000):
            print '----> Problem: Failed to test error case !!!'
            SagSendAT(uart_com, '+++')
            if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000):
                SagSendAT(uart_com, '\r')
                SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000)

    print '\nStep 8: Check +SRBCSMARTSTART write command with out-range and not configured <session id>'
    session_id = [-1, 0, 2, 3, 10, 20, 64, 65]
    for session in session_id:
        SagSendAT(uart_com, 'AT+SRBCSMARTSTART=%s,0\r' % session)
        if not SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 910\r\n'], 2000):
            print '----> Problem: Failed to test error case !!!'
            SagSendAT(uart_com, '+++')
            if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000):
                SagSendAT(uart_com, '\r')
                SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000)

    print '\nStep 9: Check +SRBCSMARTSTART write command with invalid parameter <gatt role>'
    gatt_role = [-1, 2, 'a', 'A', '*', '#']
    for role in gatt_role:
        SagSendAT(uart_com, 'AT+SRBCSMARTSTART=1,%s\r' % role)
        if not SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000):
            print '----> Problem: Failed to test error case !!!'
            SagSendAT(uart_com, '+++')
            if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000):
                SagSendAT(uart_com, '\r')
                SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000)

    print '\nStep 10: Check +SRBCSMARTSTART write command with missing parameters'
    SagSendAT(uart_com, 'AT+SRBCSMARTSTART=\r')
    if not SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000):
        print '----> Problem: Failed to test error case !!!'
        SagSendAT(uart_com, '+++')
        if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000):
            SagSendAT(uart_com, '\r')
            SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000)

    SagSendAT(uart_com, 'AT+SRBCSMARTSTART=,0\r')
    if not SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000):
        print '----> Problem: Failed to test error case !!!'
        SagSendAT(uart_com, '+++')
        if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000):
            SagSendAT(uart_com, '\r')
            SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000)

    SagSendAT(uart_com, 'AT+SRBCSMARTSTART=1\r')
    if not SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000):
        print '----> Problem: Failed to test error case !!!'
        SagSendAT(uart_com, '+++')
        if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000):
            SagSendAT(uart_com, '\r')
            SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000)

    print '\nStep 11: Check +SRBCSMARTSTART write command with extra parameter'
    SagSendAT(uart_com, 'AT+SRBCSMARTSTART=1,0,1\r')
    if not SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000):
        print '----> Problem: Failed to test error case !!!'
        SagSendAT(uart_com, '+++')
        if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000):
            SagSendAT(uart_com, '\r')
            SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000)

    SagSendAT(uart_com, 'AT+SRBCSMARTSTART=1,0,a\r')
    if not SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000):
        print '----> Problem: Failed to test error case !!!'
        SagSendAT(uart_com, '+++')
        if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000):
            SagSendAT(uart_com, '\r')
            SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000)

    print '\nStep 12: Check +SRBCSMARTSTART write command with valid parameters'
    SagSendAT(uart_com, 'AT+SRBCSMARTSTART=1,0\r')
    if not SagWaitnMatchResp(uart_com, ['\r\nCONNECT\r\n'], 2000):
        print '----> Problem: Module did not go to data mode properly!!!'
        SagSendAT(uart_com, '+++')
        if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000):
            SagSendAT(uart_com, '\r')
            SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000)
    else:
        SagSendAT(uart_com, '%s' % data)
        SagSendAT(uart_com, '+++')
        SagWaitnMatchResp(aux1_com, ['+SRBCSMARTRECV: 1,1,"%s"\r\n' % data], 2000)
        if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000):
            print '----> Problem: Module did not escape data mode properly !!!'
            SagSendAT(uart_com, '+++')
            if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000):
                SagSendAT(uart_com, '\r')
                SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 2000)

    print '\nStep 13: Close BLE connection'
    print 'On DUT...'
    SagSendAT(uart_com, "AT+SRBLECLOSE=1\r")
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLE_IND: 1,0,22\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['\r\n+SRBLE_IND: 1,0,19\r\n'], 2000)

    print '\nStep 14: Delete BLE configuration'
    print 'On DUT...'
    SagSendAT(uart_com, "AT+SRBLEDEL=1\r")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    print 'On AUX1...'
    SagSendAT(aux1_com, "AT+SRBLEDEL=1\r")
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

    print '\nStep 15: Query BLE configuration'
    print 'On DUT...'
    SagSendAT(uart_com, "AT+SRBLECFG?\r")
    if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000):
        raise Exception("---->Problem: BLE configure was not closed and delete properly !!!")
    print 'On AUX1...'
    SagSendAT(aux1_com, "AT+SRBLECFG?\r")
    if not SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000):
        raise Exception("---->Problem: BLE configure was not closed and delete properly !!!")

    print "\nTest Steps completed"

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
# Close AUX1
SagClose(aux1_com)