#!/usr/bin/env python
'''
A highly configurable shortcut application.  Originally designed to open
Google Chrome in "app" mode but later re-written to allow general
scripting too.

IDEAS:
  - could create a 'sequenced google bookmark' element that would act the same
    as a 'google-chrome bookmark' element but after the google-chrome window is
    closed the next in the sequence would open.  Usefull for things like
    checking web-comics or news sites
'''
import sys, os.path, optparse, easygui, subprocess, ConfigParser, shlex

class Element:
  def __init__(self, title=str()):
    self.title = title

  def run(self):
    pass

  def __str__(self):
    pass

class EGList(Element):
  '''
  List Box generated via the easygui toolbox
  http://easygui.sourceforge.net
  '''
  def __init__(self, title=str(), message=str(), choices=list(),
               exitAfter = None):
    Element.__init__(title)
    self.message = message
    self.choices = choices
    self.exitAfter = exitAfter

  def __str__(self):
    return self.title

  @staticmethod
  def type():
    return 'EGList'

  def _getChoicesTuple(self):
    textChoices = list()
    counter = 0
    for i in self.choices:
      textChoices.append('%d: %s' % (counter, i.__str__()))
      counter = counter+1
    return tuple(textChoices)

  def run(self):
    while 1:
      choice = easygui.choicebox(msg = self.message,
                                 title = self.title,
                                 choices = self._getChoicesTuple())
      if not choice:
        return None
      index = int(choice[0])
      choice = self.choices[index]
      if isinstance(choice, Element):
        choice.run()
      if self.exitAfter:
        return

class EGMessage(Element):
  '''
  Message Box generated via the easygui toolbox
  http://easygui.sourceforge.net
  '''
  def __init__(self, title=str(), message=str(), ok_button='Ok'):
    Element.__init__(title)
    self.message = message
    self.ok_button = ok_button

  def __str__(self):
    return self.title

  @staticmethod
  def type():
    return 'EGMessage'

  def run(self):
    easygui.msgbox(title=self.title,
                   msg = self.message,
                   ok_button = self.ok_button)

class BashCommand(Element):
  '''
  Runs a generic bash command
  '''
  def __init__(self, title=str(), command=str()):
    Element.__init__(title)
    self.command = command

  def __str__(self):
    return self.title

  @staticmethod
  def type():
    return 'BashCommand'

  def run(self):
    cmd = []
    for i in shlex.split(self.command):
      if i.find(' ') >= 0:
        i = '"' + i + '"'
      cmd.append(i)
    return subprocess.Popen(cmd).wait()

class ZenList(Element):
  '''
  List Box provided courtesy of the Zenity package in Ubuntu
  '''
  def __init__(self, title=str(), command=str(), choices=list()
               exitAfter = None):
    Element.__init__(title)
    self.command = command
    self.choices = choices

  def __str__(self):
    return self.title

  @staticmethod
  def type():
    return 'ZenList'

  def _runZenity(self):
    pass

  def run(self):
    while 1:
      choice = self._runZenity()
      if not choice:
        return None
      index = int(choice[0])
      choice = self.choices[index]
      if isinstance(choice, Element):
        choice.run()
      if self.exitAfter:
        return


class Config:
  '''
  Load/Save the config file.  Also provide a barebones config when
  there isn't one.
  '''
  def __init__(self):
    self.valid = {EGList().type(): ['type', 'message', 'choices'],
                  EGMessage().type(): ['type', 'message', 'ok_button'],
                  BashCommand().type(): ['type', 'command']}

  def _sanitizeFilename(self, filename):
    return os.path.normpath(os.path.expanduser(filename))

  def _writeDefaultFile(self, fp):
    default = ConfigParser.SafeConfigParser()
    main = 'Main'
    bash = 'aBashCmd'
    message = 'aMessageCmd'
    default.add_section(main)
    default.set(main, 'type', 'EGList')
    default.set(main, 'message', 'A message for the readers')
    default.set(main, 'choices', '%s %s' % (bash, message))
    default.set(main, 'exitAfter', 'True')
    default.add_section(bash)
    default.set(bash, 'type', 'BashCommand')
    default.set(bash, 'command', 'echo "a command"')
    default.add_section(message)
    default.set(message, 'type', 'EGMessage')
    default.set(message, 'message', 'A message for the readers')
    default.set(message, 'ok_button', 'Ok')
    default.write(fp)

  def _getFile(self, filename):
    '''
    return a valid config filename.  if filename is None then Default
    is ~/.appifier.ini, next is ./.appifier.ini
    '''
    possibleFiles = ['~/.appifier', './appifier']
    if filename:
      possibleFiles.insert(0, filename)
    possibleFiles = [self._sanitizeFilename(i) for i in possibleFiles[:]]
    for i in range(0, len(possibleFiles)):
      fname = possibleFiles[i]
      if os.path.exists(fname):
        return fname
    fname = possibleFiles[0]
    default = open(fname, 'w')
    self._writeDefaultFile(default)
    default.close()
    return possibleFiles[0]

  def _recurseCreateElement(self, cp, element):
    elementType = cp.get(element, 'type')
    if elementType == EGList().type():
      choices = cp.get(element, 'choices').split(' ')
      choiceObjects = []
      for i in choices:
        choiceObjects.append(self._recurseCreateElement(cp, i))
      exitAfter = True
      if cp.has_option(element, 'exitAfter'):
        text = cp.get(element, 'exitAfter')
        if text in ['no', 'No', 'false', 'False', '0']:
          exitAfter = False
      return EGList(title=element,
                  message=cp.get(element, 'message'),
                  choices=choiceObjects,
                  exitAfter=exitAfter)

    if elementType == EGMessage().type():
      return EGMessage(title=element,
                     message=cp.get(element, 'message'),
                     ok_button=cp.get(element, 'ok_button'))

    if elementType == BashCommand().type():
      return BashCommand(title=element,
                         command=cp.get(element, 'command'))

  def save(self, mainElement, configFile):
    configFile = self._getFile(configFile)
    cp = ConfigParser.SafeConfigParser()

  def load(self, configFile=None):
    configFile = self._getFile(configFile)
    cp = ConfigParser.SafeConfigParser()
    cp.readfp(open(configFile), 'r')
    mainElement = self._recurseCreateElement(cp, 'Main')
    return (mainElement, configFile)
    
def parseCmdLine():
  '''
  manage cli invocation
  '''
  usage = '%prog'
  version = '%prog v0.0'
  description = __doc__
  parser = optparse.OptionParser(usage = usage, 
                                 version = version,
                                 description = description)
  parser.add_option('--config', '-c', dest='config', default=None,
                    help='use a different config file than expected')
  return parser.parse_args()

def main():
  (opts, args) = parseCmdLine()
  config = Config()
  (mainElement, configFile) = config.load(opts.config)
  print configFile
  print mainElement
  try:
    # call run on mainElement.
    mainElement.run()
  
  finally:
    # save the mainElement back to the same spot 
    #config.save(mainElement, configFile)
    return 1

  return 0


if __name__ == '__main__':
  try:
    sys.exit( main() )
  except KeyboardInterrupt:
    print 'Interrupted by User.'
    sys.exit( 1 )


