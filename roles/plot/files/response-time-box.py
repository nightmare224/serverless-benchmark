import plotly.graph_objects as go
import os
import plotly.express as px
from plotly.subplots import make_subplots
from files import files
from config import *

task_name = input(f"Task Name (default task is {TASK_NAME}, press ENTER to skip): ")
TASK_NAME = TASK_NAME if task_name == "" else task_name
OUTPUT = f"{os.getcwd()}/result/pattern1/{TASK_NAME}-responsetime.html"


def get_response_time_from_file(filename):
    duration_list = []
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            line = line[:-1] if line[-1] == "\n" else line
            rsp = line.split(" ")
            if rsp[2] == "Wrote":
                # seconds
                duration = float(rsp[7][:-1])
                duration_list.append(duration)

    return duration_list

def get_response_time_from_filelist(filename_list):
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

    return duration_list


data = files(TASK_NAME)
testcase_list = sorted(data.get_pods_no())
testcase_no = len(testcase_list)
# fig = go.Figure()
fig = make_subplots(
    rows=2,
    cols=testcase_no,
    specs=[[{}]*testcase_no, [{"colspan": 3}]+[None]*(testcase_no-1)],
    shared_xaxes=True,
    shared_yaxes=True,
    vertical_spacing=0.05,
    horizontal_spacing=0.02,
    subplot_titles=["2 pod", "4 pod", "6 pod"],
)


color_list = px.colors.qualitative.Bold
is_showlegend = set()
for tc_no, testcase in enumerate(testcase_list):
    filename_list = data.get_logs_name(testcase)
    y = []
    for pod_no, filename in enumerate(filename_list):
        row = 1
        col = tc_no + 1
        resp_time_list = get_response_time_from_file(filename)
        y = resp_time_list
        x = [f"testcase-{pod_no}"] * len(resp_time_list)
        pod_name = f"pod{pod_no}"
        fig.add_trace(
            go.Box(
                y=y,
                x=x,
                name=pod_name,
                boxpoints=False,
                marker_color=color_list[int(pod_no)],
                # width=0.5
                legendgroup=f"pod{pod_no}",
                showlegend=not (pod_name in is_showlegend),
            ),
            row=row,
            col=col,
        )
        is_showlegend.add(pod_name)

for testcase in testcase_list:
    filename_list = data.get_logs_name(testcase)
    resp_time_list = get_response_time_from_filelist(filename_list)
    fig.add_trace(
        go.Box(
            y=resp_time_list,
            x=[testcase] * len(resp_time_list),
            name=testcase,
            boxmean='sd',
            marker_color="deepskyblue",
            # width=0.5
            showlegend=False
        ),
        row=2,
        col=1
    )

# fig.update_xaxes(visible=False)
fig.update_xaxes(showticklabels=False)
fig["layout"][f"yaxis1"]["title"] = "Response Time (second)"
fig["layout"][f"yaxis4"]["title"] = "Response Time (second)"
fig.update_layout(height=800, width=1300)

# fig.write_html(OUTPUT)
fig.show()
