from src import create_app

app = create_app()

if __name__ == "__main__":
    print("=" * 65)
    print("  NexZone Admin")
    print("  http://127.0.0.1:5000")
    print("  Login: frank@nexzone.com / admin123")
    print("=" * 65)
    app.run(debug=True, host="0.0.0.0", port=5000)
