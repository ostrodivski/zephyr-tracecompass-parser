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
        elif eventName == "semaphore_take_blocking" :
            self.semaphoreTakeBlocking()
        elif eventName == "semaphore_take_exit" :
            self.semaphoreTakeExit()
        elif eventName == "semaphore_give_enter" :
            self.semaphoreGiveEnter()
        elif eventName == "semaphore_give_exit" :
            self.semaphoreGiveExit()

        elif eventName == "isr_enter" :
            self.isrEnter()
        elif eventName == "isr_exit" :
            self.isrExit()

        elif eventName == "socket_close_enter" :
            self.socketGenericStateEnter("close")
        elif eventName == "socket_close_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_shutdown_enter" :
            self.socketGenericStateEnter("shutdown")
        elif eventName == "socket_shutdown_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_bind_enter" :
            self.socketGenericStateEnter("bind")
        elif eventName == "socket_bind_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_connect_enter" :
            self.socketGenericStateEnter("connect")
        elif eventName == "socket_connect_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_listen_enter" :
            self.socketGenericStateEnter("listen")
        elif eventName == "socket_listen_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_accept_enter" :
            self.socketGenericStateEnter("accept")
        elif eventName == "socket_accept_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_sendto_enter" :
            self.socketGenericStateEnter("sendto")
        elif eventName == "socket_sendto_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_sendmsg_enter" :
            self.socketGenericStateEnter("sendmsg")
        elif eventName == "socket_sendmsg_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_recvfrom_enter" :
            self.socketGenericStateEnter("recvfrom")
        elif eventName == "socket_recvfrom_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_recvmsg_enter" :
            self.socketGenericStateEnter("recvmsg")
        elif eventName == "socket_recvmsg_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_fcntl_enter" :
            self.socketGenericStateEnter("fcntl")
        elif eventName == "socket_fcntl_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_ioctl_enter" :
            self.socketGenericStateEnter("ioctl")
        elif eventName == "socket_ioctl_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_poll_enter" :
            self.socketGenericStateEnter("poll")
        elif eventName == "socket_poll_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_getsockopt_enter" :
            self.socketGenericStateEnter("getsockopt")
        elif eventName == "socket_getsockopt_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_setsockopt_enter" :
            self.socketGenericStateEnter("setsockopt")
        elif eventName == "socket_setsockopt_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_getpeername_enter" :
            self.socketGenericStateEnter("getpeername")
        elif eventName == "socket_getpeername_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_getsockname_enter" :
            self.socketGenericStateEnter("getsockname")
        elif eventName == "socket_getsockname_exit" :
            self.socketGenericStateExit()
        elif eventName == "socket_socketpair_enter" :
            self.socketGenericStateEnter("socketpair")
        elif eventName == "socket_socketpair_exit" :
            self.socketGenericStateExit()

        elif eventName == "gpio_pin_configure_interrupt_enter" :
            self.gpioGenericStateEnter("pin configure interrupt")
        elif eventName == "gpio_pin_configure_interrupt_exit" :
            self.gpioGenericStateExit()
        elif eventName == "gpio_pin_configure_enter" :
            self.gpioGenericStateEnter("pin configure")
        elif eventName == "gpio_pin_configure_exit" :
            self.gpioGenericStateExit()
        elif eventName == "gpio_port_get_direction_enter" :
            self.gpioGenericStateEnter("port get direction")
        elif eventName == "gpio_port_get_direction_exit" :
            self.gpioGenericStateExit()
        elif eventName == "gpio_pin_get_config_enter" :
            self.gpioGenericStateEnter("pin get config")
        elif eventName == "gpio_pin_get_config_exit" :
            self.gpioGenericStateExit()
        elif eventName == "gpio_port_get_raw_enter" :
            self.gpioGenericStateEnter("port get raw")
        elif eventName == "gpio_port_get_raw_exit" :
            self.gpioGenericStateExit()
        elif eventName == "gpio_port_set_mask_raw_enter" :
            self.gpioGenericStateEnter("port set mask raw")
        elif eventName == "gpio_port_set_mask_raw_exit" :
            self.gpioGenericStateExit()
        elif eventName == "gpio_port_set_bits_raw_enter" :
            self.gpioGenericStateEnter("port set bits raw")
        elif eventName == "gpio_port_set_bits_raw_exit" :
            self.gpioGenericStateExit()
        elif eventName == "gpio_port_clear_bits_raw_enter" :
            self.gpioGenericStateEnter("port clear bits raw")
        elif eventName == "gpio_port_clear_bits_raw_exit" :
            self.gpioGenericStateExit()
        elif eventName == "gpio_port_toggle_bits_enter" :
            self.gpioGenericStateEnter("port toggle bits")
        elif eventName == "gpio_port_toggle_bits_exit" :
            self.gpioGenericStateExit()
        elif eventName == "gpio_init_callback_enter" :
            self.gpioGenericStateEnter("init callback")
        elif eventName == "gpio_init_callback_exit" :
            self.gpioGenericStateExit()
        elif eventName == "gpio_add_callback_enter" :
            self.gpioGenericStateEnter("add callback")
        elif eventName == "gpio_add_callback_exit" :
            self.gpioGenericStateExit()
        elif eventName == "gpio_remove_callback_enter" :
            self.gpioGenericStateEnter("remove callback")
        elif eventName == "gpio_remove_callback_exit" :
            self.gpioGenericStateExit()
        elif eventName == "gpio_get_pending_int_enter" :
            self.gpioGenericStateEnter("get pending int")
        elif eventName == "gpio_get_pending_int_exit" :
            self.gpioGenericStateExit()
        elif eventName == "gpio_fire_callbacks_enter" :
            self.gpioGenericStateEnter("fire callbacks")
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
        self.stateEnter(semaphoreName, "Take")

    def semaphoreTakeExit(self) :
        semaphoreId = getEventFieldValue(self.currentEvent, "id")
        semaphoreName = self.getSemaphoreNameOrCreate(semaphoreId)
        self.stateExit(semaphoreName)

    def semaphoreGiveEnter(self) :
        semaphoreId = getEventFieldValue(self.currentEvent, "id")
        semaphoreName = self.getSemaphoreNameOrCreate(semaphoreId)
        self.stateEnter(semaphoreName, "Give")

    def semaphoreGiveExit(self) :
        semaphoreId = getEventFieldValue(self.currentEvent, "id")
        semaphoreName = self.getSemaphoreNameOrCreate(semaphoreId)
        self.stateExit(semaphoreName)

    def semaphoreTakeBlocking(self) :
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

    # gpio
    def gpioGenericStateEnter(self, stateName) :
        self.stateEnter("gpio", stateName)

    def gpioGenericStateExit(self) :
        self.stateExit("gpio")




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
            self.entryIdToNameMap[semaphoreId] = "semaphore_" + str(self.semaphoreCounter)
            self.semaphoreCounter += 1
        return self.entryIdToNameMap[semaphoreId]

    def getSocketNameOrCreate(self, socketId) :
        if socketId not in self.entryIdToNameMap.keys() :
            self.entryIdToNameMap[socketId] = "socket_" + str(self.socketCounter)
            self.socketCounter += 1
        return self.entryIdToNameMap[socketId]



traceDisplay = TraceDisplay()
traceDisplay.runAnalysis()
traceDisplay.displayTimeLine()
