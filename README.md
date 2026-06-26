# 🏛️ AI Copilot for Panchayat Governance

A comprehensive AI-powered government portal designed for Indian citizens to access government schemes, submit applications with voice support, and receive instant assistance in multiple languages.

## 🌟 Features

### 🎤 Voice-Enabled Application Forms
- Voice input for all form fields
- Speak instead of typing
- Real-time speech-to-text conversion
- Support for Indian English accent

### 🌐 Multi-Language Support
- 22 Official Indian languages supported
- Voice-based language selection
- Complete UI translation
- Language auto-detection in AI assistant

### 🤖 AI Assistant
- Intelligent chatbot for scheme queries
- Automatic language detection
- Context-aware responses
- Real-time assistance

### 📄 PDF Receipt Generation
- Automatic PDF generation on application submission
- Professional government-style receipts
- Downloadable and viewable in browser
- Includes all application details

### 🔐 Secure Authentication
- Aadhaar-based authentication
- JWT token implementation
- Password encryption with bcrypt
- Secure API endpoints

### 📱 Responsive Design
- Mobile-friendly interface
- Modern UI with gradient backgrounds
- Smooth animations
- Professional government portal styling

## 🛠️ Tech Stack

### Frontend
- HTML5, CSS3, JavaScript
- Speech Recognition API
- Font Awesome Icons
- Responsive Design

### Backend
- Node.js
- Express.js
- MongoDB
- JWT Authentication
- Multer (File Upload)
- PDFKit (PDF Generation)

## 📁 Project Structure

```
SAHAYAKAI/
├── src/                          # Source code
│   ├── agents/                   # AI agents
│   │   ├── chat_agent.py
│   │   ├── scheme_agent.py
│   │   ├── knowledge_agent.py
│   │   └── router.py
│   ├── core/                     # Core functionality
│   │   ├── ai_engine.py
│   │   ├── orchestrator.py
│   │   └── prompts.py
│   └── services/                 # Services
│       ├── ai_service.py
│       └── knowledge_loader.py
├── knowledge_base/               # Scheme data
│   └── schemes/
│       └── pm_awas.json
├── notebooks/                    # Jupyter notebooks
│   ├── 01_Project_Setup.ipynb
│   ├── 02_Requirement_Analysis.ipynb
│   ├── 03_System_Architecture.ipynb
│   └── 05_AI_Copilot_Core.ipynb
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 14+
- MongoDB
- Modern web browser with Speech Recognition support

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/prince1205-code/AI-COPILOT-FOR-PANCHAYAT-GOVERNANCE-.git
cd AI-COPILOT-FOR-PANCHAYAT-GOVERNANCE-
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
Create `.env` file:
```env
MONGODB_URI=mongodb://localhost:27017/panchayat_db
JWT_SECRET=your_jwt_secret_key
PORT=5000
```

4. **Start MongoDB**
```bash
mongod
```

5. **Run the application**
```bash
python src/core/ai_engine.py
```

## 📚 Government Schemes Covered

- **Pradhan Mantri Awas Yojana** - Housing for all
- **PM-KISAN** - Direct income support for farmers
- **NREGA** - Rural employment guarantee
- **Ayushman Bharat** - Healthcare coverage
- **Sukanya Samriddhi Yojana** - Girl child welfare
- **Atal Pension Yojana** - Pension scheme

## 🎯 Key Functionalities

### Application Workflow
1. User logs in with Aadhaar number
2. Selects government scheme
3. Fills 3-step form (Personal, Address, Financial)
4. Uses voice input for convenience
5. Submits application
6. Views confirmation page with all details
7. PDF receipt auto-downloads
8. Can view PDF in browser

### AI Assistant Workflow
1. User speaks or types in any language
2. AI detects language automatically
3. Website switches to detected language
4. Provides scheme information
5. Answers queries in user's language

## 🔒 Security Features

- Password hashing with bcrypt
- JWT token-based authentication
- Secure API endpoints
- Input validation
- XSS protection
- CORS configuration

## 📱 Supported Languages

Hindi, Bengali, Tamil, Telugu, Gujarati, Marathi, Kannada, Malayalam, Punjabi, Odia, Urdu, Sanskrit, Assamese, Konkani, Manipuri, Bodo, Dogri, Kashmiri, Maithili, Nepali, Santali, Sindhi

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Developer

**Prince Kumar**
- GitHub: [@prince1205-code](https://github.com/prince1205-code)

## 📞 Support

For support and queries, please open an issue in the GitHub repository.

---

**Made with ❤️ for Digital India Initiative**
