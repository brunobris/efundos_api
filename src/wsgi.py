from app import app
from resources import fundo_resource

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)