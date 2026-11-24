# Spike 1: Exporting and reading FL projects from code

**Date:** 2026-11-23
**Result:** Both work. FL can export single projects from Python, and flpdiff can read project info from Python, including tempo, time spent, created date, plugins, and samples. PyFLP doesn't work.

## Questions

1. Can code make FL Studio export a project to MP3 reliably, without me clicking anything?
2. Can code read info like BPM, instruments, and samples straight from a .flp file?

This matters because the whole app depends on it. Exporting audio is what lets Repriz work without uploads, and reading the file is how the app knows what's in each beat without opening FL. If either doesn't work, the core idea needs a different approach, so I tested them before designing or building anything else.

## Setup

- **OS:** Windows
- **FL version:** FL Studio 2024
- **Python:** 3.14 (also tried 3.13 for PyFLP)
- **Test projects:** copies of a few of my projects in `C:\BeatTest` (never test on the real projects folder). Included short projects, a longer project, and projects with missing samples or plugins.

## Part 1: Exporting by hand in PowerShell

### Command used

```powershell
& "C:\Program Files\Image-Line\FL Studio 2024\FL64.exe" /R /Emp3 /FC:\BeatTest
```

- `&` runs a program whose path has spaces in PowerShell
- `/R` means render
- `/Emp3` means export as MP3
- `/F` points at the folder of projects to export, with no space before the path

### Results

- **Basic render:** The FL Studio window opened and showed the export progress, but I didn't have to click anything. It was really quick, although my projects were pretty short. Everything sounded good. The MP3s were saved in the same folder as the projects.
- **Long project:** About 20 seconds, around the same time as exporting normally, maybe slightly quicker.
- **Missing plugins:** FL showed a message that something was missing, and I had to click OK before it kept going. After that it finished exporting.
- **FL already open:** Nothing happened.

## Part 2: Exporting from Python

Code: `render_test.py`

### Results

- Python can run FL's export with subprocess, just requires correct formatting and calling of files, mimic what is written for the terminal.
- The rendered message prints whenever FL finishes even if nothing was exported, so the app needs to check that the MP3 actually exists before marking it complete.
- The timeout force-closes FL. At 30 seconds it cut off an export of the whole folder.

### Exporting a single project

Works by passing the project path on its own, without `/F` (`/F` is for folders). Only that project's MP3 was created.

```python
subprocess.run(
    [
        r"C:\Program Files\Image-Line\FL Studio 2024\FL64.exe",
        "/R",
        "/Emp3",
        r"C:\BeatTest\weesd91926.flp",
    ],
    timeout=60,
)
```

This is what the app will use: one project per command, each with its own timeout.

### Lessons learned along the way

- Python runs the **saved** file, not what's on screen. Save before running, or turn on Auto Save.
- Put `r` in front of Windows paths (`r"C:\..."`) so backslashes aren't read as special characters like `\n`.

## Part 3: Reading project files

### PyFLP: doesn't work

Code: `read_test.py`

PyFLP has not been updated in 3 years, so it does not run on the current Python version I am using. It crashed with the same `EventEnum` error on Python 3.14 and 3.13, before reading anything from the file. It might run on 3.12, but that's the oldest Python still getting security fixes, so building on it would get worse every year. So we pivoted and tried flpdiff instead.

### flpdiff: works

flpdiff is a standalone program (download from its GitHub, saved in `tools/`), so it doesn't need any Python setup.

```powershell
.\tools\flpdiff.exe info C:\BeatTest\dke101423.flp
```

Output for one project:
```
FL Studio 21.0.3.3517 | 97.0 BPM | 4/4 | PPQ 96
Channels: 9 (5 instruments, 4 samplers)
Patterns: 9
Mixer: 127 active inserts, 9 effect slots
Arrangements: 1 (500 tracks, 96 clips)
Plugins: LABS, Vital, Fruity Parametric EQ 2
Samples: 808 - Ain't The Only That's Hard.wav, Snare - Outside.wav, Kick - Kendall Jenner.wav, Hi-Hat - Prick.wav
```

- Works on projects saved in FL 21 and FL 2024.
- BPM, plugins, and sample names are exactly what the app needs. Sample names like "808 - Ain't The Only That's Hard" tell you a lot about a beat at a glance.
- Mixer insert and track counts look like FL's empty defaults, not what I actually used, so the app shouldn't show them.
- `--format json` gives the same info in a format code can read.

### Calling flpdiff from Python

Code: `read_test.py`

flpdiff is a separate program, not a Python library, so it can't be imported. Python runs it with `subprocess.run`, like FL, and reads what it prints.

```python
result = subprocess.run(
    [r"tools\flpdiff.exe", "info", r"C:\BeatTest\weesd91926.flp", "--format", "json"],
    capture_output=True, text=True, timeout=60,
)
data = json.loads(result.stdout)
```

- `capture_output=True` saves what flpdiff prints instead of showing it. `text=True` gives it back as text.
- `result.stdout` is the normal output (the JSON), `result.stderr` is error messages, `result.returncode` is 0 for success and 2 for an error.
- `json.loads` turns the JSON text into a Python dictionary. `data.keys()` lists the top-level sections.
- `--format` and `json` have to be **two separate items** in the list. `"--format=json"` failed with a usage message and return code 2. Printing `stderr` and the return code showed exactly what was wrong.

### What's in the JSON

