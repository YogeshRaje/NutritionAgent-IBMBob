"""
IBM Granite LLM interface with guardrails for Nutrition Agentic AI
"""
from __future__ import annotations

import re
from typing import Optional

from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

from nutrition_agent.config import (
    IBM_API_KEY,
    IBM_PROJECT_ID,
    IBM_REGION,
    MODEL_ID,
    GENERATE_PARAMS,
    HARMFUL_KEYWORDS,
    MEDICAL_DISCLAIMER,
)


class NutritionLLMClient:
    """Thin wrapper around IBM Granite with input/output guardrails."""

    def __init__(self) -> None:
        credentials = Credentials(
            url=IBM_REGION,
            api_key=IBM_API_KEY,
        )
        self._client = APIClient(credentials=credentials, project_id=IBM_PROJECT_ID)
        self._model = ModelInference(
            model_id=MODEL_ID,
            api_client=self._client,
            params=GENERATE_PARAMS,
            project_id=IBM_PROJECT_ID,
        )

    # ─────────────────────────── guardrails ────────────────────────────────

    def _input_guardrail(self, prompt: str) -> Optional[str]:
        """Return a refusal message if the prompt contains harmful content."""
        lower = prompt.lower()
        for kw in HARMFUL_KEYWORDS:
            if kw in lower:
                return (
                    f"⚠️  I'm sorry, but I cannot provide advice that includes "
                    f"'{kw}'. Please consult a registered dietitian or healthcare "
                    f"professional for support with this topic."
                )
        return None

    def _output_guardrail(self, text: str) -> str:
        """Post-process model output to strip potentially unsafe patterns."""
        # Remove any accidental dosage instructions for medications
        text = re.sub(
            r"(take|consume|inject)\s+\d+\s*(mg|ml|units?)\s+of\s+\w+",
            "[medication instruction removed – consult your doctor]",
            text,
            flags=re.IGNORECASE,
        )
        return text.strip()

    # ─────────────────────────── public API ────────────────────────────────

    def generate(self, prompt: str) -> str:
        """Run guardrails, call IBM Granite, return the final text."""
        refusal = self._input_guardrail(prompt)
        if refusal:
            return refusal

        response = self._model.generate_text(prompt=prompt)
        result = self._output_guardrail(response)
        return result

    def generate_nutrition_plan(self, user_profile: dict) -> str:
        """Build a structured prompt from user_profile and call IBM Granite."""
        system_preamble = (
            "You are NutritionAgent, a helpful, respectful, and harmless AI nutritionist "
            "powered by IBM Granite. Your role is to provide personalised, evidence-based "
            "nutrition guidance. Follow these ethics principles at all times:\n"
            "1. HELPFUL: Give practical, actionable advice tailored to the user.\n"
            "2. ACCURATE: Base recommendations on established nutritional science.\n"
            "3. MINDFUL: Respect dietary preferences, culture, and medical history.\n"
            "4. SAFE: Never recommend extreme diets, fasting under 1200 kcal/day, "
            "   or advice that contradicts standard medical guidance.\n"
            "5. TRANSPARENT: Acknowledge the limits of AI and always recommend "
            "   consulting a healthcare professional for medical concerns.\n\n"
        )

        medical_context = ""
        conditions = user_profile.get("medical_history", [])
        if conditions and conditions != ["None"]:
            medical_context = (
                f"IMPORTANT – Medical Conditions: {', '.join(conditions)}. "
                "Tailor all recommendations carefully to avoid contraindications. "
            )

        prompt = f"""{system_preamble}{medical_context}

USER PROFILE:
- Name: {user_profile['name']}
- Age: {user_profile['age']} years
- Diet Preference: {user_profile['diet_preference']}
- Medical History: {', '.join(user_profile.get('medical_history', ['None']))}
- Location: {user_profile['city']}, {user_profile['country']}
- Goal: {user_profile.get('goal', 'General healthy eating')}

TASK: Generate a comprehensive, personalised weekly nutrition plan for {user_profile['name']}.

Structure your response as follows:
## 1. Nutritional Overview
   - Recommended daily calorie range
   - Key macronutrient targets (carbs, protein, fat)
   - Key micronutrients to prioritise given medical history

## 2. Weekly Meal Plan (Day-by-Day)
   For each day (Monday – Sunday), list:
   - Breakfast
   - Mid-Morning Snack
   - Lunch
   - Afternoon Snack
   - Dinner

## 3. Foods to Emphasise
   List 10 specific foods ideal for this profile with brief reasons.

## 4. Foods to Avoid or Limit
   List foods and explain why given the medical history.

## 5. Hydration & Lifestyle Tips
   Practical water intake, sleep, and activity recommendations.

## 6. Local & Seasonal Suggestions
   Suggest locally available foods from {user_profile['city']}, {user_profile['country']}.

Use a warm, encouraging, respectful tone. Be specific and practical.
"""

        raw_plan = self.generate(prompt)
        return raw_plan + MEDICAL_DISCLAIMER
