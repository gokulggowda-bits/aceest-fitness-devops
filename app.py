from flask import Flask, jsonify, request

app = Flask(__name__)

# Data from ACEest Tkinter versions — programs, workouts, diets, calorie factors
PROGRAMS = {
    "Fat Loss (FL)": {
        "workout": "Mon: Back Squat 5x5 + Core, Tue: EMOM 20min Assault Bike, Wed: Bench Press + 21-15-9, Thu: Deadlift + Box Jumps, Fri: Zone 2 Cardio 30min",
        "diet": "Breakfast: Egg Whites + Oats, Lunch: Grilled Chicken + Brown Rice, Dinner: Fish Curry + Millet Roti, Target: ~2000 kcal",
        "calorie_factor": 22
    },
    "Muscle Gain (MG)": {
        "workout": "Mon: Squat 5x5, Tue: Bench 5x5, Wed: Deadlift 4x6, Thu: Front Squat 4x8, Fri: Incline Press 4x10, Sat: Barbell Rows 4x10",
        "diet": "Breakfast: Eggs + Peanut Butter Oats, Lunch: Chicken Biryani, Dinner: Mutton Curry + Rice, Target: ~3200 kcal",
        "calorie_factor": 35
    },
    "Beginner (BG)": {
        "workout": "Full Body Circuit: Air Squats, Ring Rows, Push-ups. Focus: Technique and Consistency",
        "diet": "Balanced Tamil Meals: Idli-Sambar, Rice-Dal, Chapati. Protein Target: 120g/day",
        "calorie_factor": 26
    }
}


@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to ACEest Fitness and Gym API",
        "status": "running"
    })


@app.route("/programs", methods=["GET"])
def get_programs():
    return jsonify({"programs": list(PROGRAMS.keys())})


@app.route("/program/<name>", methods=["GET"])
def get_program(name):
    for key, val in PROGRAMS.items():
        if name.lower() in key.lower():
            return jsonify({"program": key, "details": val})
    return jsonify({"error": "Program not found"}), 404


@app.route("/calories", methods=["POST"])
def calculate_calories():
    data = request.get_json()
    weight = data.get("weight", 0)
    program = data.get("program", "")

    for key, val in PROGRAMS.items():
        if program.lower() in key.lower():
            calories = int(weight * val["calorie_factor"])
            return jsonify({
                "program": key,
                "weight_kg": weight,
                "daily_calories": calories
            })
    return jsonify({"error": "Invalid program"}), 400


@app.route("/bmi", methods=["POST"])
def calculate_bmi():
    data = request.get_json()
    weight = data.get("weight", 0)
    height_cm = data.get("height", 0)

    if weight <= 0 or height_cm <= 0:
        return jsonify({"error": "Valid weight and height required"}), 400

    h_m = height_cm / 100.0
    bmi = round(weight / (h_m * h_m), 1)

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    return jsonify({"bmi": bmi, "category": category})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
