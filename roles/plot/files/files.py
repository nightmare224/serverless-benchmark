from pathlib import Path

class files:
    def __init__(self, task):
        pods_no_with_parent = Path(f'{Path(f"{__file__}").parent}/data/{task}').iterdir()
        self.pods_no = [pod_no.name for pod_no in pods_no_with_parent]
        self.resources = {}
        self.logs = {}
        for pod_no in self.pods_no:
            self.resources[pod_no] = [path for path in Path(f'{Path(f"{__file__}").parent}/data/{task}/{pod_no}/resource').iterdir()]
            self.logs[pod_no] = [path for path in Path(f'{Path(f"{__file__}").parent}/data/{task}/{pod_no}/log').iterdir()]

    def get_pods_no(self):
        return self.pods_no

    def get_resource_name(self, pod_no):
        return self.resources[pod_no]
        
    def get_logs_name(self, pod_no):
        return self.logs[pod_no]