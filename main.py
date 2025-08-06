from app import create_app
import os

app = create_app()

print("TEMPLATE FOLDER:", app.template_folder)  # ✅ Add this debug line

if __name__ == "__main__":
    app.run(debug=True)
