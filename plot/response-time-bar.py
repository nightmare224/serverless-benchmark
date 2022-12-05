import plotly.graph_objects as go
from statistics import mean

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

filename_list = ["./data/fpo/pod_no1/floating-point-operation-sine-dc4cd8956-8bcqd"]
bar_list.append(
    go.Bar(
        name="1 pod",
        x=x,
        y=get_response_time_list(filename_list),
    )
)

filename_list = ["./data/fpo/pod_no3/floating-point-operation-sine-65ffc5884b-b445g", "./data/fpo/pod_no3/floating-point-operation-sine-65ffc5884b-l6bxq", "./data/fpo/pod_no3/floating-point-operation-sine-65ffc5884b-sj76p"]
bar_list.append(
    go.Bar(
        name="3 pod",
        x=x,
        y=get_response_time_list(filename_list),
    )
)

fig = go.Figure(bar_list)


fig.update_layout(barmode="group")
fig.show()
