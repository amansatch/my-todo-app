import json
import os

test_data = [
    {"task": "Test task", "due": "01/11/2025", "progress": 50, "id": "test-id"}
]

try:
    with open("todos_amanstrat.json", "w") as f:
        json.dump(test_data, f, indent=2)
    st.success("✅ JSON file written successfully.")
    st.write("Saved to:", os.path.abspath("todos_amanstrat.json"))
except Exception as e:
    st.error(f"❌ Failed to write JSON: {e}")
