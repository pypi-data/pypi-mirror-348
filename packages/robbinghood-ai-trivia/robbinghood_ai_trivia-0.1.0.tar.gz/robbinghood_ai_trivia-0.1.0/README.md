# RobbingHood: an ai trivia assistant. 

Bottom of this readme contains a couple feature suggestions + ways to expand this for anyone coming across this. Would also appreciate a github star if you're reading this :)

Get search grounded, up-to-date, accurate responses for any multiple choice trivia question within seconds (less than 3 on average). It combines the power of multiple AI models to give you the best possible answer under any timed based trivia game.

## Features

- **Real-time capture and analysis**: Point your camera at the question and get instant results
- **Triple-check mode**: Cross-references answers from three different AI models:
  - OpenAI's GPT-4-Turbo
  - Perplexity's Sonar Pro
  - Perplexity's Sonar
- **Continuous capture**: Keep your camera running for seamless question-to-question transitions
- **Multi-camera support**: Select from available webcams on your device
- **On-screen results**: View answers directly in the camera feed

## Technical Overview

This application demonstrates several software engineering principles and technologies:

- **Clean Architecture**: Separation of concerns with distinct layers for UI, business logic, and data
- **SOLID Principles**: Single responsibility, dependency injection, and interface segregation
- **Concurrent Processing**: Parallel API calls using ThreadPoolExecutor for optimal performance
- **Real-time Computer Vision**: OpenCV integration for camera feeds and image processing
- **Cloud AI Integration**: Multiple AI service APIs orchestrated in a single application

### Architecture

```
┌─────────────┐     ┌───────────────┐     ┌──────────────┐
│     UI      │────▶│  Application  │────▶│ AI Services  │
│  (OpenCV)   │◀────│     Core      │◀────│ (API Calls)  │
└─────────────┘     └───────────────┘     └──────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │     OCR      │
                    │   Services   │
                    └──────────────┘
```


## Technologies Used

- **Python 3.8+**: Core programming language
- **OpenCV**: Camera interfacing and image processing
- **Google Cloud Vision API**: Optical Character Recognition
- **API Integrations**: OpenAI API, Perplexity API
- **Concurrent Processing**: Python's ThreadPoolExecutor
- **Environment Management**: python-dotenv for configuration

## Code Structure

```
robbinhood/
├── main.py                 # Entry point and application bootstrap
├── config.py               # Configuration management
├── camera/                 # Camera abstraction layer
│   ├── __init__.py
│   └── camera_manager.py   # Camera operations and frame capture
├── ocr/                    # Text extraction services
│   ├── __init__.py
│   └── ocr_processor.py    # OCR processing with Google Vision
├── ai/                     # AI model interfaces
│   ├── __init__.py
│   ├── base_processor.py   # Abstract base class for AI models
│   ├── perplexity.py       # Perplexity API integration
│   └── gpt4.py             # OpenAI GPT-4 integration
├── ui/                     # User interface components
│   ├── __init__.py
│   ├── display.py          # Display management
│   └── renderer.py         # Text and overlay rendering
└── core/                   # Core application logic
    ├── __init__.py
    └── app.py              # Main application workflows
```

### Design Patterns Used

- **Factory Pattern**: For creating AI processors
- **Strategy Pattern**: Different AI models implement the same interface
- **Dependency Injection**: Components receive their dependencies
- **Observer Pattern**: UI updated as results become available

## Requirements

- Python 3.8+
- Webcam
- API keys (set as environment variables):
  - `PERPLEXITY_API_KEY`
  - `OPENAI_API_KEY`
  - `GOOGLE_CREDENTIALS_PATH` (path to your Google Cloud Vision API JSON credentials file)

## Installation

### Option 1: Install from PyPI (Recommended)

```bash
pip install robbinghood-ai-trivia
```

That's it! You can now run the application using `robbinhood-cam`.

### Option 2: Install from Source

1. Clone the repository:
```bash 
git clone https://github.com/vikvang/robbinghood.git
cd robbinghood
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install the application and its dependencies:
```bash
pip install -e .  # The '-e' makes it an editable install
```

4. Set up your API keys:
   Ensure the following environment variables are set in your shell or a `.env` file 
   (if using a `.env` file, ensure your Python script loads it, e.g., using `python-dotenv` 
   which is already a dependency; the application should handle this if `Config()` loads dotenv):
   
   ```
   PERPLEXITY_API_KEY=your_perplexity_api_key
   OPENAI_API_KEY=your_openai_api_key
   GOOGLE_CREDENTIALS_PATH=path/to/your/google_credentials.json
   ```

5. Set up Google Cloud Vision API:
   - Create a project in the [Google Cloud Console](https://console.cloud.google.com/)
   - Enable the Vision API
   - Create a service account and download the JSON credentials file
   - Set `GOOGLE_CREDENTIALS_PATH` environment variable to the path of this file.

## Usage

After installation, run the program from your terminal:
```bash
robbinhood-cam
```

This will launch the application, starting your camera. 
- The application runs in **Triple Check Mode**, querying GPT-4, Perplexity Sonar Pro, and Perplexity Sonar for each question.
- If you have multiple cameras, you might be prompted to select one, or you can specify one using the `--camera_index` argument (use `robbinhood-cam --list_cameras` to see available camera indices).

Inside the application window:
- Press **SPACE** to capture the current camera frame for analysis.
- Press **ESC** to return to the main menu (where you can change cameras or exit).

From the main menu in the application (which appears in the terminal where you launched `robbinhood-cam`):
- Choose "Start Triple Check Mode" to begin or resume camera capture.
- Choose "Change Camera" to select a different camera source.
- Choose "Exit" to close the application.

## Performance Considerations (i tried implementing the following but could be improved)

- **Parallel Processing**: AI model requests run concurrently for maximum speed
- **Non-blocking UI**: User interface remains responsive during processing
- **Optimized OCR**: Google Vision API provides high-quality text extraction
- **Memory Management**: Temporary images are properly cleaned up

## Extending the Application (feature suggestions open to anyone to build on top of this)

The modular architecture makes it easy to:

- Add new AI models by implementing the BaseAIProcessor interface
- Support alternative OCR engines by creating new OCR processor classes
- Create custom UI visualizations by extending the renderer
- Add new processing modes to the application core
