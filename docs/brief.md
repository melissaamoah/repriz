# Repriz

## Problem

My beats are labelled by some random name and the date I made them, so nothing tells me what a beat sounds like unless I open the project. To find something, I either open files at random or try to remember what I named the beat I'm looking for.

## Who it's for

FL Studio producers with a projects folder full of beats, finished and unfinished. I'm building it for myself first, with the goal of releasing it for public use.

## Competitors and how this is different

- **Offtop:** a library for your beats, demos, and samples with tags and auto BPM/key detection. But you have to export an MP3 or WAV and upload every beat yourself, so unfinished ideas never make it in. The free plan caps uploads at 100 files.
- **Sortio:** renames and reorganizes files based on their names, so it only works if your files are already named well. Mine aren't, which is the whole problem.

**Repriz in one line:** like Offtop, but you don't upload anything. It reads straight from your FL projects folder, finished or not.

## v1 goal

Point the app at your projects folder, and hear, open, or send any beat without exporting anything by hand.

Three things the app does:
1. **Listen:** hear any project without opening FL
2. **Work on it:** one click to open it in FL
3. **Send it off:** get an MP3 to an artist

## How it works

1. The app has FL Studio export an MP3 of each project in the background using FL's command-line export. No clicking through the export menu.
2. It reads info straight out of each .flp file, like BPM and the plugins and samples used, using a tool called flpdiff.
3. It saves everything in a small local database so the library loads fast and is searchable.

Built with Electron and TypeScript.

## v1 features

- Pick your projects folder
- Generate an MP3 for every project, with a progress bar, skipping projects that fail
- Library list: name, date, BPM, main instruments and samples
- Play any beat in a persistent player
- Add your own tags (genre, mood, anything) and filter by tags, BPM, and date
- Open in FL Studio
- Send: drag the MP3 out of the app, or show it in its folder

## Not in v1

- Auto-rendering every time you save
- Key detection
- AI genre and mood tagging
- Share links and cloud storage
- Mobile app
- Mac support

## Open questions

- How should the app handle the missing-plugin popup during batch exports? (see Spike 1)
- FL has to be closed for exports to work. Does the app ask the user to close it, or wait until they do?
- Should MP3s stay next to the projects or move into the app's own folder?
