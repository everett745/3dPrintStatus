from threading import Timer


class RepeatedTimer(object):
  def __init__(self, interval, function, *args, **kwargs):
    self._timer = None
    self.interval = interval
    self.function = function
    self.args = args
    self.kwargs = kwargs
    self.is_running = False

  def _run(self):
    self.is_running = False
    self.start()
    self.function(*self.args, **self.kwargs)

  def start(self):
    if not self.is_running:
      self._timer = Timer(self.interval, self._run)
      self._timer.start()
      self.is_running = True

  def stop(self):
    self._timer.cancel()
    self.is_running = False


class BotStatus(object):
  def __init__(self):
    self.lastMessage = None
    self.errors = 0
    self.step = 1

  def setLastMessage(self, lastMessage):
    self.lastMessage = lastMessage
    self.errors = 0
    self.step = 1

  def nextStep(self):
    self.step = self.step + 1