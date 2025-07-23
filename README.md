# IcosSearchSystem-2 🔍

A privacy-focused, intelligent search application built on Whoogle Search with enhanced features and modern UI improvements.

## ✨ Features

- **Privacy-First Search**: No tracking, no ads, no JavaScript required
- **Modern UI**: Clean, responsive design with dark/light theme support
- **Advanced Settings**: Modal-based configuration with hamburger menu
- **Mobile Optimized**: Responsive design for all device sizes
- **Fast Performance**: Optimized for speed and efficiency

## 🚀 Quick Start

### Deploy on Replit
1. Fork this repository
2. Click the "Run" button in Replit
3. Your search engine will be available at your Replit URL

### Local Development
```bash
# Clone the repository
git clone https://github.com/Rohithprovide/IcosSearchSystem-2.git
cd IcosSearchSystem-2

# Run the application
python main.py
```

The application will be available at `http://localhost:5000`

## 🏗️ Architecture

### Backend
- **Flask**: Web framework and routing
- **BeautifulSoup4**: HTML parsing and result filtering
- **Requests**: HTTP client for search queries
- **Cryptography**: Session encryption and security

### Frontend
- **Vanilla JavaScript**: Enhanced search functionality
- **Responsive CSS**: Modern styling with theme support
- **Jinja2 Templates**: Server-side rendering

### Key Components
- `main.py`: Application entry point
- `whoogle-search/`: Core search engine
- `app/routes.py`: Main route handlers
- `app/filter.py`: Result filtering logic
- `app/static/`: CSS, JavaScript, and assets
- `app/templates/`: HTML templates

## 🎨 UI Enhancements

### Modern Settings Interface
- Hamburger menu with popup modal
- Theme selection (Light/Dark/System)
- Safe Search toggle
- Link behavior configuration

### Enhanced Image Search
- 6 images per row layout
- 100 images per page
- Rounded corners and hover effects
- Responsive grid design

### Navigation Improvements
- Tab hover effects with underlines
- Clear button in search bar
- Smooth animations and transitions

## 🔧 Configuration

### Environment Variables
- `WHOOGLE_RESULTS_PER_PAGE`: Number of results per page (default: 100 for images)
- `WHOOGLE_CONFIG_COUNTRY`: Default country for searches
- `WHOOGLE_CONFIG_LANGUAGE`: Default language
- `WHOOGLE_CONFIG_THEME`: Default theme (light/dark/system)

### Customization
The application supports extensive customization through:
- CSS variables for theming
- Configuration options in settings modal
- URL parameters for search preferences

## 📱 Mobile Support

Fully responsive design with:
- Touch-friendly interface
- Optimized image grid (3 columns on tablets, 2 on phones)
- Mobile-specific templates and styling
- Gesture support for navigation

## 🔒 Privacy Features

- **No Tracking**: All Google tracking removed
- **No Ads**: Clean, ad-free search results
- **No JavaScript Required**: Core functionality works without JS
- **Session Encryption**: User preferences encrypted
- **Proxy Support**: Optional Tor integration

## 📊 Performance

- **Fast Loading**: Optimized for speed
- **Efficient Filtering**: Advanced result processing
- **Responsive Design**: Smooth user experience
- **Image Optimization**: Proper sizing and loading

## 🛠️ Development

### Project Structure
```
IcosSearchSystem-2/
├── main.py                 # Application entry point
├── whoogle-search/         # Core search engine
│   └── whoogle-search/
│       ├── app/
│       │   ├── routes.py   # Route handlers
│       │   ├── filter.py   # Result filtering
│       │   ├── static/     # CSS, JS, assets
│       │   └── templates/  # HTML templates
│       └── requirements.txt
├── replit.md              # Project documentation
└── README.md              # This file
```

### Adding Features
1. Create new templates in `app/templates/`
2. Add CSS styles in `app/static/css/`
3. Implement JavaScript in `app/static/js/`
4. Add routes in `app/routes.py`
5. Update filtering logic in `app/filter.py`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is based on Whoogle Search and maintains the same open-source license.

## 🙏 Acknowledgments

- [Whoogle Search](https://github.com/benbusby/whoogle-search) - The foundation of this project
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - HTML parsing

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check the documentation in `replit.md`
- Review the troubleshooting guide in `GITHUB_PUSH_GUIDE.md`

---

**Built with ❤️ for privacy-focused search**