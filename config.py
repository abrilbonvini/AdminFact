class Config:
    SECRET_KEY = "cambia-esta-clave"
    # Usuario/clave que me diste (¡ojo con el !, ya lo dejé URL-encoded!)
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:ab7Nsur57%21@localhost/adminfact"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
