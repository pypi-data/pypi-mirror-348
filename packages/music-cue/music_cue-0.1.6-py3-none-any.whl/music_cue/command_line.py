import ttkbootstrap as ttk
from music_cue.gui import MusicCueGui


def main():

    app = ttk.Window(
            title="MusicCue",
            themename="superhero",
            size=(1500, 800),
            resizable=(True, True),
        )    
    MusicCueGui(app)
    app.mainloop()


if __name__ == "__main__":
    main()
