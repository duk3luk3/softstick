import curses

class Switch:
  def __init__(self, label, positions, defidx):
    self.positions = positions
    self.label = label
    self.idx = defidx
    self.master = None
    self.slaves = []
    self.locked = False

  def set(self, idx, chain):
    if chain == None:
      chain = True
    if idx >= 0 and idx < len(self.positions):
      self.idx = idx
      for slave in self.slaves:
        if slave.locked and chain:
          slave.set(idx, True)
      if self.master and self.master.locked:
        self.master.set(idx, False)

  def inc(self, chain):
    if self.idx < len(self.positions)-1:
      self.idx += 1
      for slave in self.slaves:
        if slave.locked and chain:
          slave.inc(True)
      if self.master and self.master.locked and chain:
        self.master.inc(False)

  def dec(self, chain):
    if self.idx > 0:
      self.idx -= 1
      for slave in self.slaves:
        if slave.locked and chain:
          slave.dec(True)
      if self.master and self.master.locked and chain:
        self.master.dec(False)

  def lock(self):
    self.locked = True
    for slave in self.slaves:
      slave.locked = True

  def unlock(self):
    self.locked = False

  def toggle_lock(self):
    if self.locked:
      self.unlock()
    else:
      self.lock()


class Panel:
  def __init__(self):
    self.switches = []
    self.switch_idx = 0

  def render(self, screen):
    screen.clear()

    screen.addstr(0,0,"hello")

    line = 1

    for swidx in range(len(self.switches)):
      switch = self.switches[swidx]
      if swidx == self.switch_idx:
        screen.addstr(line,0,'>')

      screen.addstr(line, 2, switch.label)
      for idx in range(len(switch.positions)):
        if idx == switch.idx:
          screen.addstr(line, 10+(idx*4), ">" + str(switch.positions[idx]) + "<")
        else:
          screen.addstr(line, 10+(idx*4), " " + str(switch.positions[idx]) + " ")
      line += 1

    screen.refresh()

def main(stdscr):
  mwin = curses.newwin(3,80,20,0)

  p = Panel()
  lthrottle = Switch("L", [0,1,2,3,4,5,6,7,8,9,10,11,12],0)
  rthrottle = Switch("R", [0,1,2,3,4,5,6,7,8,9,10,11,12],0)
  lthrottle.slaves = [rthrottle]
  rthrottle.master = lthrottle
  rthrottle.lock()

  p.switches.append(lthrottle)
  p.switches.append(lthrottle)
  p.switches.append(Switch("Gear", ['UP','DN'],1))

  p.render(stdscr)
  
  key = stdscr.getch()
  while key != ord('x'):
    if key == curses.KEY_UP:
      if p.switch_idx > 0:
        p.switch_idx -= 1
    elif key == curses.KEY_DOWN:
      if p.switch_idx < len(p.switches)-1:
        p.switch_idx += 1
    elif key == curses.KEY_LEFT:
      p.switches[p.switch_idx].dec(True)
    elif key == curses.KEY_RIGHT:
      p.switches[p.switch_idx].inc(True)
    elif key >= ord('1') and key <= ord('9'):
      p.switches[p.switch_idx].set(int(chr(key)))
    elif key == ord('0'):
      p.switches[p.switch_idx].set(10)
    elif key == ord('`'):
      p.switches[p.switch_idx].set(0)
    elif key == ord('-'):
      p.switches[p.switch_idx].set(11)
    elif key == ord('='):
      p.switches[p.switch_idx].set(12)
    elif key == ord(' '):
      p.switches[p.switch_idx].toggle_lock()
  
    p.render(stdscr)
    mwin.addstr(0,0,str(key))
    mwin.refresh()

    key = stdscr.getch()


if __name__ == "__main__":
  curses.wrapper(main)
