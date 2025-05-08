# EXP-Bot-for-Filling-Missing-Information

**EXP Bot** is an AI-powered assistant designed to intelligently identify, prompt for, and fill missing information in JSON data structures based on natural language input. It ensures structured output through a multi-step process — from casual conversation detection to data validation.

---

## 🧠 Features

- Detects **casual/user-friendly inputs** and handles them as `chitchat`.
- Parses and completes **structured JSON** data based on user input.
- Flags missing data and prompts the user for clarification (`missing_value`).
- Seeks **user confirmation** before finalizing data.
- Returns completed JSON only after user validation (`done`).
- Includes a helpful `prompt` field in every response to guide next steps.

---

## 📁 .env File

Add your OpenAI API key to a `.env` file:

```env
OPENAI_API_KEY="sk-proj-0GfbXDF3MYYuIlgY..."
```

---

## 🧪 Test the API

You can test the bot using `curl`:

```bash
curl --location 'http://localhost:8000/chat' \
--header 'Content-Type: application/json' \
--data '{
  "prompt": "Yes",
  "user": "Jigensh"
}'
```

---

## 🧩 Response Format

The API always returns:

```json
{
  "intent": "chitchat | missing_value | confirmation | done",
  "prompt": "Next action prompt for the user",
  "data": {
    // structured JSON collected so far
  },
  "isValidatedbyUser": true | false
}
```

---

## 🚦 Intent Flow

1. **Chitchat** → casual interaction
2. **Missing Value** → prompt for incomplete data
3. **Confirmation** → ask user to review and validate
4. **Done** → return finalized JSON only after confirmation

---

## 🛠️ Tech Stack

- **FastAPI** for the backend API
- **OpenAI API** for natural language understanding
- **Python** for logic and orchestration


---

## 📦 Example Data Formats

### ✈️ flight_booking.json
```json
{
  "departure": "add departure location",
  "arrival": "add arrival location",
  "class": "add required class",
  "date": "date of departure"
}
```

### 🎬 movie_booking.json
```json
{
  "movieName": "Name of movie",
  "persons": "No of persons Adult",
  "minor": "No of Minors",
  "show_time": "Time of Screening"
}
```