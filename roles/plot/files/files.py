from os import listdir

class files:
    def __init__(self, task):
        self.task = task
        self.pods_no = listdir(f'data/{self.task}')
        self.resources = {}
        self.logs = {}
        for pod_no in self.pods_no:
            self.resources[pod_no] = listdir(f'data/{self.task}/{pod_no}/resource')
            self.logs[pod_no] = listdir(f'data/{self.task}/{pod_no}/log')

    def get_pods_no(self):
        return self.pods_no

    def get_resource_name(self, pod_no):
        return self.resources[pod_no]
        
    def get_logs_name(self, pod_no):
        return self.logs[pod_no]