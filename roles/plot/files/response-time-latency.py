import plotly.graph_objects as go
import os
import plotly.express as px
from plotly.subplots import make_subplots
from files import files
from config import *
from statistics import mean, median

task_name = input(f"Task Name (default task is {TASK_NAME}, press ENTER to skip): ")
TASK_NAME = TASK_NAME if task_name == "" else task_name
OUTPUT = f"{os.getcwd()}/result/{SUBPATH}/{TASK_NAME}-responsetime.html"


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

def response_mean(node_type, trgpod_no):
    data = files(TASK_NAME, node_type, trgpod_no)
    testcase_list = sorted(data.get_pods_no())
    # print(testcase_list)
    testcase_no = len(testcase_list)
    y = []
    x = []
    # print(testcase_list)
    for testcase in testcase_list:
        filename_list = data.get_logs_name(testcase)
        testcase_no = len(filename_list)
        name = ""
        for i in range(testcase_no):
            name += f"{testcase}{i}, "
        name = name[:-2]
        resp_time_list = get_response_time_from_filelist(filename_list)
        y_val = mean(resp_time_list)
        if node_type == "edge":
            y_val = y_val - 0.5
        y.append(y_val)

        x.append(int(testcase[1:3]))
    return x, y


fig = go.Figure()

x1, y1 = response_mean("cloud", "1")
x2, y2 = response_mean("edge", "5")


# color_list = px.colors.qualitative.Bold
color_list = ["blue", "darkorange"]

fig.add_trace(
    go.Bar(
        y=[j-i for i,j in zip(y1, y2)],
        x=x1,
        # name=node_type,
        # name=testcase_no,
        # name=testcase,
        # marker_color="deepskyblue",
        # marker_color=color_list[0],
        # line=dict(
        #         width=3
        #     )
        # showlegend=False, hoverinfo= 'y'
    )
)


# fig.update_xaxes(visible=False)
# fig.update_xaxes(showticklabels=False)
# fig["layout"][f"yaxis1"]["title"] = "Response Time (second)"
# fig["layout"][f"yaxis4"]["title"] = "Response Time (second)"
fig.update_layout(
    height=800,
    width=1000,
    xaxis=dict(title="Parellel requests"),
    yaxis=dict(title="Differnce of Execution time (s)"),
    legend={"itemsizing": "constant", "itemwidth": 30},
    font=dict(
        # family="Courier New, monospace",
        size=18,  # Set the font size here
        # color="RebeccaPurple"
    ),
    plot_bgcolor='rgba(0,0,0,0)'
)  # , hovermode="y unified")

# fig.write_html(OUTPUT)
fig.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True, gridwidth=1, gridcolor='gray')
fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True, gridwidth=1, gridcolor='gray')
fig.show()
