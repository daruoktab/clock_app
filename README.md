# Digital Clock App

A beautiful digital clock application with ASCII art display, multiple themes, and world time zones.

![Digital Clock App](https://img.shields.io/badge/Clock-Digital-blue) ![GitHub Pages](https://img.shields.io/badge/Deployed-GitHub%20Pages-green)

## 🌟 Features

- **Large ASCII Art Display**: Beautiful monospace font clock display
- **Multiple Themes**: Neon, Classic, Matrix, and Cyberpunk themes
- **World Time Zones**: Shows time for New York, London, Tokyo, Sydney, and Dubai
- **12/24 Hour Format**: Toggle between time formats
- **Responsive Design**: Works on desktop and mobile devices
- **Keyboard Shortcuts**: Quick navigation with hotkeys
- **Real-time Updates**: Updates every second

## 🎮 Controls

### Web Version
- **T**: Toggle Theme (Neon → Classic → Matrix → Cyberpunk)
- **F**: Toggle Format (12H ↔ 24H)
- **S**: Toggle Seconds display
- **Q**: Quit (with confirmation)

### Python Terminal Version
Same controls as above, plus runs in your terminal!

## 🚀 Deployment

### GitHub Pages (Web Version)

1. **Enable GitHub Pages**:
   - Go to your repository settings
   - Navigate to "Pages" section
   - Select "GitHub Actions" as the source

2. **Automatic Deployment**:
   - The GitHub Actions workflow will automatically deploy your app
   - Every push to `main` or `master` branch triggers a new deployment
   - Your app will be available at: `https://yourusername.github.io/your-repo-name`

3. **Manual Deploy** (if needed):
   ```bash
   git add .
   git commit -m "Deploy clock app"
   git push origin main
   ```

### Running Locally

#### Web Version
1. Clone the repository
2. Open `index.html` in a web browser
3. Or serve with a local server:
   ```bash
   python -m http.server 8000
   # Then visit http://localhost:8000
   ```

#### Python Terminal Version
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python digital_clock.py
   ```

## 📁 Project Structure

```
clock_app/
├── index.html          # Web app HTML
├── style.css           # Web app styles
├── script.js           # Web app JavaScript
├── digital_clock.py    # Python terminal version
├── requirements.txt    # Python dependencies
├── .github/
│   └── workflows/
│       └── deploy.yml  # GitHub Actions deployment
└── README.md          # This file
```

## 🎨 Themes

- **Neon**: Cyan colors with a futuristic feel
- **Classic**: Gold/amber retro terminal style
- **Matrix**: Green matrix-inspired theme
- **Cyberpunk**: Magenta cyberpunk aesthetic

## 🌍 World Time Zones

The app displays current time for:
- 🗽 New York (America/New_York)
- 🏰 London (Europe/London)
- 🗾 Tokyo (Asia/Tokyo)
- 🇦🇺 Sydney (Australia/Sydney)
- 🏜️ Dubai (Asia/Dubai)

## 🛠️ Technologies

### Web Version
- HTML5
- CSS3 (with CSS Grid and Flexbox)
- Vanilla JavaScript
- JetBrains Mono font
- GitHub Actions for deployment

### Python Version
- Python 3.7+
- Textual (Terminal UI framework)
- pytz (Timezone handling)

## 📱 Responsive Design

The web version is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones
- Various screen sizes

## 🔧 Customization

You can easily customize:
- **Colors**: Edit CSS custom properties in `style.css`
- **Time Zones**: Modify the timezone list in `script.js`
- **ASCII Art**: Update the `ASCII_DIGITS` object for custom characters
- **Themes**: Add new themes by extending the CSS classes

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test both web and Python versions
5. Submit a pull request

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Issues](../../issues) page
2. Create a new issue if needed
3. Include details about your environment and the problem

---

**Enjoy your new digital clock! ⏰**
