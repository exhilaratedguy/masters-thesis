class Notifier:
    def __init__(self):
        self.observers = []

    def subscribe(self, eventname, callback):
        self.observers.append([eventname, callback])

    def notify(self, eventname, *args):
        for observer in self.observers:
            if observer[0] == eventname:
                observer[1](*args)
