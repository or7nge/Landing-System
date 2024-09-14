class Directive:
    def __init__(self, command="NO ARUKO", value=None):
        '''
        Commands:
        NO ARUKO [no value] - no aruko currently detected (in case of landing, the drone should start ascending to search for aruko)
        DESCEND [no value] - aruko is in the center, the drone should descend
        ROTATE [value] - drone should rotate itself [value] degrees clockwise
        MOVE [value] - drone should move [value] cm forward
        '''
        self.command = command
        self.value = value

    def __str__(self):
        if self.value:
            return f"{self.command} {self.value}"
        return self.command

    def color(self):
        if self.command == "NO ARUKO":
            return (100, 100, 100)
        elif self.command == "DESCEND":
            return (0, 255, 0)
        else:
            return (0, 0, 255)
