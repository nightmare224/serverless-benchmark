import plotly.graph_objects as go
import os
from plotly.subplots import make_subplots
from datetime import datetime


# Every one seconds would have metric


TASK = "floating-point-operation-sine"


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
        lines_len = len(lines)
        for cnt, line in enumerate(lines):
            line = line[:-1] if line[-1] == "\n" else line
            rsrc = line.split("|")
            # retrive metric
            time = datetime.strptime(rsrc[0], "%Y/%m/%d %H:%M:%S ")
            pod_name = rsrc[1].split("_")[2]
            cpu = float(rsrc[2][:-1])
            memory = float(rsrc[3][:-1])
            blocki = to_MB(rsrc[4].split(" / ")[0])
            blocko = to_MB(rsrc[4].split(" / ")[1])
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
    pod_name = os.path.basename(filename)
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


def add_trace_to_fig(fig, pod_to_resource, col_no):
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
                    name=f"{rsrc_name} pod{pod_no}",
                ),
                row=row,
                col=col,
            )
            row += 1


fig = make_subplots(
    rows=5,
    cols=2,
    shared_xaxes=True,
    shared_yaxes=True,
    vertical_spacing=0.05,
    horizontal_spacing=0.02,
    subplot_titles=(
        "cpu",
        "cpu",
        "memory",
        "memory",
        "block I/O (in)",
        "block I/O (in)",
        "block I/O (out)",
        "block I/O (out)",
        "inflight request",
        "inflight request",
    ),
)

pod_to_resource1 = get_pod_to_resource("./data/fpo/pod_no1/fpo-resource-1pod")
pod_to_resource1 = add_inflight(
    "./data/fpo/pod_no1/floating-point-operation-sine-dc4cd8956-8bcqd", pod_to_resource1
)
add_trace_to_fig(fig, pod_to_resource1, 1)
pod_to_resource2 = get_pod_to_resource("./data/fpo/pod_no3/fpo-resource-3pod")
add_inflight(
    "./data/fpo/pod_no3/floating-point-operation-sine-65ffc5884b-b445g",
    pod_to_resource2,
)
add_inflight(
    "./data/fpo/pod_no3/floating-point-operation-sine-65ffc5884b-l6bxq",
    pod_to_resource2,
)
add_inflight(
    "./data/fpo/pod_no3/floating-point-operation-sine-65ffc5884b-sj76p",
    pod_to_resource2,
)
add_trace_to_fig(fig, pod_to_resource2, 2)

fig.update_layout(
    height=1000, width=1300, title_text=f"{TASK} (hey -t 0 -z 1m -c 20 -q 5)", showlegend=False
)

fig['layout']['yaxis']['title']='percentage'
fig['layout']['yaxis3']['title']='percentage'
fig['layout']['yaxis5']['title']='MB'
fig['layout']['yaxis7']['title']='MB'
fig['layout']['yaxis9']['title']='request Count'
# fig.write_html(f"/Users/thl/Documents/VU/distributedSystem/lab/result/{TASK}.html")
fig.show()
