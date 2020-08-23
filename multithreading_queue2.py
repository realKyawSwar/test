import queue
import threading
import time

name_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]


class sample_Thread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q

    def run(self):
        print("initializing " + self.name)
        process_data(self.name, self.q)
        print("Exiting " + self.name)


# helper function to process data
def process_data(threadName, q):
    while not thread_exit_Flag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            print("% s processing % s" % (threadName, data))
            time.sleep(1)
        else:
            queueLock.release()
            time.sleep(1)


def main():
    thread_list = ["Thread-1", "Thread-2", "thread-3"]
    threads = []
    threadID = 1
    # Create new threads
    for thread_name in thread_list:
        thread = sample_Thread(threadID, thread_name, workQueue)
        thread.start()
        threads.append(thread)
        threadID += 1
    # Fill the queue
    queueLock.acquire()
    for items in name_list:
        workQueue.put(items)
    queueLock.release()
    # Wait for the queue to empty
    while not workQueue.empty():
        pass
    return threads


if __name__ == "__main__":
    thread_exit_Flag = 0
    queueLock = threading.Lock()
    workQueue = queue.Queue(len(name_list))
    threads = main()
    # Notify threads it's time to exit
    thread_exit_Flag = 1

    # Wait for all threads to complete
    for t in threads:
        t.join()
    print("Exit Main Thread")
