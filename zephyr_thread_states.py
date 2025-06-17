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
		
		self.threadIdToNameMap = {}
		self.semaphoreIdToNameMap = {}
		self.semaphoreIndex = 1
				


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



	### EVENT HANDLING ###



	# threads
	def threadCreate(self) :
		threadId = getEventFieldValue(self.currentEvent, "thread_id")
		threadName = getEventFieldValue(self.currentEvent, "name")
		if threadId in self.threadIdToNameMap.keys() :
			self.raiseAlreadyExistsException(threadId)
		self.threadIdToNameMap[threadId] = threadName

	def threadNameSet(self) :
		threadId = getEventFieldValue(self.currentEvent, "thread_id")
		threadName = getEventFieldValue(self.currentEvent, "name")
		if threadId not in self.threadIdToNameMap.keys() :
			self.raiseNotCreatedException(threadId)
		self.threadIdToNameMap[threadId] = threadName

	def threadSwitchedIn(self) :
		threadId = getEventFieldValue(self.currentEvent, "thread_id")
		threadName = getEventFieldValue(self.currentEvent, "name")
		self.checkThreadIntegrity(threadId, threadName)
		
		quark = self.ss.getQuarkAbsoluteAndAdd(threadName)
		self.ss.modifyAttribute(self.currentEvent.getTimestamp().toNanos(), "Running", quark)

	def threadSwitchedOut(self) :
		threadId = getEventFieldValue(self.currentEvent, "thread_id")
		threadName = getEventFieldValue(self.currentEvent, "name")
		self.checkThreadIntegrity(threadId, threadName)
		
		quark = self.ss.getQuarkAbsoluteAndAdd(threadName)
		self.ss.removeAttribute(self.currentEvent.getTimestamp().toNanos(), quark)
	
	# semaphors
	def semaphoreTakeEnter(self) :
		semaphoreId = getEventFieldValue(self.currentEvent, "id")
		semaphoreName = self.getOrCreateSemaphoreName(semaphoreId)
		
		quark = self.ss.getQuarkAbsoluteAndAdd(semaphoreName)
		self.ss.modifyAttribute(self.currentEvent.getTimestamp().toNanos(), "Take", quark)
		
	def semaphoreTakeBlocking(self) :
		return None
		
	def semaphoreTakeExit(self) :
		semaphoreId = getEventFieldValue(self.currentEvent, "id")
		self.checkSemaphoreIntegrity(semaphoreId)
		semaphoreName = self.semaphoreIdToNameMap[semaphoreId]
		
		quark = self.ss.getQuarkAbsoluteAndAdd(semaphoreName)
		self.ss.removeAttribute(self.currentEvent.getTimestamp().toNanos(), quark)

	def semaphoreGiveEnter(self) :
		semaphoreId = getEventFieldValue(self.currentEvent, "id")
		semaphoreName = self.getOrCreateSemaphoreName(semaphoreId)

		quark = self.ss.getQuarkAbsoluteAndAdd(semaphoreName)
		self.ss.modifyAttribute(self.currentEvent.getTimestamp().toNanos(), "Give", quark)

	def semaphoreGiveExit(self) :
		semaphoreId = getEventFieldValue(self.currentEvent, "id")
		self.checkSemaphoreIntegrity(semaphoreId)
			
		semaphoreName = self.semaphoreIdToNameMap[semaphoreId]
		
		quark = self.ss.getQuarkAbsoluteAndAdd(semaphoreName)
		self.ss.removeAttribute(self.currentEvent.getTimestamp().toNanos(), quark)
		
		

	### AUXILIARY ###



	def checkThreadIntegrity(self, threadId, threadName) :
		if threadId not in self.threadIdToNameMap.keys() :
			if threadName == "main" or threadName == "idle" :
				self.threadIdToNameMap[threadId] = threadName
			else :
				self.raiseThreadNotCreatedException(threadId)
		if self.threadIdToNameMap[threadId] != threadName :
			self.raiseWrongThreadNameException(threadId, threadName)

	def checkSemaphoreIntegrity(self, semaphoreId) :
		if semaphoreId not in self.semaphoreIdToNameMap.keys() :
			self.raiseSemaphoreNotCreatedException(semaphoreId)
			
	def getOrCreateSemaphoreName(self, semaphoreId) :
		if semaphoreId not in self.semaphoreIdToNameMap.keys() :
			semaphoreName = "semaphore_" + str(self.semaphoreIndex)
			self.semaphoreIndex += 1
			self.semaphoreIdToNameMap[semaphoreId] = semaphoreName
			return semaphoreName
		else :
			return self.semaphoreIdToNameMap[semaphoreId]



	### EXCEPTIONS ###


	
	def displayEntryError(self) :
		return "Error at entry no " + str(self.entryIndex) + ": " + str(self.currentEvent.getContent())
		
	def raiseThreadNotCreatedException(self, threadId) :
		raise Exception(self.displayEntryError() + "\nThread " + str(threadId) + " not created yet.")
	
	def raiseAlreadyExistsException(self, threadId) :
		raise Exception(self.displayEntryError() + "\nThread " + str(threadId) + " already exists.")

	def raiseWrongThreadNameException(self, threadId, threadName) :
		raise Exception(self.displayEntryError() + "\nThread " + str(threadId) + " name should be " + \
			self.threadIdToNameMap[threadId] + ", not " + threadName + ".")

	def raiseSemaphoreNotCreatedException(self, semaphoreId) :
		raise Exception(self.displayEntryError() + "\nSemaphore " + str(semaphoreId) + " not created yet.")

traceDisplay = TraceDisplay()
traceDisplay.runAnalysis()
traceDisplay.displayTimeLine()
