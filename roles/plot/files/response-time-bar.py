import plotly.graph_objects as go
import os
from statistics import mean
from files import files


TASK = "floating-point-operation-sine"
OUTPUT = f"{os.getcwd()}/result/{TASK}-responsetime.html"


def get_response_time_list(filename_list):
    duration_list = []
    for filename in filename_list:
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                line = line[:-1] if line[-1] == "\n" else line
                rsp = line.split(" ")
                if rsp[2] == "Wrote":
                    # seconds
                    duration = float(rsp[7][:-1])
                    duration_list.append(duration)

    return [mean(duration_list), max(duration_list), min(duration_list)]


bar_list = []
x = ["Average time", "Max time", "Min time"]

data = files(TASK)
pods_no = data.get_pods_no()
for pod_no in pods_no:
    filename_list = data.get_logs_name(pod_no)
    bar_list.append(
        go.Bar(
            name=f"{pod_no[6:]} pod",
            x=x,
            y=get_response_time_list(filename_list)
        )
    )
fig = go.Figure(bar_list)

fig.update_layout(barmode="group")
fig.write_html(OUTPUT)
fig.show()
