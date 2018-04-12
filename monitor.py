from __future__ import print_function

import pyxhook
import time
import datetime
import json

#configuration

SLEEP_TIME_SECOND=5
CACHE_FILE="./data/cache"
ACTIVITY_FILE="./data/activity"
ASCII_SPACE=32


def notify_user_activity():
    """
    send a mail to the user or something, with a recap of the last week
    """
    pass

def persist_cache_to_activity(cache_file, activity_file):
    """
    get data from cache and aggregate it in activity for each day
        =>
            {
                2018: {
                    00: {
                        0: screentime_duration: 42 # <===== this is V1,
                        1: { # <=== this should be v2
                            begin:
                            end:
                            screentime_duration:
                            biggest_continuous_screentime_duration:
                            break_total_duration:
                            number_of_break:
                            biggest_break_duration:
                        },
                    }
                }
            }
    """
    # read data
    data = json.load(open(activity_file))
    # read cache
    with open(cache_file, "r") as cache:
        line = str.split(cache.readline())
        date = datetime.datetime.fromtimestamp(float(line[0]))
        duration = float(line[1])
        year = str(date.year)
        month = str(date.month)
        day = str(date.day)
        # append duration to data
        if year in data:
            if month in data[year]:
                if day in data[year][month]:
                    data[year][month][day] += duration
                else:
                    data[year][month][day] = duration
            else:
                data[year][month] = { day: duration }
        else:
            data[year] = { month:{ day: duration } }
    # write data
    with open(activity_file, 'w') as activity:
        json.dump(data, activity)

def user_is_active(timestamp, duration, file):
    """
    write that the user has been active for the corresponding time
    at a datetime in a cache file
        =>
        timestamp1;inactivity
        timestamp2;inactivity
        ...
    """
    with open(file, "a") as cache:
        cache.write("%s %s"%(timestamp, duration))
    

def kbevent(event):
    """
    Event trigger on user action, should kill the event listener for the 
    desired time and then put it back
    """
    global running
    global hookman
    try:
        user_is_active(time.time(), SLEEP_TIME_SECOND, CACHE_FILE)
        if event.Ascii == ASCII_SPACE:
            unregister_hook_callback(hookman)
            running = False
        else:
            unregister_hook_callback(hookman)
            time.sleep(SLEEP_TIME_SECOND)
            hookman = register_hook_callback()
    except Exception as e:
        unregister_hook_callback(hookman)
        time.sleep(5)
        hookman = register_hook_callback()

def unregister_hook_callback(hookman):
    hookman.cancel()

def register_hook_callback():
    """
    Register the trigger on the user action
    """
    #init
    hookman = pyxhook.HookManager()
    #event
    hookman.KeyDown = kbevent
    hookman.KeyUp = kbevent
    hookman.MouseMovement = kbevent
    hookman.MouseAllButtonsUp = kbevent
    hookman.MouseAllButtonsDown = kbevent
    # start & return
    hookman.start()
    return hookman


if __name__ == '__main__':
    hookman = register_hook_callback()

    running = True
    while running:
        time.sleep(0.2)

    # Close the listener when we are done (stop the thread)
    unregister_hook_callback(hookman)