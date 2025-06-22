// Digital Clock App JavaScript

// ASCII art for digits (same as Python version)
const ASCII_DIGITS = {
    '0': [" ##### ", "#     #", "#     #", "#     #", " ##### "],
    '1': ["  #    ", " ##    ", "  #    ", "  #    ", " ###   "],
    '2': [" ##### ", "     # ", " ##### ", "#     ", " ##### "],
    '3': [" ##### ", "     # ", "  #### ", "     # ", " ##### "],
    '4': ["#   #  ", "#   #  ", "#######", "    #  ", "    #  "],
    '5': [" ##### ", "#      ", " ####  ", "     # ", " ##### "],
    '6': [" ##### ", "#      ", " ##### ", "#     #", " ##### "],
    '7': [" ##### ", "    #  ", "   #   ", "  #    ", " #     "],
    '8': [" ##### ", "#     #", " ##### ", "#     #", " ##### "],
    '9': [" ##### ", "#     #", " ##### ", "     # ", " ##### "],
    ':': [" ", "•", " ", "•", " "],
    'A': ["  ###  ", " #   # ", " ##### ", "#     #", "#     #"],
    'P': [" ####  ", "#    # ", " ####  ", "#      ", "#      "],
    'M': ["#     #", "##   ##", "# # # #", "#  #  #", "#     #"],
    ' ': ["       ", "       ", "       ", "       ", "       "],
};

// Global state
let currentTheme = 'neon';
let timeFormat = 24; // 24 or 12
let showSeconds = true;
const startTime = Date.now();

// Theme cycle
const themes = ['neon', 'classic', 'matrix', 'cyberpunk'];

function createBigTime(timeStr) {
    const outputLines = ["", "", "", "", ""];
    
    for (const char of timeStr.toUpperCase()) {
        const pattern = ASCII_DIGITS[char] || ASCII_DIGITS[' '];
        for (let i = 0; i < 5; i++) {
            outputLines[i] += pattern[i] + " ";
        }
    }
    
    return outputLines.join('\n');
}

function formatTime(date, format24h, includeSeconds) {
    let hours = date.getHours();
    const minutes = date.getMinutes();
    const seconds = date.getSeconds();
    let ampm = '';
    
    if (!format24h) {
        ampm = hours >= 12 ? ' PM' : ' AM';
        hours = hours % 12;
        if (hours === 0) hours = 12;
    }
    
    const timeStr = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}${includeSeconds ? ':' + seconds.toString().padStart(2, '0') : ''}${ampm}`;
    return timeStr;
}

function getWeekNumber(date) {
    const firstDayOfYear = new Date(date.getFullYear(), 0, 1);
    const pastDaysOfYear = (date - firstDayOfYear) / 86400000;
    return Math.ceil((pastDaysOfYear + firstDayOfYear.getDay() + 1) / 7);
}

function updateDisplay() {
    const now = new Date();
    
    // Main time display
    const timeStr = formatTime(now, timeFormat === 24, showSeconds);
    const bigTime = createBigTime(timeStr);
    document.getElementById('asciiClock').textContent = bigTime;
    
    // Date info
    const dateOptions = { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    };
    const dateStr = now.toLocaleDateString('en-US', dateOptions);
    const weekNum = getWeekNumber(now);
    document.getElementById('dateInfo').textContent = `📅 ${dateStr} • Week ${weekNum}`;
    
    // World times
    updateWorldTimes();
    
    // Status bar
    const uptime = Math.floor((Date.now() - startTime) / 1000);
    const hours = Math.floor(uptime / 3600);
    const minutes = Math.floor((uptime % 3600) / 60);
    const seconds = uptime % 60;
    const uptimeStr = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    
    const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    const status = `Theme: ${currentTheme.toUpperCase()} | Format: ${timeFormat}H | Uptime: ${uptimeStr} | ${timezone}`;
    document.getElementById('statusBar').textContent = status;
}

function updateWorldTimes() {
    const timezones = {
        'worldNY': { timezone: 'America/New_York', flag: '🗽', city: 'New York' },
        'worldLondon': { timezone: 'Europe/London', flag: '🏰', city: 'London' },
        'worldTokyo': { timezone: 'Asia/Tokyo', flag: '🗾', city: 'Tokyo' },
        'worldSydney': { timezone: 'Australia/Sydney', flag: '🇦🇺', city: 'Sydney' },
        'worldDubai': { timezone: 'Asia/Dubai', flag: '🏜️', city: 'Dubai' }
    };
      for (const [elementId, info] of Object.entries(timezones)) {
        try {
            const now = new Date();
            const timeInZone = new Intl.DateTimeFormat('en-US', {
                timeZone: info.timezone,
                hour: '2-digit',
                minute: '2-digit',
                hour12: false
            }).format(now);
            
            document.getElementById(elementId).textContent = 
                `${info.flag} ${info.city.padEnd(8)} ${timeInZone}`;
        } catch (_error) {
            document.getElementById(elementId).textContent = 
                `${info.flag} ${info.city.padEnd(8)} --:--`;
        }
    }
}

function toggleTheme() {
    const currentIndex = themes.indexOf(currentTheme);
    currentTheme = themes[(currentIndex + 1) % themes.length];
    
    const container = document.getElementById('clockContainer');
    container.className = `clock-container ${currentTheme}`;
}

function toggleFormat() {
    timeFormat = timeFormat === 24 ? 12 : 24;
}

function toggleSeconds() {
    showSeconds = !showSeconds;
}

// Keyboard bindings
document.addEventListener('keydown', function(event) {
    switch(event.key.toLowerCase()) {
        case 't':
            toggleTheme();
            break;
        case 'f':
            toggleFormat();
            break;
        case 's':
            toggleSeconds();
            break;        case 'q':
            if (confirm('Are you sure you want to close the clock?')) {
                globalThis.close();
            }
            break;
    }
});

// Initialize the clock
document.addEventListener('DOMContentLoaded', function() {
    updateDisplay();
    setInterval(updateDisplay, 1000);
});

// Handle visibility change to save resources
document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'visible') {
        updateDisplay();
    }
});
