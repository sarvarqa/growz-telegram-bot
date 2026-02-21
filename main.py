from bot import build_application

def main():
    app = build_application()
    print("Bot ishga tushdi...")
    app.run_polling(close_loop=False)

if __name__ == "__main__":
    main()