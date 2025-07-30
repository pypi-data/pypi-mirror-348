# Music Cue

Music Cue is a simple GUI based App to administer title and artist information in an Excel file.

## Data formatting of 'source' sheet

The data must be delivered in an Excel file, in a sheet called "Muziek". This sheet must contain
the following column header names:
- SESSION NAME
- EVENT
- CLIP NAME
- START TIME
- END TIME 
- DURATION
- STATE

The following rules apply to the data in the rest of the sheet
- The SESSION or Episode name must always begin with E01, E02, etc., where the digits represent an Episode index. The SESSION or Episode names must be present in all cells of the column.
- In the EVENT column events (integers) must be present. These number must be unique. The cells in the column may be empty for formatting purposes. If this is the case, all data on the corresponding row is not processed.
- The clip name must be formatted as follows: clip_name.file_format.text. The file format and preceding text is split of to enable the calculation of the clip name. As clip names are used in multiple episodes, the related artist and title can be administered just one time for all fragments in all episodes.
- Start and END time are in datetime format, where the first two digits which represents the episode index, are stripped off, when duration times are calculated.
- DURATION and STATE data is not used in the App.

## GUI Features

The app is build using the Python ttkbootstrap library. The GUI uses two tabs.

## General GUI tab

- With the "Browse" button the Excel file must be selected. It is recommended to place the Excel file of particular programs into different folders. If the App returns an application error, probably something is wrong with the formatting of the sheet. Check for example if the correct column header names are used and if all cells have meaningful data present (except data of columns DURATION and STATE in the "Muziek" tab)
- When the Excel is selected for the first time, the "Create" button must be pressed. This creates some additional sheets. First the so-called "Database sheet" where artist and title information is stored. Also, several reports are produced. The most important one is that per Episode, data is made available regarding the usage of particular clip names. When clips are used more than one time in an episode, the time of all individual clips is added. The clip with added times is therefor presented only one time in an episode sheet.
- The "Update" button can be used if additional Episodes have been added to the "Muziek" source sheet.
- The "Create or Update" button creates per Episode a new folder. In these folders music files can be stored.

![image info](./media/general_tab.png)

## Episode GUI tab

- First you need to select an episode using the drop-down menu.
- Using the "Get" button, the administered data per event is presented. You can move the columns of the data to ensure that clip names fits the space in the screen.
- When you select a particular event using the drop-down menu and press the "Edit" button, you can administer the Artist and Title information in an popup entry widget.
- When you place an MP4 formatted music file named "Episode.mp4" in a sub-folder of the program folder and press the "Split" button, the fragments of each event are made available for playback purposes.

![image info](./media/episode_tab.png)

## Installation

Music Cue requires Python 3.9 or higher to run.

Install the library using a Windows or MAC console

```sh
pip install music-cue
```

Then create a Python script called "music_cue_exe.py" with the following content

```sh
import music_cue.command_line
music_cue.command_line.main()
```

Place this file in a separate folder (in the example shown in "MusicCue"). Navigate to the folder using a windows or MAC terminal and execute (see last line in example with "python music_cue_exe.py") the script. A log file named "error-log.txt" is placed in the folder when the App is run for the first time for troubleshooting purposes.

```sh
C:\Users\verke>cd Desktop
C:\Users\verke\Desktop>cd "MusicCue"
C:\Users\verke\Desktop\MusicCue>python music_cue_exe.py
```

## To do
- Installation procedure for pydub library for Windows and MAC.
- Automatic backup of Excel files.
- Unit tests.

## License

MIT
