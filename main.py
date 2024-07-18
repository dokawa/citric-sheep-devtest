from app import create_app

# Create the app instance
app = create_app("development")

if __name__ == "__main__":
    app.run()
