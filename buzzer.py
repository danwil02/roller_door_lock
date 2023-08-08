from PiicoDev_Buzzer import PiicoDev_Buzzer, sleep_ms

# Define some note-frequency pairs
notes = {
    "C4": 262,
    "Db": 277,
    "D": 294,
    "Eb": 311,
    "E": 330,
    "F": 349,
    "Gb": 370,
    "G": 392,
    "Ab": 415,
    "A": 440,
    "Bb": 466,
    "B": 494,
    "C5": 523,
    "rest": 0,  # zero Hertz is the same as no tone at all
}


class Buzzer:
    # define a melody - two-dimensional list of notes and note-duration (ms)
    success_melody = [
        ["C4", 200],
        ["E", 200],
        ["G", 200],
        ["rest", 100],
        ["C5", 100],
        ["C5", 100],
    ]

    fail_melody = [
        ["Gb", 300],
        ["Gb", 300],
        ["Gb", 300],
        ["rest", 100],
    ]

    def __init__(self) -> None:
        self.buzz = PiicoDev_Buzzer(volume=2)

    def play_tone(self, note_str="C4", duration_ms=100):
        self.buzz.tone(note_str, duration_ms)

    def play_success_melody(self):
        # play the melody
        for x in self.success_melody:
            note = x[0]  # extract the note name
            duration = x[1]  # extract the duration
            self.buzz.tone(notes[note], duration)
            sleep_ms(duration)

    def play_fail_melody(self):
        # play the melody
        for x in self.fail_melody:
            note = x[0]  # extract the note name
            duration = x[1]  # extract the duration
            self.buzz.tone(notes[note], duration)
            sleep_ms(duration)

    def play_sweep(self, reverse=False, duration=150):
        # play the melody
        freqs = list(notes.values())
        freqs.sort(reverse=reverse)
        for freq in freqs:
            self.buzz.tone(freq, duration)
            sleep_ms(duration)

    def play_pip(self):
        self.buzz.tone(notes["A"], dur=100)
        sleep_ms(100)


def buzzer_test():
    print("Buzzer test . . . ")
    buzzer = Buzzer()
    for i in range(0, 10):
        buzzer.play_pip()
    buzzer.play_sweep()
    buzzer.play_sweep(reverse=True)
    buzzer.play_success_melody()
    buzzer.play_fail_melody()
    print("Buzzer test . . . Done")


if __name__ == "__main__":
    buzzer_test()
