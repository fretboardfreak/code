#!/usr/bin/env python
""" ttracker.py is a little script to help track what you're doing with your
    time by periodically bugging you for updates on your task activity on a
    user defined interval.

    Beware of choosing too large an interval though, when multiple tasks are
    chosen for a single interval the interval is simply split evenly between
    the chosen tasks. This could place unnecessary meaning on tasks that you
    only spent 3 or 4 minutes on during an interval of an hour because it may
    be logged as 20 minutes of activity if only 3 tasks are chosen.

    Choosing too small an interval just gets annoying but missing an occasional
    update is okay.  After a short time ttracker will give up on trying to get
    an update and just wait until the next interval; however, this will have
    the effect of temporarily doubling your interval and giving extra weight to
    small tasks.  Just a warning.
"""
import sys, optparse, os, subprocess, time
import configobj


class OptParser(optparse.OptionParser):
    def format_description(self, formatter):
        return self.description


# Config File Constants
FILENAME = None

MAIN_SECTION = 'main'
INTERVAL = 'interval'
LAST_UPDATE = 'lastUpdate'

TASKS_SECTION = 'tasks'

DEFAULT_INTERVAL = 20
DEFAULT_CONFIG = {MAIN_SECTION: {INTERVAL: DEFAULT_INTERVAL,
                                 LAST_UPDATE: 0},
                  TASKS_SECTION: {'Sanity Triage': 0,
                                  'Tickets': 0,
                                  'Emails': 0,
                                  'System Maintenance': 0,
                                  'Sprint Story': 0,
                                  'Meeting': 0,
                                  'Support External': 0,
                                  'Support Preventable': 0
                                  }
                 }

# Zenity constants
TIMEOUT = 300  # seconds
SEPARATOR = ","
TASK_LIST_CMD = ('zenity --list --text "%s" --height 400 '
                 '--checklist --multiple --separator "' + SEPARATOR +
                 '" --column "" --column "Task" ')
NEW_TASK_CMD = ('zenity --entry --text "Please enter a new task (comma '
                'separated for multiple, duplicates are ignored)"')
ADD_TASK = 'Add Task'


def setConfigDefaults(config):
    """ Make sure all the required sections and fields are in the config file.
    """
    _setSectionDefaults(config, DEFAULT_CONFIG)
    config.write()


def _setSectionDefaults(config, section):
    """ Set defaults for a section of the config.  Recurse on any subsections.
    """
    for name, value in section.iteritems():
        config.setdefault(name, value)
        if isinstance(value, dict):
            _setSectionDefaults(config[name], section[name])


def getConfig():
    """ Create and validate a new config object
    """
    config = configobj.ConfigObj(FILENAME)
    setConfigDefaults(config)
    return config


def addTasks(newTasks, config):
    """ Add a list of new tasks
    """
    for task in newTasks:
        if not task in config[TASKS_SECTION]:
            config[TASKS_SECTION].setdefault(task, 0)
    config.write()


def runZenityCmd(cmd):
    """ Run one of the zenity commands and return the stdout.

        :return: (str or None) The stdout of the zenity command or None if user
                 clicked cancel or the dialogue timed out.
    """
    retCode = None
    startTime = time.time()
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

    while retCode is None:
        retCode = proc.poll()
        if startTime + TIMEOUT < time.time():
            print "killing zenity..."
            subprocess.call(['killall', 'zenity'])
            break

    if retCode is None:  # timeout or user clicked cancel
        return None
    stdout, _ = proc.communicate()
    if stdout.strip() == '':
        return None
    return stdout


def update(config):
    """ Query the user for an update about what they're doing

        :return: True if an update was skipped, None otherwise
    """
    config.reload()
    lastUpdateTimestamp = float(config[MAIN_SECTION][LAST_UPDATE])
    minsSinceUpdate = (time.time() - lastUpdateTimestamp) / 60.0
    print "Mins since update: %s" % minsSinceUpdate

    tasks = config[TASKS_SECTION].keys()
    tasks.sort()
    taskList = ' '.join(['FALSE "%s"' % task for task in tasks])
    taskList += ' FALSE "%s"' % ADD_TASK

    msg = ('What tasks have you worked on in the last %s mins?' %
           int(minsSinceUpdate))
    response = runZenityCmd(TASK_LIST_CMD % msg + taskList)
    if response is None:
        return True

    tasks = [task.strip() for task in response.split(SEPARATOR)]

    newTasks = []
    if ADD_TASK in tasks:
        tasks.remove(ADD_TASK)
        newTaskString = runZenityCmd(NEW_TASK_CMD)
        newTasks = [task.strip() for task in newTaskString.split(SEPARATOR)]
        addTasks(newTasks, config)

    tasks.extend(newTasks)

    divisions = len(tasks)
    if divisions == 0:
        divisions = 1
    perTaskIncrement = minsSinceUpdate / divisions
    print "per task increment: %s" % perTaskIncrement

    print "Tasks to update: %s" % tasks
    for task in tasks:
        config[TASKS_SECTION][task] = (float(config[TASKS_SECTION][task]) +
                                       perTaskIncrement)
    config[MAIN_SECTION][LAST_UPDATE] = time.time()
    config.write()


def parseCmdLine():
    """
    manage cli invocation
    """
    usage = '%prog [options] CONFIG_FILE'
    version = '%prog v0.2'
    description = __doc__
    parser = OptParser(usage=usage, version=version, description=description)
    parser.add_option('-i', '--interval', default=DEFAULT_INTERVAL,
            help='Interval in minutes to bug user for task update.'
                 ' [default: %s]' % DEFAULT_INTERVAL)
    opts, args = parser.parse_args()
    if len(args) != 1:
        parser.error('Please specify a config file.')

    return opts, args


def main():
    opts, args = parseCmdLine()

    global FILENAME
    FILENAME = args[0]

    config = getConfig()

    if opts.interval:
        config[MAIN_SECTION][INTERVAL] = opts.interval

    config[MAIN_SECTION][LAST_UPDATE] = time.time()
    config.write()

    while 1:
        config.reload()
        interval = float(config[MAIN_SECTION][INTERVAL])
        print "%s minutes until next update..." % interval

        time.sleep(interval * 60)

        if update(config):
            print "Skipped update..."


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print "Interrupted by user. Exiting..."