Top-level sections: `_type`, `arrangements`, `channels`, `metadata`, `mixer`, `opaque_events`, `patterns`, `score_log`

- **`metadata`** has the useful project info:
  - `tempo`: the BPM (144 for this project)
  - `version`: FL version that last saved it (24.2.2, so FL 2024 is confirmed)
  - `created_on`: the date the project was made. Better than the file's modified date, which changes every save.
  - `time_spent`: how long I worked on the project, in seconds (about 54 minutes for this one)
  - `title`, `artists`, `genre`: empty unless filled in through FL's project info
- **`channels`**: a list with one entry per row in the Channel Rack (see below).
- **`patterns`**: every note in every pattern, with its key, velocity, position, and length. This is why the JSON is so long.
- **`mixer`**: mostly empty defaults (`"plugin": null` in every slot), so not useful.

To get a value, chain square brackets: `data["metadata"]["tempo"]`. Some values are one level deeper than expected: `data["metadata"]["time_spent"]["seconds"]`, `data["metadata"]["created_on"]["iso"]`.

### Channels

`data["channels"]` is a **list**, one item per row in the Channel Rack, in order. `data["channels"][0]` is the first row. Each channel is a dictionary:

| Field | In FL, it's... |
|---|---|
| `name` | The label on the channel button |
| `kind` | `instrument` (a plugin makes the sound) or sampler (plays an audio file) |
| `plugin` | The plugin loaded in the channel, with `name` and `vendor`. `None` if there's no plugin. |
| `sample_path` | For samplers, where the audio file lives. It's a dictionary, and the path text is in `["value"]`. |
| `color` | The channel button's color |
| `volume`, `pan`, `muted` | The channel's knobs and on/off light |
| `target_insert` | The mixer track it's routed to |

Loop through every channel, showing the plugin if there is one, otherwise the sample:

```python
for channel in data["channels"]:
    if channel["plugin"] is not None:
        print(channel["name"], channel["plugin"]["name"])
    else:
        print(channel["name"], Path(channel["sample_path"]["value"]).stem)
```

- In this project, only 1 of 12 channels had a plugin (Splice INSTRUMENT). The rest were samples, so sample names say more about this beat than plugin names.
- Channel names are often already the sample name, like "Kick - Those Dimples On Her Back," so showing both would repeat info.
- Errors I hit and what they meant:
  - `KeyError`: no field with that name at that level. The field was one level deeper.
  - `TypeError ... not 'dict'`: `sample_path` is a dictionary, not the path text. Needed `["value"]`.
  - Using brackets on `None` crashes, so check `is not None` first.
- `pathlib.Path` pulls pieces out of a file path: `.name` (file name), `.stem` (file name without .wav), `.parent.name` (folder it's in), `.parts` (every folder from the top down).
- The download is about 115 MB because it bundles its own runtime.

## What this means for the app

- **Exporting works.** The core idea is possible.
- **Export one project at a time, each with its own timeout.** One timeout for a whole folder doesn't scale. This way a stuck project only affects itself, and the app can mark it "needs attention" and move on.
- **Check that the MP3 exists** before marking a project done. FL finishing doesn't mean it exported.
- **The missing-plugin popup stops exports until someone clicks OK.** This is the biggest problem. Options:
  - Look for an FL setting that turns off missing-plugin warnings (not sure one exists)
  - Accept it and tell users FL may ask about missing plugins during setup
  - Use the per-project timeout: if a project takes too long, close FL, mark it "needs attention," and move on
  - Auto-click the popup with a Windows automation library (fragile, last resort)
- **FL has to be closed for exports to work.** Producers usually have FL open, so the app needs to detect whether FL is running, then either ask the user to close it or wait until they do.
- **The FL window pops up during exports.** Users will see it, so it's a UX question to come back to.
- **MP3s land next to the projects,** so the app knows where to find them. Still need to decide whether they stay there.
- **About 20 seconds per long project** means 300 projects could take 1.5 to 2 hours the first time. Fine as a one-time setup if the app shows progress. After that, only new or changed projects need exporting, which the app can tell from each file's modified date.
- **Use flpdiff to read project info,** called from Python with subprocess, the same way as FL.
- **flpdiff adds about 115 MB** to the app's download size if it ships with it.
- **Use `created_on` for the date a beat was made,** not the file's modified date.
- **`time_spent` could be a feature:** sort by time spent, so the beats I worked on most come to the top. Those are probably the best ideas.
- **Sample paths are available,** so the app can show which samples and kits a beat uses.
- **Open question, the kit name:** the kit is a folder in the sample's path, but counting up from the file is inconsistent because some kits use subfolders (like `Kicks`). Counting down from a kits folder might work, but only if kits live in one place, and samples from Splice, FL packs, or my own recordings live elsewhere. Decide when designing the library view.
- **Idea for later:** since every note is in the file, the app could guess a beat's musical key from its MIDI notes, with no audio analysis. Wouldn't work for beats built mostly from audio samples. Not v1.

## Open questions / next steps

- [x] Test exporting a single project instead of a whole folder
- [x] Call flpdiff from Python and read its JSON output
- [x] Print tempo, time spent, and created date from `metadata`
- [x] Look inside `channels` to find plugin and sample names
- [ ] Decide which fields the app uses (Phase 3, when designing the library view)
- [ ] Decide how to show the kit name (Phase 3)
- [ ] Check FL's settings for a way to turn off missing-plugin warnings
