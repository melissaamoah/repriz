# Roadmap

The plan from here to a released v1. This is a living doc: when a spike or test changes the plan, update it here and log the reason in the decisions log.

Each phase ends with something I can check off. Don't start a phase until the one before it is done, unless there's a clear reason.

## Phase 1: Prove the risky parts ✅

**Goal:** Know that the core idea works before designing or building anything. Details in Spike 1.

- [x] FL exports projects from code (PowerShell, then Python)
- [x] Project info can be read from .flp files (flpdiff works, PyFLP doesn't)
- [x] Export a single project instead of a whole folder
- [x] Call flpdiff from Python and read its JSON output
- [x] Pull out the fields the app needs (tempo, time spent, created date, plugins, samples)

## Phase 2: Choose how the app is built ✅

**Goal:** Pick the tools for the app's window and interface, based on research instead of guessing.

- [x] Research the options: PySide6, Electron, Tauri
- [x] Build a tiny "hello world" Electron app (in `app/`, runs with `npm start`)
- [x] Log the decision in the decisions log (Electron + TypeScript)

## Phase 3: Design v1

**Goal:** A design that matches what's actually possible and has been seen by real producers.

- [ ] Update the Figma to match the real data: BPM, plugins, samples, time spent, and created date, but no key
- [ ] Decide how to show the kit name for samples (see Spike 1 notes)
- [ ] Design the states the spike revealed: first-time setup, "FL must be closed," export progress, "needs attention"
- [ ] Show it to 3 to 5 producers and adjust

## Phase 4: Build v1 in slices

**Goal:** A working v1. Each slice works end to end before starting the next.

- [ ] Slice 1: Scan the projects folder, read each project with flpdiff, save to a database
- [ ] Slice 2: Export MP3s one project at a time, with timeouts and a status for each project
- [ ] Slice 3: Library view
- [ ] Slice 4: Player
- [ ] Slice 5: Tags and filters
- [ ] Slice 6: Open in FL, send

## Phase 5: Test and release

**Goal:** Real producers using it, and a story I can tell in interviews.

- [ ] Test with projects saved in FL 2026, since many public users will be on it
- [ ] Get it to a small group of producers and fix the top issues
- [ ] Package it so people can install it
- [ ] Write the case study and resume bullet, with real numbers (projects handled, export success rate, users)

## Later (not v1)

Auto-export on save, key detection, AI tag suggestions, share links, Mac support, letting users customize their library's look (like MySpace, a "Notion for your beats").
