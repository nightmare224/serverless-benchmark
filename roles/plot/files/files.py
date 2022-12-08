from os import listdir

class files:
    def __init__(self, task):
        self.task = task
        self.pods_no = listdir(f'data/{self.task}')
        self.resources = {}
        self.logs = {}
        for pod_no in self.pods_no:
            tmp = listdir(f'data/{self.task}/{pod_no}/resource')
            self.resources[pod_no] = [f'data/{self.task}/{pod_no}/resource/{resource_name}' for resource_name in tmp]
            tmp = listdir(f'data/{self.task}/{pod_no}/log')
            self.logs[pod_no] = [f'data/{self.task}/{pod_no}/log/{log_name}' for log_name in tmp]

    def get_pods_no(self):
        return self.pods_no

    def get_resource_name(self, pod_no):
        return self.resources[pod_no]
        
    def get_logs_name(self, pod_no):
        return self.logs[pod_no]