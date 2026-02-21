# Voice and Language Support Feature

## Overview
This feature enables non-technical users to submit grievances using voice recordings in their regional languages. The system automatically transcribes the audio, translates it to English, and stores the original language metadata.

**Issue #291: Local Language and Voice-Based Grievance Submission**

## Features

### 1. Voice Transcription
- Support for multiple audio formats (WAV, MP3, FLAC)
- Automatic speech-to-text conversion
- Confidence scoring for transcription quality
- Manual correction workflow for low-confidence transcriptions

### 2. Multi-Language Support
The system supports the following Indian regional languages:
- Hindi (hi)
- Bengali (bn)
- Telugu (te)
- Marathi (mr)
- Tamil (ta)
- Gujarati (gu)
- Kannada (kn)
- Malayalam (ml)
- Punjabi (pa)
- Odia (or)
- Assamese (as)
- English (en)

### 3. Auto-Translation
- Automatic language detection
- Translation from regional languages to English
- Preservation of original text for reference

### 4. Confidence Scoring
- Transcription confidence scores (0-1 scale)
- Automatic flagging for manual correction when confidence < 0.7
- Transparency in transcription quality

## API Endpoints

### 1. Transcribe Voice to Text
**POST** `/api/voice/transcribe`

Transcribe an audio file to text with automatic translation.

**Request:**
- `audio_file`: Audio file (multipart/form-data)
- `preferred_language`: Language code (default: 'auto')

**Response:**
```json
{
  "original_text": "मुझे सड़क की समस्या है",
  "translated_text": "I have a road problem",
  "source_language": "hi",
  "source_language_name": "Hindi",
  "confidence": 0.85,
  "manual_correction_needed": false,
  "error": null
}
```

### 2. Translate Text
**POST** `/api/voice/translate`

Translate text from one language to another.

**Request:**
```json
{
  "text": "मुझे सड़क की समस्या है",
  "source_language": "auto",
  "target_language": "en"
}
```

**Response:**
```json
{
  "translated_text": "I have a road problem",
  "source_language": "hi",
  "source_language_name": "Hindi",
  "target_language": "en",
  "target_language_name": "English",
  "original_text": "मुझे सड़क की समस्या है",
  "error": null
}
```

### 3. Submit Voice Issue
**POST** `/api/voice/submit-issue`

Submit a grievance via voice recording.

**Request:**
- `audio_file`: Voice recording (multipart/form-data)
- `category`: Issue category (Road, Water, Garbage, etc.)
- `user_email`: User's email (optional)
- `latitude`: GPS latitude (optional)
- `longitude`: GPS longitude (optional)
- `location`: Location description (optional)
- `preferred_language`: Language code (default: 'auto')
- `manual_description`: Manual correction if needed (optional)

**Response:**
```json
{
  "id": 123,
  "message": "Voice issue submitted successfully. Transcription confidence: 85.00%",
  "action_plan": null
}
```

### 4. Get Supported Languages
**GET** `/api/voice/supported-languages`

Get list of all supported languages.

**Response:**
```json
{
  "languages": {
    "hi": "Hindi",
    "mr": "Marathi",
    "en": "English",
    ...
  },
  "total_count": 12
}
```

### 5. Get Issue Audio
**GET** `/api/voice/issue/{issue_id}/audio`

Retrieve the original audio file for a voice-submitted issue.

## Database Schema

### New Columns in `issues` Table
- `submission_type`: 'text' or 'voice'
- `original_language`: Language code (e.g., 'hi', 'mr')
- `original_text`: Original text in regional language
- `transcription_confidence`: Float (0-1) confidence score
- `manual_correction_applied`: Boolean flag
- `audio_file_path`: Path to stored audio file

## Implementation Details

### Voice Service (`voice_service.py`)
Main service class handling:
- Audio file processing
- Speech recognition using Google Speech Recognition
- Language detection using langdetect
- Translation using Google Translate
- Confidence estimation

