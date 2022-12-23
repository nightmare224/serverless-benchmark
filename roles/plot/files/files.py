from pathlib import Path
from config import *

class files:
    def __init__(self, task, subpath = "", trgpod_no = 0):
        filepath = f'{Path(f"{__file__}").parent}/data/{subpath}/{task}'
        pods_no_with_parent = Path(filepath ).iterdir()
        self.pods_no = []
        for pod_no in pods_no_with_parent:
            if trgpod_no == 0:
                self.pods_no.append(pod_no.name)
            elif pod_no.name[-1] == str(trgpod_no):
                self.pods_no.append(pod_no.name)
        self.pods_no.sort(key=lambda x:x[1:3])
        # self.pods_no = [pod_no.name for pod_no in pods_no_with_parent]
        # for name in self.pods_no:
        # print(self.pods_no)
        self.resources = {}
        self.logs = {}
        for pod_no in self.pods_no:
            self.resources[pod_no] = [path for path in Path(f'{filepath}/{pod_no}/resource').iterdir()]
            self.logs[pod_no] = [path for path in Path(f'{filepath}/{pod_no}/log').iterdir()]

    def get_pods_no(self):
        return self.pods_no

    def get_resource_name(self, pod_no):
        return self.resources[pod_no]
        
    def get_logs_name(self, pod_no):
        return self.logs[pod_no]