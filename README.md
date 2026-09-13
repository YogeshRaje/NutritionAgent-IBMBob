# 🥗 NutritionAgent – IBM Granite AI

> **Personalised Nutrition Planning powered by IBM Granite LLM via IBM watsonx.ai**  
> Built with IBM Bob | Agentic AI | Ethical AI | HAM Principles

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![IBM watsonx.ai](https://img.shields.io/badge/IBM-watsonx.ai-0f62fe)](https://www.ibm.com/products/watsonx-ai)
[![IBM Granite](https://img.shields.io/badge/Model-granite--3--8b--instruct-green)](https://www.ibm.com/granite)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 📌 Overview

**NutritionAgent** is an Agentic AI application that generates personalised weekly nutrition plans using the **IBM Granite 3-8B Instruct** language model. The agent collects user details through an interactive CLI, builds a contextual prompt enriched with medical history and location data, and generates a structured, ethical nutrition plan — saved as a Markdown file.

### What it does
- Collects: **name, age, diet preference, medical history, location, health goal**
- Generates a **7-day personalised meal plan** with breakfast, snacks, lunch, and dinner
- Provides **nutritional overview, foods to emphasise/avoid, hydration tips, local suggestions**
- Applies **AI ethics (HAM), input/output guardrails**, and a clear **medical disclaimer**
- Saves every plan as a timestamped `.md` file

---

## 🏗️ Architecture

```
User CLI → Input Guardrails → Prompt Builder → IBM Granite LLM (watsonx.ai)
                                                       ↓
Markdown File ← Plan Generator ← Output Guardrails ← LLM Response
```

### Project Structure

```
NutritionAgent-IBMBob/
├── nutrition_agent/
│   ├── __init__.py          # Package init
│   ├── config.py            # .env loader, constants, disclaimer
│   ├── llm_client.py        # IBM Granite interface + guardrails
│   ├── user_intake.py       # Interactive CLI user profile collector
│   └── plan_generator.py    # Orchestrates generation + saves .md
├── tests/
│   ├── __init__.py
│   └── test_nutrition_agent.py  # Full LLM testing suite
├── nutrition_plans/         # Generated plans (created at runtime)
├── main.py                  # Application entry point
├── run.bat                  # Windows launcher (auto-setup + run)
├── index.html               # Portfolio website
├── sample_nutrition_plan.md # Sample output for reference
├── requirements.txt         # Python dependencies
├── .env                     # Secrets (NOT committed to git)
├── .gitignore
└── README.md
```

---

## ⚡ Quick Start

### Prerequisites
- Python 3.10 or higher
- IBM watsonx.ai account with an API Key and Project ID
- Internet connection

### 1. Clone the repository

```bash
git clone https://github.com/YogeshRaje/NutritionAgent-IBMBob.git
cd NutritionAgent-IBMBob
```

### 2. Configure IBM credentials

Create a `.env` file in the project root:

```env
IBM_API_KEY=your_ibm_api_key_here
IBM_PROJECT_ID=your_project_id_here
IBM_REGION=https://us-south.ml.cloud.ibm.com
PORT=3000
```

> **How to get credentials:**
> 1. Go to [IBM watsonx.ai](https://dataplatform.cloud.ibm.com/)
> 2. Create or open a project
> 3. Go to **Manage → Access (IAM)** to create an API key
> 4. Copy your **Project ID** from project settings

### 3a. Windows – Double-click to run (easiest)

```
run.bat
```

The batch file will:
- Check Python installation
- Create a virtual environment automatically
- Install all dependencies
- Launch the application

### 3b. Manual setup

```bash
# Create and activate virtual environment
python -m venv nutrition_env
nutrition_env\Scripts\activate      # Windows
# source nutrition_env/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

---

## 🎯 Usage

When you run the application, you will be prompted to enter:

| Field | Example |
|-------|---------|
| Full name | `Priya Sharma` |
| Age | `35` |
| Diet preference | `1` (Vegetarian) |
| Medical history | `2,3` (Diabetes Type 2, Hypertension) |
| City | `Mumbai` |
| Country | `India` |
| Health goal | `4` (Manage diabetes) |

After confirmation, IBM Granite generates a complete 7-day plan which is:
- **Displayed** in the terminal with rich formatting
- **Saved** automatically to `nutrition_plans/nutrition_plan_<name>_<city>_<timestamp>.md`

---

## 🧪 Running Tests

```bash
# Activate virtual environment first
nutrition_env\Scripts\activate

# Run all tests with coverage
pytest tests/ -v --tb=short

# Run with coverage report
pytest tests/ -v --cov=nutrition_agent --cov-report=term-missing
```

### Test Categories
| Test Category | Description |
|---------------|-------------|
| Unit Tests | Config, validators, filename generation |
| Guardrail Tests | Harmful keyword detection, output sanitisation |
| Profile Tests | User profile schema validation |
| Integration Tests | End-to-end LLM call with IBM Granite |
| HAM Compliance | Helpful, Accurate, Mindful tone verification |
| Medical Safety | Medical condition handling, disclaimer presence |
| Edge Cases | Empty input, boundary ages, special characters |

---

## ⚖️ AI Ethics & HAM Principles

NutritionAgent is built on the **HAM (Helpful, Accurate, Mindful)** ethical framework:

| Principle | Implementation |
|-----------|----------------|
| **Helpful** | Practical, actionable weekly meal plans tailored to the individual |
| **Accurate** | Evidence-based nutritional science embedded in system prompts |
| **Mindful** | Respects dietary choices, culture, religion, and medical constraints |
| **Safe** | Guardrails refuse harmful advice (crash diets, extreme restriction) |
| **Transparent** | Clearly identifies as AI; always recommends professional consultation |

### Guardrails
- **Input guardrails** — detect and block prompts containing harmful keywords (extreme fasting, starvation, crash diets, etc.)
- **Output guardrails** — post-process LLM output to remove accidental medication dosing instructions
- **Medical disclaimer** — automatically appended to every generated plan

---

## 🛡️ Medical Disclaimer

> This nutrition plan is generated by an AI system (IBM Granite LLM) for **informational purposes only**. It does **NOT** constitute medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional or registered dietitian before making significant dietary changes, especially if you have existing medical conditions. The developers and IBM are not liable for any health outcomes resulting from the use of this application.

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| AI Model | IBM Granite 3-8B Instruct (`ibm/granite-3-8b-instruct`) |
| AI Platform | IBM watsonx.ai |
| Development Tool | IBM Bob (Agentic AI Developer) |
| Language | Python 3.10+ |
| IBM SDK | `ibm-watsonx-ai==1.1.2` |
| CLI UI | `rich` + `questionary` |
| Config | `python-dotenv` |
| Testing | `pytest` + `pytest-cov` |
| Output Format | Markdown (`.md`) |
| Launcher | Windows Batch (`.bat`) |

---

## 📊 Agentic AI SDLC Phases

| Phase | Description |
|-------|-------------|
| 1. Requirements & Ethics | User stories, HAM principles, guardrail requirements |
| 2. Data & Knowledge Design | User profile schema, medical condition taxonomy |
| 3. Model Selection | IBM Granite 3-8B Instruct selected for safety and instruction-following |
| 4. Prompt Engineering | Structured system prompt with HAM principles and output template |
| 5. Guardrails & Safety | Input filtering, output post-processing, medical disclaimers |
| 6. Integration & Build | Modular Python package with clean separation of concerns |
| 7. Testing & Validation | LLM test suite with accuracy, safety, HAM, edge case coverage |
| 8. Deployment | GitHub deployment with README, .gitignore, requirements.txt |

---

## 🚀 Deployment on GitHub

```bash
git init
git add .
git commit -m "Initial commit: NutritionAgent IBM Granite AI"
git remote add origin https://github.com/YogeshRaje/NutritionAgent-IBMBob.git
git branch -M main
git push -u origin main
```

---

## 📄 Sample Output

See [`sample_nutrition_plan.md`](sample_nutrition_plan.md) for a complete example of a generated nutrition plan.

---

## 👥 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- **IBM watsonx.ai** for enterprise-grade AI infrastructure
- **IBM Granite** for safe, instruction-following language models
- **IBM Bob** for agentic AI development assistance
- Built as part of the **IBM Bob Portfolio Project Series**

---

*🥗 NutritionAgent – Helping you eat smarter, live better – ethically.*
