# PowerSave Mobile App

React Native mobile application for the PowerSave National Energy Solidarity Ecosystem.

## Features

- ✅ **Waste Wallet** - Track savings and waste fee coverage
- ✅ **Saving Sessions** - Schedule and manage energy saving sessions
- ✅ **Green Garden** - Gamification with virtual plants
- ✅ **Dashboard** - Overview of all metrics
- ✅ **Profile** - User settings and achievements

## Screenshots

> Screenshots coming soon

## Tech Stack

- **Framework:** React Native 0.72
- **Navigation:** React Navigation v6
- **State Management:** React Context API
- **HTTP Client:** Axios
- **Storage:** AsyncStorage
- **UI Components:** Custom components
- **Icons:** React Native Vector Icons

## Prerequisites

- Node.js >= 18.0.0
- npm >= 9.0.0
- React Native CLI
- Android Studio (for Android)
- Xcode (for iOS, macOS only)

## Installation

### 1. Install Dependencies

```bash
cd mobile
npm install
```

### 2. iOS Setup (macOS only)

```bash
cd ios
pod install
cd ..
```

### 3. Android Setup

Make sure you have Android Studio installed and configured.

## Running the App

### Android

```bash
npm run android
```

### iOS (macOS only)

```bash
npm run ios
```

### Development Server

```bash
npm start
```

## Project Structure

```
mobile/
├── App.js                   # Main app entry point
├── src/
│   ├── components/          # Reusable components
│   ├── screens/             # Screen components
│   │   ├── HomeScreen.js
│   │   ├── WasteWalletScreen.js
│   │   ├── SessionsScreen.js
│   │   ├── GreenGardenScreen.js
│   │   └── ProfileScreen.js
│   ├── navigation/          # Navigation configuration
│   │   └── AppNavigator.js
│   ├── context/             # React Context
│   │   └── AppContext.js
│   ├── services/            # API services
│   │   └── api.js
│   └── utils/               # Utility functions
├── assets/                  # Images, icons, fonts
└── package.json
```

## API Integration

The app connects to the PowerSave backend API:

- **Development:** `http://localhost:8000/api/v1`
- **Production:** `https://api.powersave.cy/api/v1`

### API Endpoints Used

```javascript
// Authentication
POST /auth/register
POST /auth/register-property
GET  /auth/users/{userId}

// Waste Wallet
GET  /wallet/{userId}/balance
GET  /wallet/{userId}/transactions
GET  /wallet/{userId}/coverage
POST /wallet/{userId}/donate

// Saving Sessions
POST /sessions
GET  /sessions/{sessionId}
GET  /sessions/user/{userId}
POST /sessions/{sessionId}/start
POST /sessions/{sessionId}/complete
GET  /sessions/user/{userId}/stats
```

## Screens

### 1. Home Screen

Dashboard with overview of all metrics:
- Wallet balance
- Total kWh saved
- Green Points
- Quick actions
- How it works guide

### 2. Waste Wallet Screen

Manage waste fee credits:
- Current balance display
- Coverage percentage with progress bar
- Transaction history
- Donation to solidarity fund
- Monthly coverage stats

### 3. Sessions Screen

Schedule and manage saving sessions:
- User stats (sessions, kWh, earnings, points)
- Schedule new session
- List of all sessions (scheduled, in progress, completed)
- Start/complete session actions
- Session results with rewards

### 4. Green Garden Screen

Gamification with virtual plants:
- Green Points balance
- 5×5 garden grid
- Plant catalog
- Plant and water mechanics
- Growth stages visualization

### 5. Profile Screen

User settings and information:
- Profile details
- Achievements/badges
- Settings menu
- Help & FAQ
- Logout

## State Management

### AppContext

Global state managed via React Context:

```javascript
const {
  userId,
  walletBalance,
  totalKwhSaved,
  greenPoints,
  refreshUserData
} = useApp();
```

## Styling

All screens use React Native StyleSheet with a consistent design:

- **Primary Color:** #4CAF50 (Green)
- **Secondary Color:** #2196F3 (Blue)
- **Accent Color:** #FF5722 (Orange)
- **Background:** #F5F5F5
- **Cards:** #FFFFFF with 12px border radius

## Development

### Formatting

```bash
npm run format
```

### Linting

```bash
npm run lint
```

### Testing

```bash
npm test
```

## Build for Production

### Android

```bash
cd android
./gradlew assembleRelease
# APK will be at: android/app/build/outputs/apk/release/app-release.apk
```

### iOS

```bash
# Open Xcode
open ios/PowerSave.xcworkspace
# Archive and export from Xcode
```

## Environment Variables

Create a `.env` file in the mobile directory:

```
API_BASE_URL=http://localhost:8000/api/v1
```

## Known Issues

- Push notifications not yet implemented
- Smart meter integration is mocked
- Some features are placeholders ("Coming Soon")

## Roadmap

- [ ] Push notifications (Firebase)
- [ ] Real-time smart meter integration
- [ ] Offline mode support
- [ ] Dark mode
- [ ] Multilingual support (Greek, English, Turkish, Russian)
- [ ] Social sharing features
- [ ] Advanced statistics charts
- [ ] Badge collection system
- [ ] Community leaderboards

## Contributing

1. Follow React Native best practices
2. Use functional components and hooks
3. Add PropTypes for all components
4. Write meaningful commit messages
5. Test on both iOS and Android

## License

Proprietary - PowerSave Cyprus 2025
