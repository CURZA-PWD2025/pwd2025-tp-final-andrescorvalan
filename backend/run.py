import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Si la variable PORT existe (como en Docker), la usa. 
    # Si no usa el 5000 por defecto.
    port = int(os.environ.get('PORT', 5000))
    
    # host='0.0.0.0',para q ande Docker
    app.run(host='0.0.0.0', port=port, debug=True)