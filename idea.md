##################
******************
2.1: moore's law:The number of  transistors in a dense
integrated circuit will continue to double in approx 2 year:

2.2 :
    - possible if set of instruction is independent of each other
        - in terms of execution order: if 1,2,3 task execute and finish in
            different order there is no differecne in final output;
        - and shared recource: should share as little resourece as possible
        

2.3:

    1.type of concurrency :
        - parallel programming
        - asynchronous programming

    2.parallel programming:
        - dividing the task in parts and assign each to each of cpu core
        - task thats are cup oriented meaing ( that task which need more 
        computation rather than work which is taking large iput or output)
        cpu bound.(graphics processing)
        - in a multicore processor and have a single threaded programm only 
        one core will be in charge of executing the task;

    3. Asynchronous programming:
        - task that need reading/writting from other device or user
        - subtask is assign to another thread and when its finish 
        returning result to main thred by callback function
            -in some language a object is given to main thread known as:
                -  object is type not yet completed and 
                - called future,promise or task;
                - application wait on its completition or check back later time;
        - example: db call, upload/download ,webservices call

2.4:

    1. python thread use GIL(Global interpeter lock):
        - what you get when os switch between thread
        - allows only one thread to hold the control of the Python interpreter
        - This means that in python only one thread will be executed at a time.
    2. multiprocessig:
        - use subprocess instead of thread
        - can be used the machanism of multiprocessor feature
        - this allows to remove global interpert lock and allows 
        python to use multiple processor core;

2.6:

    1.insalling package using pip from requiremet.txt
        - list required package in *.txt file 
        - run "pip3 install -r requirement.txt"

###############
***************
3.1:

    1. Process:
        - running instance of computer programm(has many instruction)
        - has memory and system resource,security attribute
        - has small parts named:- Thread (smallest sequence of instruction)
        - thread ebanles process to run multiple task at once
        - multicore : enable thread to be assigne to many core
        - single core: threads shares core;

    


3.2:

    two ways to creaing thread:
    1. calling and pasing thread 
    threading.Thread(group=None,target=node,name=Node,args=(),kwargs={},daemon=none)
        - group: grouping thread by name
        - target: name of funciotn
        - name: name of thread if not set then will be added like Thread{counter_of_thread}
        - args: argument to function
        - kwargs: if function takes dictionary argument
        - daemon: specify wheather the thread is terminated if its parent thread is dead

    2. implenting class:
        class demo(threading.Thread):
            def __int__(self,var):
                Thread.__int__(self) #must call it
                self.var =var

            def run(self): # function def here

        task=demo(var)
        task.start()
        task.join()

vvi:

        in this case we can create a for loop to create and start thread
        but we should not join() cause that will make to stop creatring new
        thread before finising of previous thread so we can do is we 
        add the thread to a list and then after addding all off them
        we will again make a for loop and start joining the theread 


3.3 :
    thread life cycle:

    new: when thread is created;
    ready: when start() is called;
        - thread is ready to be schedule in cpu
    running: when join() is called
        - mainThread goes to blocked state
        - and remaing blocked untill x thread is finished;

    -:running: when running thread goes to **running** state
    -:ready: when psused thread goes to **ready** state
    -:blocked: it it need some prior task to complete then 
    thread goes to **blocked** state
    -:termainated: when finished execution or unhandled
    error occurs;

    2. every thread has :
        - own counter : maintains intruction that is been executed current time
        - own memory stack : Scratch space for a thread and local var is kept here
        - register : to hold data that been used in computation.
    3. thread with in a process shares:
        - open files
        - network sockets
        - os resource 

    once a thread is start we have little control on how it works 
    os maintian a schedular for controlling thread;

    4. cpu determines which thread to run
    5. when one thread is stop in mid of execution and new thread is started (context switching) if the new thread is from different process then a expensive switch is 
    done thats why

        pp using thred is better( > ) than pp using process

    6. read about : thread interference (race condition)
        -two thread working on same resource:
        deposit(100)
        withdraw(50)

        1. d: reads var            balance = 0
        2. d suspended;             b=0;
        3. w reads and withdraws    b=-50
        4. d swithch back 
            reads it's own stack    b=0
        5. deposit                  b=100

        but the balance should be 50 



