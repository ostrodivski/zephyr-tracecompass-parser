#
# This script is meant to be run on Trace Compass with EASE scripting module.
#

loadModule('/TraceCompass/Trace')
loadModule('/TraceCompass/Analysis')
loadModule('/TraceCompass/DataProvider')
loadModule('/TraceCompass/View')
loadModule('/TraceCompass/Utils')


class TraceDisplay :
    def __init__(self) :
        self.trace = getActiveTrace()
        self.analysis = createScriptedAnalysis(self.trace, "ringTimeLine.js")
        self.ss = self.analysis.getStateSystem(False)

        self.entryIndex = 1
        self.currentEvent = None
        self.eventIter = getEventIterator(self.trace)

        self.entryIdToNameMap = {}

        self.semaphoreCounter = 1
        self.mutexCounter = 1
        self.socketCounter = 1            

    ### MAIN FUNCTIONS ###



    # main loop
    def runAnalysis(self) :
        while self.eventIter.hasNext() :
            self.currentEvent = self.eventIter.next()        
            self.handleCurrentEvent()
        if self.currentEvent != None :
            self.ss.closeHistory(self.currentEvent.getTimestamp().toNanos())

    def displayTimeLine(self) :
        hmap = java.util.HashMap()
        hmap.put(ENTRY_PATH, '*')
        provider = createTimeGraphProvider(self.analysis, hmap)
        if provider != None :
            openTimeGraphView(provider)

    def handleCurrentEvent(self) :
        eventName = self.currentEvent.getName()
        if eventName == "thread_create" :
            self.threadCreate()
        elif eventName == "thread_name_set" :
            self.threadNameSet()            
        elif eventName == "thread_switched_in" :
            self.threadSwitchedIn()            
        elif eventName == "thread_switched_out" :
            self.threadSwitchedOut()

        elif eventName == "semaphore_take_enter" :
            self.semaphoreTakeEnter()
        elif eventName == "semaphore_take_exit" :
            self.semaphoreTakeExit()
        elif eventName == "semaphore_give_enter" :
            self.semaphoreGiveEnter()
        elif eventName == "semaphore_give_exit" :
            self.semaphoreGiveExit()
        elif eventName == "semaphore_take_blocking" :
            self.semaphoreTakeBlocking()

        elif eventName == "mutex_lock_enter" :
            self.mutexLockEnter()
        elif eventName == "mutex_lock_exit" :
            self.mutexLockExit()
        elif eventName == "mutex_unlock_enter" :
            self.mutexUnlockEnter()
        elif eventName == "mutex_unlock_exit" :
            self.mutexUnlockExit()
        elif eventName == "mutex_lock_blocking" :
            self.mutexLockBlocking()
    
        elif eventName == "isr_enter" :
            self.isrEnter()
        elif eventName == "isr_exit" :
            self.isrExit()

        elif eventName == "socket_close_enter" :
            self.socketGenericStateEnter("Close")
        elif eventName == "socket_close_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_shutdown_enter" :
            self.socketGenericStateEnter("Shutdown")
        elif eventName == "socket_shutdown_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_bind_enter" :
            self.socketGenericStateEnter("Bind")
        elif eventName == "socket_bind_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_connect_enter" :
            self.socketGenericStateEnter("Connect")
        elif eventName == "socket_connect_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_listen_enter" :
            self.socketGenericStateEnter("Listen")
        elif eventName == "socket_listen_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_accept_enter" :
            self.socketGenericStateEnter("Accept")
        elif eventName == "socket_accept_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_sendto_enter" :
            self.socketGenericStateEnter("Sendto")
        elif eventName == "socket_sendto_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_sendmsg_enter" :
            self.socketGenericStateEnter("Sendmsg")
        elif eventName == "socket_sendmsg_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_recvfrom_enter" :
            self.socketGenericStateEnter("Recvfrom")
        elif eventName == "socket_recvfrom_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_recvmsg_enter" :
            self.socketGenericStateEnter("Recvmsg")
        elif eventName == "socket_recvmsg_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_fcntl_enter" :
            self.socketGenericStateEnter("Fcntl")
        elif eventName == "socket_fcntl_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_ioctl_enter" :
            self.socketGenericStateEnter("Ioctl")
        elif eventName == "socket_ioctl_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_poll_enter" :
            self.socketGenericStateEnter("Poll")
        elif eventName == "socket_poll_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_getsockopt_enter" :
            self.socketGenericStateEnter("Getsockopt")
        elif eventName == "socket_getsockopt_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_setsockopt_enter" :
            self.socketGenericStateEnter("Setsockopt")
        elif eventName == "socket_setsockopt_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_getpeername_enter" :
            self.socketGenericStateEnter("Getpeername")
        elif eventName == "socket_getpeername_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_getsockname_enter" :
            self.socketGenericStateEnter("Getsockname")
        elif eventName == "socket_getsockname_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_socketpair_enter" :
            self.socketGenericStateEnter("Socketpair")
        elif eventName == "socket_socketpair_exit" :
            self.socketGenericStateExit()

        elif eventName == "net_recv_data_enter" :
            self.netRecvDataEnter()
        elif eventName == "net_recv_data_exit" :
            self.netRecvDataExit()
        elif eventName == "net_send_data_enter" :
            self.netSendDataEnter()
        elif eventName == "net_send_data_exit" :
            self.netSendDataExit()

        elif eventName == "gpio_pin_configure_interrupt_enter" :
            self.gpioGenericStateEnter("Pin configure interrupt")
        elif eventName == "gpio_pin_configure_interrupt_exit" :
            self.gpioGenericStateExit()
        elif eventName == "gpio_pin_configure_enter" :
            self.gpioGenericStateEnter("Pin configure")
        elif eventName == "gpio_pin_configure_exit" :
            self.gpioGenericStateExit()
        elif eventName == "gpio_port_get_direction_enter" :
            self.gpioGenericStateEnter("Port get direction")
        elif eventName == "gpio_port_get_direction_exit" :
            self.gpioGenericStateExit()
        elif eventName == "gpio_pin_get_config_enter" :
            self.gpioGenericStateEnter("Pin get config")
        elif eventName == "gpio_pin_get_config_exit" :
            self.gpioGenericStateExit()
        elif eventName == "gpio_port_get_raw_enter" :
            self.gpioGenericStateEnter("Port get raw")
        elif eventName == "gpio_port_get_raw_exit" :
            self.gpioGenericStateExit()
        elif eventName == "gpio_port_set_mask_raw_enter" :
            self.gpioGenericStateEnter("Port set mask raw")
        elif eventName == "gpio_port_set_mask_raw_exit" :
            self.gpioGenericStateExit()
        elif eventName == "gpio_port_set_bits_raw_enter" :
            self.gpioGenericStateEnter("Port set bits raw")
        elif eventName == "gpio_port_set_bits_raw_exit" :
            self.gpioGenericStateExit()
        elif eventName == "gpio_port_clear_bits_raw_enter" :
            self.gpioGenericStateEnter("Port clear bits raw")
        elif eventName == "gpio_port_clear_bits_raw_exit" :
            self.gpioGenericStateExit()
        elif eventName == "gpio_port_toggle_bits_enter" :
            self.gpioGenericStateEnter("Port toggle bits")
        elif eventName == "gpio_port_toggle_bits_exit" :
            self.gpioGenericStateExit()
        elif eventName == "gpio_init_callback_enter" :
            self.gpioGenericStateEnter("Init callback")
        elif eventName == "gpio_init_callback_exit" :
            self.gpioGenericStateExit()
        elif eventName == "gpio_add_callback_enter" :
            self.gpioGenericStateEnter("Add callback")
        elif eventName == "gpio_add_callback_exit" :
            self.gpioGenericStateExit()
        elif eventName == "gpio_remove_callback_enter" :
            self.gpioGenericStateEnter("Remove callback")
        elif eventName == "gpio_remove_callback_exit" :
            self.gpioGenericStateExit()
        elif eventName == "gpio_get_pending_int_enter" :
            self.gpioGenericStateEnter("Get pending int")
        elif eventName == "gpio_get_pending_int_exit" :
            self.gpioGenericStateExit()
        elif eventName == "gpio_fire_callbacks_enter" :
            self.gpioGenericStateEnter("Fire callbacks")
        elif eventName == "gpio_fire_callbacks_exit" :
            self.gpioGenericStateExit()





    ### EVENT HANDLING ###


    # thread
    def threadCreate(self) :
        threadId = getEventFieldValue(self.currentEvent, "thread_id")
        self.getThreadNameOrCreate(threadId)

    def threadNameSet(self) :
        threadId = getEventFieldValue(self.currentEvent, "thread_id")
        threadName = getEventFieldValue(self.currentEvent, "name")
        self.entryRename(threadId, threadName)

    def threadSwitchedIn(self) :
        threadId = getEventFieldValue(self.currentEvent, "thread_id")
        threadName = self.getThreadNameOrCreate(threadId)
        self.stateEnter(threadName, "Running")

    def threadSwitchedOut(self) :
        threadId = getEventFieldValue(self.currentEvent, "thread_id")
        threadName = self.getThreadNameOrCreate(threadId)
        self.stateExit(threadName)

    # semaphores
    def semaphoreTakeEnter(self) :
        semaphoreId = getEventFieldValue(self.currentEvent, "id")
        semaphoreName = self.getSemaphoreNameOrCreate(semaphoreId)
        self.stateEnter(semaphoreName, "Taking")

    def semaphoreTakeExit(self) :
        semaphoreId = getEventFieldValue(self.currentEvent, "id")
        semaphoreName = self.getSemaphoreNameOrCreate(semaphoreId)
        self.stateExit(semaphoreName)
        self.stateEnter(semaphoreName, "Taken")

    def semaphoreGiveEnter(self) :
        semaphoreId = getEventFieldValue(self.currentEvent, "id")
        semaphoreName = self.getSemaphoreNameOrCreate(semaphoreId)
        self.stateExit(semaphoreName)
        self.stateEnter(semaphoreName, "Give")

    def semaphoreGiveExit(self) :
        semaphoreId = getEventFieldValue(self.currentEvent, "id")
        semaphoreName = self.getSemaphoreNameOrCreate(semaphoreId)
        self.stateExit(semaphoreName)

    def semaphoreTakeBlocking(self) :
        pass
    
    def mutexLockEnter(self) :
        mutexId = getEventFieldValue(self.currentEvent, "id")
        mutexName = self.getMutexNameOrCreate(mutexId)
        self.stateEnter(mutexName, "Lock")

    def mutexLockExit(self) :
        mutexId = getEventFieldValue(self.currentEvent, "id")
        mutexName = self.getSemaphoreNameOrCreate(mutexId)
        self.stateExit(mutexName)

    def mutexUnlockEnter(self) :
        mutexId = getEventFieldValue(self.currentEvent, "id")
        mutexName = self.getMutexNameOrCreate(mutexId)
        self.stateEnter(mutexName, "Unlock")

    def mutexUnlockExit(self) :
        mutexId = getEventFieldValue(self.currentEvent, "id")
        mutexName = self.getSemaphoreNameOrCreate(mutexId)
        self.stateExit(mutexName)

    def mutexLockBlocking(self) :
        pass

    # isr
    def isrEnter(self) :
        self.stateEnter("isr", "interrupt")

    def isrExit(self) :
        self.stateExit("isr")

    # sockets
    def socketGenericStateEnter(self, stateName) :
        socketId = getEventFieldValue(self.currentEvent, "id")
        socketName = self.getSocketNameOrCreate(socketId)
        self.stateEnter(socketName, stateName)

    def socketGenericStateExit(self) :
        socketId = getEventFieldValue(self.currentEvent, "id")
        socketName = self.getSocketNameOrCreate(socketId)
        self.stateExit(socketName)

    # net
    def netRecvDataEnter(self) :
        self.stateEnter("net", "Recv data")
    def netRecvDataExit(self) :
        self.stateExit("net")
    def netSendDataEnter(self) :
        self.stateEnter("net", "Send data")
    def netSendDataExit(self) :
        self.stateExit("net")

    # gpio
    def gpioGenericStateEnter(self, stateName) :
        self.stateEnter("gpio", stateName)

    def gpioGenericStateExit(self) :
        self.stateExit("gpio")



    ### AUXILIARY ###



    def entryRename(self, entryId, newEntryName) :
        if entryId not in self.entryIdToNameMap.keys() :
            pass
        self.entryIdToNameMap[entryId] = newEntryName

    def stateEnter(self, entryName, stateName) :
        quark = self.ss.getQuarkAbsoluteAndAdd(entryName)
        self.ss.modifyAttribute(self.currentEvent.getTimestamp().toNanos(), stateName, quark)

    def stateExit(self, entryName) :
        quark = self.ss.getQuarkAbsoluteAndAdd(entryName)
        self.ss.removeAttribute(self.currentEvent.getTimestamp().toNanos(), quark)

    def getThreadNameOrCreate(self, threadId) :
        if threadId not in self.entryIdToNameMap.keys() :
            self.entryIdToNameMap[threadId] = getEventFieldValue(self.currentEvent, "name")
        return self.entryIdToNameMap[threadId]

    def getSemaphoreNameOrCreate(self, semaphoreId) :
        if semaphoreId not in self.entryIdToNameMap.keys() :
            self.entryIdToNameMap[semaphoreId] = "semaphore_" + str(self.semaphoreCounter) + \
                " (" + str(semaphoreId) + ")"
            self.semaphoreCounter += 1
        return self.entryIdToNameMap[semaphoreId]

    def getMutexNameOrCreate(self, mutexId) :
        if mutexId not in self.entryIdToNameMap.keys() :
            self.entryIdToNameMap[mutexId] = "mutex_" + str(self.mutexCounter) + \
                " (" + str(mutexId) + ")"
            self.mutexCounter += 1
        return self.entryIdToNameMap[mutexId]

    def getSocketNameOrCreate(self, socketId) :
        if socketId not in self.entryIdToNameMap.keys() :
            self.entryIdToNameMap[socketId] = "socket_" + str(self.socketCounter) + \
                " (" + str(socketId) + ")"
            self.socketCounter += 1
        return self.entryIdToNameMap[socketId]



traceDisplay = TraceDisplay()
traceDisplay.runAnalysis()
traceDisplay.displayTimeLine()
