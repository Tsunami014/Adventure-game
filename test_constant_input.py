from pynput import keyboard

class EventLoop:
    def __init__(self):
        self.pressing = []
    
    def check(self):
        ks = []
        with keyboard.Events() as events:
            # Block for as much as possible
            event = events.get(0.1)
            if event is None:
                return []
            #if event.key == keyboard.KeyCode.from_char('s'):
            if isinstance(event, keyboard.Events.Press):
                if not event.key in self.pressing:
                    if 'char' in dir(event.key):
                        ks.append(event.key.char)
                    else:
                        ks.append(event.key.name)
                    self.pressing.append(event.key)
            elif isinstance(event, keyboard.Events.Release):
                if event.key in self.pressing:
                    self.pressing.remove(event.key)
        return ks

print('Press s')
e = EventLoop()

while True:
    found = e.check()
    if found != []:
        print(', '.join(found))
