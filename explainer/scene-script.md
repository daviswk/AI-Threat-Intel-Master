# Assurance Engine explainer: scene script

Written for generated visuals, so it describes the app instead of pointing at
buttons. 26 scenes of about 10 seconds each, roughly 3.5 minutes, 16:9.

## Style note (paste with the script)

Flat 2D motion graphics. Dark navy background with a faint blueprint dot grid.
Cyan accent, amber for highlights, green for "passed". Simple geometric
figures and icons, no photoreal people. Keep on-screen text to short labels of
one to three words; do not try to draw readable app screens. One calm narrator.

## Narration (paste this part as the script)

1. This is the Assurance Engine: a twelve-module course where you learn to test security, privacy and AI controls by actually testing them.
2. You play the second line: the independent tester. You write the test procedures and the findings yourself.
3. Claude is your tutor. It teaches by asking questions, and later plays a skeptical staff engineer who pushes back on your work.
4. Three helper agents work out of sight. One builds each lab system. One attacks it. One grades your work without ever seeing the conversation.
5. The twelve modules form a chain. Each one produces something the next one needs, so nothing is taught twice.
6. Every module runs the same loop: pre-flight, then incubation, ingestion, lab, heuristics, and a gate.
7. Why this way? Because you struggle first. Evidence lands in front of you before any teaching.
8. Then you read, then you test a real system with code, and at the end you defend your finding. Each module has a fixed time box.
9. You work in two windows. Claude Code is the conversation: the teaching, the lab, the gate.
10. Mission Control, the web app, is your desk. You see where you are, read, write your own files, and run tests.
11. One file records where you are. Only Claude Code changes it. The app just watches.
12. Mission Control has three views. The Campaign Map shows all twelve modules and which one is live.
13. The Active Room is where the work happens: a briefing on the left, your workbench, and the test harness.
14. At the top of the room is a banner. It always says what comes next, and where: in the app, or in Claude Code.
15. The Arsenal collects what you keep: your heuristics, flashcards and portfolio pieces.
16. Here is one module, start to finish, using a toy example: a bakery that must escalate any warm fridge reading within thirty minutes.
17. Start every session by typing slash sync down in Claude Code. In pre-flight, Claude verifies the sources. There is nothing for you to do yet.
18. Incubation. You get two evidence packages that look almost identical. Only one is sound. You write your diagnosis cold, before any teaching.
19. Ingestion. Claude teaches the new ideas by question, tied to what your first attempt got right and what it missed.
20. The lab. A builder agent creates the system. A red team agent attacks it. Then you write a test procedure in plain words.
21. Claude helps turn your procedure into code, and you run it. A green test means your procedure is sound, not that the control passed.
22. The verdict: five warm readings were escalated hours late. You write one finding that says what must be true, and never designs the fix.
23. Heuristics. You boil the lesson down to a rule: if a summary says one hundred percent, recompute it from the rows.
24. The gate. An edge case question, pushback from the staff engineer, four versions of your finding, and an isolated grader.
25. When all four checks pass, the module is complete and the next one unlocks. End the session with slash sync up.
26. That is the whole loop. Sync down. Open Mission Control. Read the banner. Do what it says, where it says. Sync up.

## Visual per scene

| # | Picture |
|---|---|
| 1 | Twelve numbered tiles light up one by one on the grid |
| 2 | One figure steps forward holding a clipboard; a "2nd line" label |
| 3 | A chat bubble asking a question; it turns into a figure with folded arms |
| 4 | Three small robots behind a curtain: one builds, one pokes, one stamps |
| 5 | An arrow carries a document from tile 1 to tile 2, then onward |
| 6 | Six stations on a loop track, each lighting in turn |
| 7 | A folder of evidence drops onto a desk before a book does |
| 8 | Book, then code brackets, then a figure at a podium; a timer beside them |
| 9 | Two windows side by side; the left one fills with chat bubbles |
| 10 | The right window becomes a desk with a map, a notepad and a play button |
| 11 | A single file icon between the windows; one writes to it, one watches |
| 12 | A map of twelve nodes, one glowing |
| 13 | A room in three panes: reading, writing, a test console |
| 14 | A banner unrolls across the top with an arrow pointing left or right |
| 15 | A shelf collecting cards, a rulebook and a framed write-up |
| 16 | A bakery fridge with a thermometer and a 30-minute timer |
| 17 | A sync arrow pulling files down; a checklist being ticked by a robot |
| 18 | Two near-identical folders, A and B; a question mark between them |
| 19 | Question marks turning into light bulbs over an open book |
| 20 | One robot builds a fridge log, another tampers with it, the figure writes steps |
| 21 | Written steps turn into code; a green tick appears beside a magnifying glass |
| 22 | Five amber clocks on a table of rows; a five-part form being filled |
| 23 | A card stamped "If... then verify..." slides into a rulebook |
| 24 | Four doors in a row; the figure passes each one |
| 25 | Tile 1 turns green, tile 2 lights up; a sync arrow pushing files up |
| 26 | The loop in five icons: sync down, app, banner, do, sync up |
