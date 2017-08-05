from service import app

# For local development only
if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=8000)
