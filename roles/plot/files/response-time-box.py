import plotly.graph_objects as go
import os
import plotly.express as px
from statistics import mean, stdev
from files import files
from config import *


task_name = input(f"Task Name (default task is {TASK_NAME}, press ENTER to skip): ")
TASK_NAME = TASK_NAME if task_name == "" else task_name
OUTPUT = f"{os.getcwd()}/result/{TASK_NAME}-responsetime.html"


def get_response_time_list(filename):
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


fig = go.Figure()

# x1 = ['day 1', 'day 1', 'day 1', 'day 1', 'day 1', 'day 1']
# x2 = ['day 2', 'day 2', 'day 2', 'day 2', 'day 2', 'day 2']

# fig = go.Figure()


# fig.add_trace(go.Box(
#     y=[0.2, 0.2, 0.6, 1.0, 0.5, 0.4],
#     x=x1,
#     name='kale1'
# ))
# fig.add_trace(go.Box(
#     y=[0.2, 0.7, 0.9, 0.1, 0.5, 0.3],
#     x=x2,
#     name='kale2'
# ))
# fig.add_trace(go.Box(
#     y=[0.6, 0.7, 0.3, 0.6, 0.0, 0.5, 0.7, 0.9, 0.5, 0.8, 0.7, 0.2],
#     x=x1*2,
#     name='radishes1'
# ))

data = files(TASK_NAME)
testcase_list = sorted(data.get_pods_no())
# print(pods_no)
# podno_dict = {"pod0":}
color_list = px.colors.qualitative.Bold
for testcase in testcase_list:
    print(testcase)
    filename_list = data.get_logs_name(testcase)
    # print(filename_list)
    for pod_no, filename in enumerate(filename_list):
        resp_time_list = get_response_time_list(filename)
        # print([testcase] * len(resp_time_list))
        fig.add_trace(
            go.Box(
                y=resp_time_list,
                x=[testcase] * len(resp_time_list),
                name=f"pod {pod_no}",
                # boxpoints=False,
                marker_color=color_list[int(pod_no)],
                # width=0.5
                showlegend=False
            )
        )

fig.update_layout(
    # height=600, width=300,
    # boxgroupgap=0.2,
    # boxgap=0.1,
    boxmode='group'
)
# fig.write_html(OUTPUT)
fig.show()