### Router (`routers/voice.py`)
API endpoints for:
- Voice transcription
- Text translation
- Voice-based issue submission
- Language information
- Audio file retrieval

### Dependencies
```txt
SpeechRecognition     # Speech-to-text
pydub                 # Audio processing
googletrans==4.0.0rc1 # Translation
langdetect            # Language detection
indic-nlp-library     # Indian language support
```

## Usage Examples

### Frontend Integration

#### 1. Record and Submit Voice Grievance
```javascript
// Record audio using Web Audio API
const mediaRecorder = new MediaRecorder(stream);
const audioChunks = [];

mediaRecorder.ondataavailable = (event) => {
  audioChunks.push(event.data);
};

mediaRecorder.onstop = async () => {
  const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
  
  // Submit via API
  const formData = new FormData();
  formData.append('audio_file', audioBlob, 'recording.wav');
  formData.append('category', 'Road');
  formData.append('preferred_language', 'hi');
  
  const response = await fetch('/api/voice/submit-issue', {
    method: 'POST',
    body: formData
  });
  
  const result = await response.json();
  console.log('Issue created:', result.id);
};
```

#### 2. Transcribe and Preview Before Submission
```javascript
// Step 1: Transcribe audio
const formData = new FormData();
formData.append('audio_file', audioBlob);
formData.append('preferred_language', 'auto');

const transcribeResponse = await fetch('/api/voice/transcribe', {
  method: 'POST',
  body: formData
});

const transcription = await transcribeResponse.json();

// Step 2: Show preview to user
console.log('Original:', transcription.original_text);
console.log('English:', transcription.translated_text);
console.log('Confidence:', transcription.confidence);

// Step 3: Allow manual correction if needed
if (transcription.manual_correction_needed) {
  // Show text input for correction
  const correctedText = await getUserCorrection(transcription.translated_text);
  
  // Submit with correction
  const submitFormData = new FormData();
  submitFormData.append('audio_file', audioBlob);
  submitFormData.append('category', 'Road');
  submitFormData.append('manual_description', correctedText);
  
  await fetch('/api/voice/submit-issue', {
    method: 'POST',
    body: submitFormData
  });
}
```

## On-Ground Impact

### Increased Accessibility
- **Elderly citizens**: Can report issues without typing
- **Rural users**: Can use their regional language
- **Low literacy**: Voice removes typing barriers

### Better Coverage
- More diverse user base
- Increased rural adoption
- Better representation of non-English speakers

### Data Preservation
- Original language context preserved
- Cultural nuances maintained
- Audit trail with audio recordings

## Testing

### Manual Testing
1. Record a voice message in Hindi/Marathi
2. Submit via `/api/voice/transcribe`
3. Verify transcription and translation
4. Check confidence score
5. Submit as issue via `/api/voice/submit-issue`

### Sample Audio Files
Create test recordings with:
- Clear speech (high confidence)
- Noisy background (low confidence)
- Different languages (Hindi, Marathi, English)
- Different accents

## Future Enhancements
1. Offline support for common languages
2. Real-time transcription feedback
3. Voice verification for authenticity
4. Dialect recognition
5. Multi-speaker detection
6. Emotion/urgency detection from voice

## Security Considerations
- Audio files stored securely with unique names
- User consent for voice recording
- Privacy-preserving transcription (no cloud storage of raw audio)
- Secure deletion of audio after processing (configurable retention)

## Performance
- Average transcription time: 2-5 seconds
- Supported audio length: up to 60 seconds per recording
- Storage: ~1-2 MB per minute of audio (WAV format)

## Troubleshooting

### Common Issues

1. **"Could not understand audio"**
   - Solution: Speak clearly, reduce background noise
   - Enable manual correction workflow

2. **Low confidence scores**
   - Solution: Use manual correction feature
   - Record in quieter environment

3. **Translation errors**
   - Solution: Provide manual description override
   - Use simpler vocabulary

## License
This feature is part of VishwaGuru and follows the same license.
