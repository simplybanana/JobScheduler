from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from threading import Thread, Event
import RandomAttributes
import MachineDefine


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

#random number Generator Thread
thread = Thread()
thread_stop_event = Event()


def randomNumberGenerator():
    """
    Generate a random number every 1 second and emit to a socketio instance (broadcast)
    Ideally to be run in a separate thread?
    """
    i = 0
    j = []
    k = []
    while not thread_stop_event.isSet():

        if i % 2 == 0:
            j.append(i)
            k.append(i)
            socketio.emit('newnumber', {'XP13': j, 'XP251': j, 'WP01': k, 'JM01': j}, namespace='/test')
        else:
            j.append(i)
            socketio.emit('newnumber', {'XP13': j, 'XP251': j, 'JM01': j},
                          namespace='/test')
        socketio.sleep(10)
        i += 1


def randomJobs():
    g = MachineDefine.create_graph()
    i = 100000
    while not thread_stop_event.isSet():
        if i %2 == 0:
            j = RandomAttributes.Job(i, "Letter", 180000, 36000, 4, 0, False, "Color", "Env", 2, 36, foldType="Tri")
        else:
            j = RandomAttributes.Job(i, "Letter", 90000, 18000, 4, 0, False, "Color", "Env", 1, 18, foldType="Tri")
        g, path, time = RandomAttributes.job_path(g,j)
        for item in path:
            if type(item) != str:
                socketio.emit('newnumber', {item.name: item.queue}, namespace='/test')
        i += 1
        socketio.sleep(5)

@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('jobViewDash.html')


@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        thread = socketio.start_background_task(randomNumberGenerator)


if __name__ == '__main__':
    socketio.run(app)