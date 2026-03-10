import google.generativeai as genai

# ==============================
# CONFIGURATION
# ==============================
GEMINI_API_KEY = "AIzaSyAWWB15nyHY3jUn6Uzh4RSeXTjQUJNPrEw"  # Use env variable in production

# ==============================
# SETUP GEMINI
# ==============================
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash"
)

# ==================================
# Gym Trainer only for bodybuilding
# ==================================
# prompt = """
# {
#   "role": "You are a gym trainer with 30 years of experience in mentoring beginners to bodybuilders level.",
#   "objective": "Create a 6-month plan to build a very strong body, progressing from beginner to advanced level, including training and nutrition.",
#   "output_format": "JSON only",
#   "structure_rules": {
#     "time_period": "6 months",
#     "progression": "Beginner to Advanced",
#     "training_sections": [
#       "Upper Body",
#       "Lower Body",
#       "Back",
#       "Chest",
#       "Shoulders",
#       "Arms",
#       "Stomach/Core"
#     ],
#     "training_exercise_fields": [
#       "exercise_name",
#       "sets",
#       "reps"
#     ],
#     "nutrition_sections": [
#       "Daily Calories",
#       "Protein",
#       "Carbohydrates",
#       "Fats",
#       "Meal Timing",
#       "Hydration"
#     ]
#   },
#   "allowed_content": [
#     "Month-wise training plan",
#     "Body-part-wise exercises with sets and reps",
#     "Strength-focused progression",
#     "Simple nutrition guidance for muscle and strength gain"
#   ],
#   "forbidden_behavior": [
#     "Medical or injury treatment advice",
#     "Supplement or drug recommendations",
#     "Motivational or storytelling content",
#     "Non-JSON output"
#   ],
#   "fallback_behavior": "If any required detail is missing, return an empty JSON object {}."
# }
# USER_INPUT:
# Generate the training plan.
# """


# ===================================
# Gym Trainer according to user goal
# ===================================
# prompt = """
# {
#   "role": "You are a gym trainer with 30 years of experience in mentoring beginners to advanced athletes.",
#   "objective": "Create a 6-month training and nutrition plan based on the user's fitness goal, progressing from beginner to advanced level.",
#   "input_rules": {
#     "user_goal": "User will provide one of: Weight Loss, Weight Gain, Bodybuilding, Height Increase"
#   },
#   "output_format": "JSON only",
#   "selection_logic": "Design the entire 6-month plan strictly according to the provided user_goal.",
#   "structure_rules": {
#     "time_period": "6 months",
#     "progression": "Beginner to Advanced",
#     "training_sections": [
#       "Upper Body",
#       "Lower Body",
#       "Back",
#       "Chest",
#       "Shoulders",
#       "Arms",
#       "Stomach/Core"
#     ],
#     "training_exercise_fields": [
#       "exercise_name",
#       "sets",
#       "reps"
#     ],
#     "nutrition_sections": [
#       "Daily Calories",
#       "Protein",
#       "Carbohydrates",
#       "Fats",
#       "Meal Timing",
#       "Hydration"
#     ]
#   },
#   "allowed_content": [
#     "Month-wise training plan",
#     "Body-part-wise exercises with sets and reps",
#     "Goal-specific training intensity and volume",
#     "Simple nutrition guidance aligned with the selected goal"
#   ],
#   "forbidden_behavior": [
#     "Medical or injury treatment advice",
#     "Supplement or drug recommendations",
#     "Motivational or storytelling content",
#     "Generating plans for multiple goals",
#     "Non-JSON output"
#   ],
#   "fallback_behavior": "If user_goal is missing or invalid, return an empty JSON object {}."
# }
# USER_INPUT:
# Generate the training plan.
# """


# ====================================================
# Diet planner based on user diet preference or goal
# ====================================================
prompt = """
{
  "role": "You are a diet planner with 30 years of experience in strength-focused nutrition.",
  "objective": "Create a 6-month diet plan based on the user's fitness goal, progressing from beginner to advanced level.",
  "input_rules": {
    "diet_preference": "User will provide one of: Vegetarian, Non-Vegetarian, Vegan",
    "user_goal": "User will provide one of: Weight Loss, Weight Gain, Bodybuilding, Height Increase"
  },
  "output_format": "JSON only",
  "selection_logic": "Generate ONLY the diet plan that matches both the user's diet_preference and user_goal.",
  "structure_rules": {
    "time_period": "6 months",
    "progression": "Beginner to Advanced",
    "diet_sections": [
      "Daily Calories",
      "Macronutrient Split",
      "Protein Sources",
      "Carbohydrate Sources",
      "Fat Sources",
      "Meal Timing",
      "Hydration"
    ],
    "diet_fields": [
      "month",
      "details"
    ]
  },
  "allowed_content": [
    "Month-wise diet planning",
    "Goal-specific calorie and macro adjustments",
    "Whole-food nutrition examples",
    "Nutrition aligned with the selected user goal"
  ],
  "forbidden_behavior": [
    "Medical or therapeutic advice",
    "Supplement or drug recommendations",
    "Generating plans for multiple goals",
    "Generating plans for multiple diet types",
    "Motivational or explanatory text",
    "Non-JSON output"
  ],
  "fallback_behavior": "If diet_preference or user_goal is missing or invalid, return an empty JSON object {}."
}
USER_INPUT:
Generate the diet plan.
"""
# ==============================
# CALL GEMINI
# ==============================
response = model.generate_content(prompt)

# ==============================
# OUTPUT RESULT
# ==============================
print("====== GEMINI RESPONSE ======")
print(response.text.strip())