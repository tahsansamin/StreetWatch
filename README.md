# StreetWatch 🛣️

## The Problem

Uganda's roads are facing a critical infrastructure challenge. Potholes and road damage pose significant safety risks to commuters and vehicles, yet comprehensive road surveillance remains expensive for local authorities. Traditional surveillance systems require extensive capital investment, specialized personnel, and ongoing maintenance—costs that strain municipal budgets and limit coverage across vast urban and rural areas.



## The Solution

**StreetWatch** is a community driven surveillance tools. As a road user you upload photos of road hazards you encounter which forms a map of what needs servicing to be used by authorities. By empowering citizens to report and document road damage through a simple interface, StreetWatch enables authorities to:

- 📊 **Monitor road conditions** in real-time across their jurisdiction
- 💰 **Reduce surveillance costs** through crowdsourced reporting
- 🎯 **Prioritize repairs** based on severity and frequency of reports
- 👥 **Engage communities** in civic infrastructure maintenance

Live app: https://street-watch-six.vercel.app/
Watch me use the app on the roads of Kampala : https://www.youtube.com/watch?v=fa7LzTvRdic !

## How It Works

1. **Citizens Report**: Users capture and submit photos of potholes and road damage through the mobile-friendly web interface
2. **AI Detection**: Our machine learning model automatically prevents spam uploads.
3. **Data Aggregation**: Reports are mapped and aggregated to show problem areas
4. **Authority Access**: Local authorities can access the dashboard to view all reported issues and plan maintenance

## Key Features

✅ **Real-time reporting** - Citizens can submit reports instantly with photos  
✅ **Intelligent detection** - AI-powered pothole and road damage identification  
✅ **Interactive mapping** - Visualize all reported issues on an interactive map  
✅ **Severity classification** - Automatic assessment of damage severity  
✅ **Image compression** - Optimized for low-bandwidth conditions, ensuring accessibility in areas with poor connectivity  
✅ **Cost-effective** - Eliminates need for expensive surveillance infrastructure  
✅ **Community-driven** - Transforms citizens into road monitors

## Tech Stack

### Frontend
- **React** - Modern UI framework
- **Vite** - Fast build tooling
- **JavaScript/JSX** - Dynamic interactivity
- **Interactive Maps** - Geospatial visualization

### Backend
- **Python** - Core application logic
- **ONNX** - ML model inference for pothole detection
- **FastAPI** - handles API endpoints
- **Supabase** - object storage and database services

## Project Structure

```
StreetWatch/
├── frontend/                 # React web application
│   ├── src/
│   │   ├── App.jsx          # Main application component
│   │   ├── MapView.jsx      # Interactive map interface
│   │   ├── api.js           # API communication
│   │   └── assets/          # Static assets
│   ├── package.json
│   └── vite.config.js
├── backend/                  # Python Flask/FastAPI server
│   ├── main.py              # Application entry point
│   ├── detection_pothole.py # ML detection logic
│   ├── objects.py           # Data models
│   ├── best.onnx           # Pre-trained detection model
│   └── requirements.txt      # Python dependencies
└── README.md                # This file
```

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the server:
```bash
python main.py
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```


## Contributing

We welcome contributions from the community! Whether you're fixing bugs, adding features, or improving documentation, please feel free to submit pull requests.

## Impact

By connecting communities with local authorities, StreetWatch transforms road maintenance from a top-down, expensive process into a collaborative effort. Early adoption in Uganda could serve as a model for cost-effective infrastructure monitoring across Africa and beyond.

## License

This project is open source and available under the MIT License.


---

**Building better roads, one report at a time.** 🚗✨
