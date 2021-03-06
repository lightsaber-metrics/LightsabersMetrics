from LightsabersMetrics import LSM
import PySimpleGUI as sg
import threading
import os

def buildLayout():
    statusText = sg.Text("Status: Stopped", tooltip="Current status of the program.", key="statusText", size=(20, 0))
    moduleText = sg.Text("Modules", enable_events=False, tooltip="Enable the modules by clicking the checkboxes below.")
    eventLogBox = sg.Checkbox("Event Log", tooltip="Saves event logs in the Logs folder.", default=True, key="eventLog")
    statBox = sg.Checkbox("Stats", tooltip="Saves stats (winner, map, loser, etc) to the Logs folder.", default=True, key="stats")
    streamerBox = sg.Checkbox("Streamer", tooltip="Write current stats to text files in the Stream folder to be read by OBS/Streamlabs.", key="streamer")
    scoreboardBox = sg.Checkbox("Scoreboard", tooltip="Automatically update HattrickSwayze's scoreboard.", key="sbBox", enable_events=True)
    scoreboardKeyText = sg.Text("Key:", tooltip="For more info, go to https://beegame.rocks/", key='sbKeyText')
    scoreboardKeyField = sg.InputText("", disabled=True, key="sbKey", size=(20, None), tooltip="Put your scoreboard key here.", disabled_readonly_background_color="grey")
    startRecordingButton = sg.Button("Start Recording", key="startButton", tooltip="Starts recording with the selected modules enabled.  Minimizes the window.")
    stopRecordingButton = sg.Button("Stop Recording", key="stopButton", tooltip="Stops the recording.", disabled=True)
    exitButton = sg.Button("Exit", key="exitButton", tooltip="Exits the program.")
    layout = [[statusText],
    [moduleText], 
    [eventLogBox], 
    [statBox], 
    [streamerBox], 
    [scoreboardBox, scoreboardKeyText, scoreboardKeyField], 
    [startRecordingButton, stopRecordingButton, exitButton]]
    return layout

if __name__ == '__main__':
    icon = os.path.join("res", "icon.ico")
    window = sg.Window("Lightsaber's Metrics", buildLayout(), icon=icon)
    while True:
        event, values = window.read()
        if (event == "exitButton" or event == sg.WIN_CLOSED):
            break
        if (event == "sbBox"):
            window['sbKey'].Update(disabled = not bool(window['sbBox'].get()))
            window['sbKey'].Update(value="")
        if (event == "startButton"):
            for element in window.element_list():
                if hasattr(element, 'Disabled'):
                    element.Update(disabled = True)
            window['exitButton'].Update(disabled = False)
            window['stopButton'].Update(disabled = False)
            window['statusText'].Update(value = "Status: Recording")
            window.minimize()
            modules = []
            if values['eventLog']:
                modules.append("logging")
            if values['stats']:
                modules.append("stats")
            if values['streamer']:
                modules.append("streamer")
            if values["sbBox"]:
                modules.append("scoreboard")
            metric = LSM(modules=modules, scoreboardKey=values['sbKey'])
            thread = threading.Thread(target=metric.record, daemon=True)
            thread.start()
        if (event == "stopButton"):
            for element in window.element_list():
                if hasattr(element, 'Disabled'):
                    element.Update(disabled = False)
                window['stopButton'].Update(disabled = True)
                window['sbKey'].Update(disabled = not bool(window['sbBox'].get()))
                window['statusText'].Update(value = "Status: Stopped")
                metric.stop()
    window.close()