from ai.grievance_ai import classify_with_ai
result = classify_with_ai(
   "Mere area mein 3 din se paani nahi aa raha hai.",
    "hi"
)
print(result)
print("Category : ", result.category)
print("Department : ", result.department)
print("Priority : ", result.priority)
print("Summary : ", result.summary)
print("Intent : ", result.intent)