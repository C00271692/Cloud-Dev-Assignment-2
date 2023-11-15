from flask import Flask, render_template, request  # from module import Class.


import os

import hfpy_utils
import swim_utils


app = Flask(__name__)


@app.get("/hello")
def hello():
    return "Hello from my first web app - cool, isn't it?"  # ANY string.


@app.post("/chart")
def display_chart():
    events = request.form["events"]
    (
        name,
        age,
        distance,
        stroke,
        the_times,
        converts,
        the_average,
    ) = swim_utils.get_swimmers_data(events)

    the_title = f"{name} (Under {age}) {distance} {stroke}"
    from_max = max(converts) + 50
    the_converts = [hfpy_utils.convert2range(n, 0, from_max, 0, 350) for n in converts]

    the_converts.reverse()
    the_times.reverse()

    the_data = zip(the_converts, the_times)
    return render_template(
        "chart.html",
        title=the_title,
        average=the_average,
        data=the_data,
    )


@app.get("/")
@app.get("/getswimmers")
def get_swimmers_names():
    files = os.listdir(swim_utils.FOLDER)
    files.remove(".DS_Store")
    names = set()
    for swimmer in files:
        names.add(swim_utils.get_swimmers_data(swimmer)[0])
    return render_template(
        "select.html",
        title="Select a swimmer to chart",
        data=sorted(names),
    )


@app.post("/displayevents")
def get_swimmers_events():
    swimmer = request.form["swimmer"]
    filenames = os.listdir(swim_utils.FOLDER)
    filenames.remove(".DS_Store")
    events = []
    for filename in filenames:
        name, age, distance, stroke = filename.split("-")
        if name == swimmer:
            events.append(filename)
    return render_template(
        "events.html",
        title="Select an event to chart",
        data=sorted(events),
    )


if __name__ == "__main__":
    app.run(debug=True)  # Starts a local (test) webserver, and waits... forever.
