try:
    import pymysql

    pymysql.install_as_MySQLdb()
except ImportError:
    # pymysql not installed - fine if you're only using SQLite (DB_ENGINE=sqlite)
    pass
