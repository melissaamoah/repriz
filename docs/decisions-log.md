# Decisions log

Every major decision, why I made it, and what would change my mind. Newest at the top.

<!-- Template:
## YYYY-MM-DD: Decision title
**Decision:**
**Why:**
**Alternatives considered:**
**What would make me revisit this:**
-->

## 2026-11-24: Build the app with Electron and TypeScript
**Decision:** Repriz is an Electron app, with a web-style frontend (HTML, CSS, JavaScript/TypeScript) and a Node.js backend.
**Why:** Electron ships its own copy of Chromium inside the app, so every user gets the same engine and the design looks and behaves the same on every computer. That matters because I want the app to match my Figma designs, not look generic. The interface is HTML and CSS, so I can build what I design. Frontend and backend are both TypeScript, so I'm learning one language across the whole app, and I've worked with Electron before. Node can run FL and flpdiff the same way Python's `subprocess` does, so Python is no longer required now that PyFLP is gone.
**Alternatives considered:**
- Tauri: smaller downloads, but it uses each computer's own web engine, so the design can render differently on Windows vs Mac. Its backend is Rust, which I don't know, and learning Rust and frontend at the same time is a lot for a first full app.
- PySide6 (Python + Qt): matching a modern custom design is harder, and the skills transfer less to jobs.
**What would make me revisit this:** The download gets too big. Electron is often over 100 MB on its own, and flpdiff adds about 115 MB, so Repriz could be 250 MB+. Or Electron's memory use makes the app feel heavy next to FL.

## 2026-11-23: Use flpdiff instead of PyFLP to read project files
**Decision:** Read BPM, plugins, and sample names from .flp files with flpdiff, called from Python with subprocess.
**Why:** PyFLP crashed on Python 3.14 and 3.13 before reading anything. It hasn't been updated since 2023, so it isn't keeping up with Python or FL. flpdiff read both FL 21 and FL 2024 projects correctly, and since it's a standalone program, the app can use any current Python. Details in Spike 1.
**Alternatives considered:** PyFLP on Python 3.12 (the oldest supported version, so a bad long-term bet), dawparse (no documented way to get BPM, channels, or plugins).
**What would make me revisit this:** flpdiff stops being maintained or breaks on a new FL version, or its 115 MB size becomes a problem for the app download.

## 2026-11-23: Export one project at a time, each with its own timeout
**Decision:** The app sends FL one project at a time instead of a whole folder.
**Why:** A timeout force-closes FL. One timeout for a whole folder can't fit both 3 projects and 300, and one stuck project would block everything. One at a time means a stuck project only affects itself, and the app can mark it "needs attention" and move on.
**Alternatives considered:** Exporting the whole folder in one command.
**What would make me revisit this:** Starting FL once per project turns out to be much slower than one folder export.

## 2026-11-23: Keep sharing local for v1
**Decision:** "Sending off" a beat in v1 means the MP3 is ready to drag into a DM or email, or open in its folder. No share links.
**Why:** Share links like Offtop's need accounts, cloud storage, and a server. That's basically a second app. Local sharing still solves the real need, which is getting a beat to someone quickly.
**Alternatives considered:** Cloud share links, uploading to SoundCloud or Google Drive.
**What would make me revisit this:** Users say dragging files out isn't enough, or v1 is done and stable.

## 2026-11-23: Render the full beat instead of a snippet
**Decision:** Export one full MP3 per project and use it for both previewing and sending.
**Why:** Sending a beat needs the full audio anyway, so one file covers both. The original plan rendered a short snippet 30% in and split it into weighted chunks for AI analysis, which was extra complexity for a feature that's no longer in v1.
**Alternatives considered:** Short preview clips only.
**What would make me revisit this:** Full exports take too long or use too much disk space across hundreds of projects.

## 2026-11-23: Make audio previews the core of v1
**Decision:** v1 is built around hearing your beats, not around metadata or AI tags.
**Why:** My actual problem is that I can't tell what a beat sounds like without opening it. BPM and plugin lists help a little, but only hearing it solves that. Exporting audio is also what makes this different from Offtop: Offtop needs uploads because it needs audio, and Repriz gets audio straight from the project.
**Alternatives considered:** A metadata-only v1 (BPM, plugins, dates) with previews later.
**What would make me revisit this:** Command-line exporting turns out to be too unreliable to build on.

## 2026-11-23: Read project info from the .flp file instead of AI audio analysis
**Decision:** Get BPM, instruments, and samples by reading the .flp file (originally planned with PyFLP, now flpdiff, see above). Users add genre and mood tags themselves. No AI in v1.
**Why:** The original plan exported audio so AI could listen and guess the BPM, key, genre, and mood. But the BPM is already saved in the project file, so analyzing audio to find it is like listening to a song to guess the tempo when it's written on the sheet music. Training a genre/mood model is a whole separate project, unfinished loops are hard to classify, and once users can hear a beat they can tag it in two seconds.
**Alternatives considered:** librosa/Essentia for BPM and key, a PyTorch model for genre and mood.
**What would make me revisit this:** v1 is done and users want suggested tags. AI suggestions that the user confirms could come in a later version.

## 2026-11-23: The app is a separate desktop app, not an FL extension
**Decision:** Repriz runs next to FL Studio instead of inside it.
**Why:** As far as I know, FL doesn't let outside apps add panels inside it. Its scripting is for MIDI controllers and the piano roll. Worth double-checking.
**Alternatives considered:** An FL Studio extension or plugin.
**What would make me revisit this:** Finding an official way to add a panel inside FL.