3.4: thread synchornization:

    1. best practice is to keep less shared resource:
    
    2. lock :(to synchronize access to shared resources) 
        - two state:
            -locked:
            - unlocked:

    3. locked by a thread can be unlocked by the same thread;(noother thread can unlock it)

    3.2 acquired: lock is being used by a thread;

    3.3 if other thread try to acquire lock it the trying thread 
    goes to blocked state;

    3.5 lock is created on shared resource;

    4. lock:
        - create a lock 
        - assign the resouce
        - lock is now acquired
        - if some exception occurs during execution of the current thread 
        there may be situation that the lock is not released ever that why 
        we can call the release() in fillay() method

    5. python with() statement can be used with locks,semaphore,files,networks:
            -- autometically acquires and releases the mentiond resources
    6. when to use lock:
        - needed if modifiying variables like adding or repalcing
        - not needed if just reading;

    7 lock.isAcquere(false) = just returns false if a thread is calling a locked lock dont put the calling thread to block state;

    8.lock.locked(): checks if a lock is acquried or not

    9. rLock(): "X" is acquiring a lock then again "X" calls the lock 
        normal lock will block the "X" lock but rLock() will just keep 
        continue "X" as this actually holding the lock;
3.5:
    semaphore:

    1. maintains a counter 
        - acquired is called counter is decremented
        - release called counter is incremented
        - counter never goes under 0
        - if 0 and called the calling thread goes to block 


    2: semaphore allows one or more thread to run at same time
        - by default 1


3.6 :

    Event:
        - one thread send a event and other waits(blocked) for it
        - set() makes true to release for blocked thread
        - clear make set() to false and blockes subsuquence thread

    pseudo code:

    cond = condition()

    #consume one item
    cond.acquire()
    while not an_item_is_avaiable()
        cond.wait()
    get_an_availavle_item()
    cond.release()

    # produce one item
    cond.acquire()
    make_an_intem_available()
    cond.notify()
    cond.release()


3.7:

    Inter thread communication:(Queue) { can be used instead of event and condition }
    put(): puts an item into thread
    get(): removes an item from queue
    task_done(): marks an item that is gotten from queue as completed/processed
    join(): blocks unitll all the item of queue is done 

    1: get() and put() are blocking call:
        - when queue is instantiate we can specify max number of item it 
        can have;

        - get(): if there is no item in queue then calling get() blocks the thread and remains blocked untill new item is put or user
        specified threshold time is reached;

        - put(): if queue() is full then calling put() block 
        and remains blocked untill get() is called or user specified 
        threshold time is finished;
        
    2 .poison pill technique:
        add a special value to queue as a check that no elemnt is ni queue

    3. after adding queue we are not waiting for all download to finish rather
    resizing stat working 

    4. firstly we created a thread for downloading the this add files to 
    queue and another thread to resize;
        -so ne need to complete all download ,resize can start
        - poison pill is added 

    3.8:
        1: do python threading only for i/o operation;
        for only Global intrepert lock
        2: GIL:
            -prevents multiple native thread to run in python
            - only one python thread is executed at a time;
            
        Q: then how multithreading works:
        it switches between threads
            - this slows down cpu bound operation
            - benefits i/o operatin cause untill i/o is completed all works are stopped

###############################################################

    4.1:
    1.every process has 
        -processor state 
        - security attribute
        - memory 
        - system resources
        - has some thread that shares the processes common all
          above 4 thing but not shares among other process
        -one interpreter for every proces so as GIL
        - there for multiple process can run in multiprocess
        architecture
        - as no shared memory need less synchronization 
        - can be paused and start by os call
        - can be terminated or paused using system call
        - higer memory footprint
        - expensive context switchs

    4.2
    1. argument passed to process architecture must be pickleable(serializable)
    porcess(group= none,target=none,name=none,args(),kwargs={}
    dameon=None)

    2 . like thread process has start() and join() 
        - start() an new worker process is created under main process
        - main porcess in blocked for worker proecess to finish

    -daemon :
        - when process exits all its daemon child process exits
        - if it has non-daemon child then process cant exit untill
        all its non-daemon process finishes 
        - daemon-child cant creates its own child process

    isalive(): status of process
    terminate();
    - process exit code:
        - 0 no error occure
        - >0 has error 
        - <0 means (-1*signal code)

    - forced kill process:
        - finally clause and exit handler will not run
        - shared resource will be inconsistance

4.3

    class multiprocessing.Pool(num_process,initializer,initargs,maxtasksperchild)
        -inilializer and initargs no need to be pickleable
    1: multiprocesser pool:
        - number of worker process == by default number of core avaiable
        - init function no need to be pickleable
        - if value is set to maxtaskperchild ther worker process is killed after
        that value and new process is created;

4.4 

    1: processes use os supported communication channel for communication.
    - pipe:
        - bidirectional two process can write at both end
        -  for case of three process if two writes on the same side 
        data may corrupt thats why queue comes in
    
    - queue:
        - it has semaphore and lock for process safety
        





            