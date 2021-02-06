# Lightsaber'sMetrics
This is a program that attempts to track stats in a live Killer Queen Black set, by taking screenshots of the game (via MSS) and performing image analysis.
Main file to run (right now) is LightsabersMetrics.py


## Features
  * Detect what map is being played on, and exactly when it starts
  * Accurately track berries in the hive for blue and gold
  * Track queen lives (working for most maps)
  * Real time 🐌 tracker
  * Detect the winning team
  * Detect the victory condition
  * Track a full best of 5 set
  * Output event log for each game
  * Output set information in CSV format
  
 ## Restrictions
  * Right now, this only works for fullscreen 1920x1080 KQB.  Other resolutions will break things horribly.  May only work with one monitor, too.
  * Alt-tabbing duing gameplay will probably break stuff.  Doing it in between sets or in between a match (during loading) *should* be okay.
  * This cannot be used on video streamed to/through Twitch/Discord, due to image compression.  It should work on locally recorded games.
  * I've only tested this on Windows, I've tried to make the code OS agnostic but I can't guarantee compatibility.
  
## Coming soon
  * GUI
  * Live text file editing for use with OBS
  * Integration with HattrickSwayze's Scoreboard
  * Player/Stat detection using Prosive's API
  * Gate control percentage

## Instructions
  Make sure you have Python 3.9 installed and in your system path
  Run this command to install required libraries
  ```console
  py -m pip install -r requirements.txt
  ```
  Start either the GUI or tracker directly in the command line
  ```console
  py MetricGui.py
  ```
  or
  ```console
  py LightsabersMetrics.py
  ```