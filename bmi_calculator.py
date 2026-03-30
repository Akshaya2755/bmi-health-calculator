def calculate_bmi(height, weight):

    height = float(height)
    weight = float(weight)

    bmi = weight / (height ** 2)

    if bmi < 18.5:
        category = "Underweight"
        tip = "You should eat more nutritious food."

    elif bmi < 25:
        category = "Normal"
        tip = "Great! Maintain your healthy lifestyle."

    elif bmi < 30:
        category = "Overweight"
        tip = "Exercise regularly and maintain balanced diet."

    else:
        category = "Obese"
        tip = "Consult a doctor and follow a proper health plan."

    return round(bmi,2), category, tip