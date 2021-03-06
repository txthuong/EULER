# Test Name                                Description
# A_BX_POWER_SRPSCFG_0004                  Check if module can wake up from deep sleep with wake-up mode RTC GPIO and input level which will trigger wake-up to HIGH
#
# Requirement
#   1 Euler module
#   1 AP running at 2.4GHz band
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
    SagSendAT(uart_com, 'AT+FMM\r')
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet serial number"
    SagSendAT(uart_com, 'AT+CGSN\r')
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet revision information"
    SagSendAT(uart_com, 'ATI3\r')
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)

except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_POWER_SRPSCFG_0004
# -----------------------------------------------------------------------------------

test_ID = "A_BX_POWER_SRPSCFG_0004"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***************************************************************************************************************"
    print "%s: Check if module can wake up from deep sleep with wake-up mode RTC GPIO and input level which will trigger wake-up to HIGH" % test_ID
    print "***************************************************************************************************************"

    gpio_list = [2]

    for gpio in gpio_list:
        print "\nStep 1: Configure GPIO %s as input with internal pull down resistor" % gpio
        SagSendAT(uart_com, "AT+KGPIOCFG=%s,1,1\r" % gpio)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

        print "\nStep 2: Configure power saving in wake-up mode RTC GPIO with GPIO %s and level HIGH" % gpio
        SagSendAT(uart_com, "AT+SRPSCFG=0,%s,1\r" % gpio)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

        print "\nStep 3: Query power saving configure"
        SagSendAT(uart_com, "AT+SRPSCFG?\r")
        SagWaitnMatchResp(uart_com, ['\r\n+SRPSCFG: 0,%s,1' % gpio], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

        print "\nStep 4: Put module to deep sleep mode "
        SagSendAT(uart_com, "AT+SRPSMODE=1\r")

        print "\nStep 5: Send AT command to check if module is actual in sleep mode"
        for i in range(0, 5):
            SagSendAT(uart_com, "AT\r")
            resp = SagWaitResp(uart_com, ['\r\nOK\r\n'], 2000)
            if resp != '':
                print '----> Problem: Module is not in sleep mode !!!'
                VarGlobal.statOfItem = "NOK"
                break

        print "\nStep 6: Set GPIO %s to HIGH to Wake up module from deep sleep mode" % gpio
        wx.MessageBox('Set GPIO %s to HIGH to Wake up module then click "OK"' % gpio, 'Info',wx.OK)
        SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 2000)

        print "\nStep 7: Send AT command to check if module did wake up from deep sleep mode"
        for i in range(0, 5):
            SagSendAT(uart_com, "AT\r")
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

# Restore Power Saving Configuration to default
SagSendAT(uart_com, 'AT+SRPSCFG=0,0,0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)
