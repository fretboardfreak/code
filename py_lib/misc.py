import sys, getpass


def whoami():
    return getpass.getuser()


def colorize(color, message):
    if not sys.stdout.isatty():
        return message
    color_map = {
        'azure':   '36',
        'black':   '1;30',
        'blue':    '34',
        'cyan':    '36',
        'green':   '32',
        'grey':    '1;30',
        'magenta': '35',
        'maroon':  '35',
        'orange':  '1;31',
        'pink':    '1;31',
        'red':     '31',
        'spring':  '1;32',
        'teal':    '36',
        'violet':  '35',
        'white':   '0',
        'yellow':  '1;33',
    }
    escape = color_map.get(color.lower(), '0')
    return "\n".join("\033[%sm%s\033[0m" % (escape, line)
                     for line in message.splitlines())
