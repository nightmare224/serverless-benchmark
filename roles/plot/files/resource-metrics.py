import plotly.graph_objects as go
import plotly.express as px
import os
from pathlib import Path
from plotly.subplots import make_subplots
from datetime import datetime
from files import files
from config import *

# Every one seconds would have metric

task_name = input(f"Task Name (default task is {TASK_NAME}, press ENTER to skip): ")
TASK_NAME = TASK_NAME if task_name == "" else task_name
OUTPUT = f"{os.getcwd()}/result/{TASK_NAME}-resource.html"


def to_MB(data):
    if data[-2:] == "kB":
        return float(data[:-2]) / 1000
    elif data[-2:] == "MB":
        return float(data[:-2])
    elif data[-2:] == "GB":
        return float(data[:-2]) * 1000
    elif data[-1:] == "B":
        return float(data[:-1]) / 1000 / 1000


# init and clean the file
def get_pod_to_resource(filename):
    pod_to_resource = {}
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            line = line[:-1] if line[-1] == "\n" else line
            rsrc = line.split("|")
            # retrive metric
            try:
                time = datetime.strptime(rsrc[0], "%Y/%m/%d %H:%M:%S ")
                pod_name = rsrc[1].split("_")[2]
                cpu = float(rsrc[2][:-1]) / CORE_NUM
                memory = float(rsrc[3][:-1])
                blocki = to_MB(rsrc[4].split(" / ")[0])
                blocko = to_MB(rsrc[4].split(" / ")[1])
            except:
                continue
            # set default
            pod_to_resource.setdefault(pod_name, {})
            pod_to_resource[pod_name].setdefault("time", [])
            pod_to_resource[pod_name].setdefault("cpu", [])
            pod_to_resource[pod_name].setdefault("memory", [])
            pod_to_resource[pod_name].setdefault("blocki", [])
            pod_to_resource[pod_name].setdefault("blocko", [])
            # store metric to array
            if time in pod_to_resource[pod_name]["time"]:
                pod_to_resource[pod_name]["cpu"][-1] = cpu
                pod_to_resource[pod_name]["memory"][-1] = memory
                pod_to_resource[pod_name]["blocki"][-1] = blocki
                pod_to_resource[pod_name]["blocko"][-1] = blocko
            else:
                pod_to_resource[pod_name]["time"].append(time)
                pod_to_resource[pod_name]["cpu"].append(cpu)
                pod_to_resource[pod_name]["memory"].append(memory)
                pod_to_resource[pod_name]["blocki"].append(blocki)
                pod_to_resource[pod_name]["blocko"].append(blocko)
    return pod_to_resource


def add_inflight(filename, pod_to_resource):
    # inflight request
    pod_name = Path(filename).name
    time_x = pod_to_resource[pod_name]["time"]
    inflight_y = [0]
    curr_time_idx = 0
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            line = line[:-1] if line[-1] == "\n" else line
            rsp = line.split(" ")
            time = datetime.strptime(f"{rsp[0]} {rsp[1]}", "%Y/%m/%d %H:%M:%S")
            while time > time_x[curr_time_idx]:
                inflight_y.append(inflight_y[curr_time_idx])
                curr_time_idx += 1
            if rsp[2] == "Wrote":
                inflight_y[curr_time_idx] -= 1
            elif rsp[2] == "Forking":
                inflight_y[curr_time_idx] += 1
    pod_to_resource[pod_name]["inflight"] = inflight_y
    return pod_to_resource


def format_time(pod_to_resource):
    for pod_name in pod_to_resource:
        starttime = pod_to_resource[pod_name]["time"][0]
        for idx, time in enumerate(pod_to_resource[pod_name]["time"]):
            pod_to_resource[pod_name]["time"][idx] = (time - starttime).total_seconds()
    return pod_to_resource


def add_trace_to_fig(fig, pod_to_resource, col_no, last):
    color_list = px.colors.qualitative.Bold
    col = col_no
    for pod_no, pod_name in enumerate(pod_to_resource.keys()):
        row = 1
        rsrc = pod_to_resource[pod_name]
        x = rsrc["time"]
        for rsrc_name in ["cpu", "memory", "blocki", "blocko", "inflight"]:
            y = rsrc[rsrc_name]
            fig.append_trace(
                go.Scatter(
                    x=x,
                    y=y,
                    name=f"pod{pod_no}",
                    marker_color=color_list[int(pod_no)],
                    legendgroup=f"pod{pod_no}",
                    showlegend=last and row == 1,
                ),
                row=row,
                col=col,
            )
            row += 1


data = files(TASK_NAME)
pods_no = sorted(data.get_pods_no())
testcase_no = len(pods_no)
metric_titles = [
    "CPU Load",
    "Memory Load",
    "Block I/O (In)",
    "Block I/O (Out)",
    "Inflight Request",
]
metric_no = len(metric_titles)

subplot_tiltes = []
for title in metric_titles:
    for i in range(testcase_no):
        subplot_tiltes.append(title)


fig = make_subplots(
    rows=metric_no,
    cols=len(pods_no),
    shared_xaxes=True,
    shared_yaxes=True,
    vertical_spacing=0.05,
    horizontal_spacing=0.02,
    subplot_titles=subplot_tiltes,
)
for num, pod_no in enumerate(pods_no):
    resource = data.get_resource_name(pod_no)[0]
    # print(f'resource: {resource}')
    logs = data.get_logs_name(pod_no)
    pod_to_resource = get_pod_to_resource(resource)
    for log in logs:
        pod_to_resource = add_inflight(log, pod_to_resource)
    pod_to_resource = format_time(pod_to_resource)
    add_trace_to_fig(fig, pod_to_resource, num + 1, (num + 1) == len(pods_no))

# fig.update_layout(height=1000, width=1500, title_text=f"{TASK_NAME}", showlegend=False)
fig.update_layout(height=1000, width=1500, title_text=f"{TASK_NAME}")


for i in range(testcase_no):
    offset = (metric_no - 1) * testcase_no + i + 1
    fig["layout"][f"xaxis{offset}"]["title"] = "Time (second)"
for i, unit in enumerate(
    [
        "CPU Load (%)",
        "Memory Load (%)",
        "Block In (MB)",
        "Block out (MB)",
        "Number of Inflight Request",
    ]
):
    offset = 1 + i * testcase_no
    fig["layout"][f"yaxis{offset}"]["title"] = unit

fig.write_html(OUTPUT)
fig.show()
