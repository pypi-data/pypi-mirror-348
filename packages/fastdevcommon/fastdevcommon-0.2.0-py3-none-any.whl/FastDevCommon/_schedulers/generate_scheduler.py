import os
import time
from threading import Thread


class GenerateScheduler:
    def __init__(self):
        self.processes = {}
        self.trigger_processes = {}
        self.threahs = []

    def term(self):
        """
        结束进程
        :return:
        """
        print('%d to term child process' % os.getpid())
        try:
            for generate_id, p in self.processes.items():
                print('process %d-%d terminate' % (os.getpid(), p.pid))
                if p.is_alive:
                    p.terminate()
                    print('stop process')
                    p.join()
            self.processes = {}
        except Exception as e:
            print(str(e))
        try:
            for generate_id, p in self.trigger_processes.items():
                obj = p["obj"]
                obj.close()
            self.trigger_processes = {}
        except Exception as e:
            print(str(e))

    def generate_process(self, target, *args, generate_id=None, **kwargs):
        """
        生成进程
        :return:
        """
        process = Thread(target=target, args=(*args,))
        process.start()
        if generate_id:
            print(f"启动{generate_id}进程")
            self.processes.update({generate_id: process})
            time.sleep(0.2)
        else:
            self.threahs.append(process)


    def trigger_term(self, generate_id):
        """
        结束进程
        :return:
        """
        if generate_id in self.trigger_processes:
            obj = self.trigger_processes[generate_id]["obj"]
            obj.close()
            self.trigger_processes.pop(generate_id)
        if self.threahs:
            self.threahs = []


scheduler = GenerateScheduler()
