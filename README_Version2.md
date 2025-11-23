# Digital Timezone Clock

A simple, accessible, single-page digital clock that displays the current time in multiple time zones. Built with plain HTML, CSS and JavaScript (no external libraries).

Features
- Live updating every second.
- Pre-populated common time zones.
- Add any IANA timezone identifier (e.g. "America/New_York", "Europe/Paris", "Asia/Tokyo").
- Remove clocks you no longer want to see.
- Toggle between 12-hour and 24-hour display.
- Responsive and keyboard accessible.

How to use
1. Open `index.html` in any modern browser (Edge, Chrome, Firefox, Safari).
2. Use the Add Time Zone input to pick from the suggestions or type a valid IANA timezone and press Add.
3. Click the clock's Remove button to remove it.
4. Toggle 12/24-hour format from the top-right switch.

Notes
- The app uses the browser's Intl API to format times. The timezone must be a valid IANA timezone identifier.
- If a timezone is invalid, you'll see an error message below the input.

Files
- index.html — markup and structure.
- styles.css — layout and styling.
- script.js — logic to update clocks, add/remove zones and toggle format.

## License

Copyright (c) 2025 Yadullah

All rights reserved.

This software and associated documentation files (the "Software") are the exclusive property of Yadullah.

Permission is hereby granted to view and use the Software for personal, non-commercial purposes only.

Restrictions:
- Redistribution, modification, sublicensing, or commercial use of the Software is strictly prohibited without prior written consent from Yadullah.
- Copying or launching derivative projects based on this Software is forbidden.
- Any unauthorized use will be subject to legal action under applicable copyright laws.

For licensing inquiries, please contact Yadullah.