import openai
import tkinter as tk
from tkinter import messagebox, Listbox

# Set your OpenAI API key
openai.api_key = "your-api-key"

# Function to generate dish suggestions
def get_dish_suggestions(cuisine, meal_type, ingredients):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional chef. Suggest dishes based on user preferences and ingredients.",
                },
                {
                    "role": "user",
                    "content": f"Suggest 5 {meal_type} dishes from {cuisine} cuisine that can be prepared with the following ingredients: {ingredients}. Provide a brief description of each dish.",
                },
            ],
            temperature=0.7,
            max_tokens=500,
        )
        suggestions = response["choices"][0]["message"]["content"]
        return suggestions.split("\n")  # Split into a list for easier display
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch suggestions: {str(e)}")
        return []

# Function to get detailed recipe for a selected dish
def get_recipe(dish_name):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional chef providing detailed recipes.",
                },
                {
                    "role": "user",
                    "content": f"Provide a detailed, step-by-step recipe for {dish_name}.",
                },
            ],
            temperature=0.7,
            max_tokens=1000,
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch recipe: {str(e)}")
        return "No recipe available."

# Function to display suggestions
def display_suggestions():
    cuisine = cuisine_entry.get()
    meal_type = meal_type_entry.get()
    ingredients = ingredients_entry.get()

    if not cuisine or not meal_type or not ingredients:
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    suggestions = get_dish_suggestions(cuisine, meal_type, ingredients)
    suggestions_list.delete(0, tk.END)  # Clear previous suggestions

    for suggestion in suggestions:
        if suggestion.strip():  # Avoid empty lines
            suggestions_list.insert(tk.END, suggestion)

# Function to display detailed recipe
def display_recipe():
    selected_dish = suggestions_list.get(tk.ACTIVE)
    if not selected_dish:
        messagebox.showwarning("Selection Error", "Please select a dish!")
        return

    recipe = get_recipe(selected_dish)
    recipe_text.delete("1.0", tk.END)  # Clear previous recipe
    recipe_text.insert(tk.END, recipe)

# Set up the UI
root = tk.Tk()
root.title("Chef GPT")

# Input fields
tk.Label(root, text="Cuisine:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
cuisine_entry = tk.Entry(root, width=30)
cuisine_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Meal Type:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
meal_type_entry = tk.Entry(root, width=30)
meal_type_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Ingredients:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
ingredients_entry = tk.Entry(root, width=50)
ingredients_entry.grid(row=2, column=1, padx=5, pady=5)

# Suggestion listbox
tk.Label(root, text="Dish Suggestions:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
suggestions_list = Listbox(root, width=60, height=10)
suggestions_list.grid(row=3, column=1, padx=5, pady=5)

# Buttons
tk.Button(root, text="Get Suggestions", command=display_suggestions).grid(row=4, column=0, padx=5, pady=10)
tk.Button(root, text="Get Recipe", command=display_recipe).grid(row=4, column=1, padx=5, pady=10)

# Recipe display
tk.Label(root, text="Recipe:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
recipe_text = tk.Text(root, width=60, height=15)
recipe_text.grid(row=5, column=1, padx=5, pady=5)

# Run the app
root.mainloop()
