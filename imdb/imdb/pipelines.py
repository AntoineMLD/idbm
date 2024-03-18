import psycopg2
import re

class PostgreSQLPipeline:
    
    def __init__(self):
        hostname = 'localhost'
        username = 'postgres'
        password = 'azerton'
        database = 'imdb_data'
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

        self.cursor.execute("""
        DROP TABLE IF EXISTS imdb_data;
        CREATE TABLE imdb_data (
            id SERIAL PRIMARY KEY,
            titre TEXT,
            genre TEXT,
            serie TEXT,
            pegi TEXT,
            duree TEXT,
            saisons TEXT,
            annee INT,
            annee_serie TEXT,
            score TEXT,
            nombre_vote INT,
            description TEXT,
            casting_principal TEXT,
            langue TEXT,
            pays TEXT,
            details TEXT
        )
        """)

    def process_item(self, item, spider):
        score = self.convert_score(item.get('score', 0))
        nombre_vote = self.convert_nombre_vote(item.get('nombre_vote', '0'))
        genre = ';'.join(item.get('genre', []))  
        casting_principal = ';'.join(item.get('casting_principal', []))  
        langue = ';'.join(item.get('langue', []))  
        pays = ';'.join(item.get('pays', []))
        annee_value = item.get('annee', 0)
        try:
            annee = int(annee_value) if annee_value is not None else 0
        except ValueError:
            annee = 0   
        annee = int(annee_value) if annee_value is not None else 0 
        pegi = item.get('pegi')
        duree = self.convert_time(item.get('duree', '0'))
        serie = item.get('serie')
        saisons = item.get('saisons')
        annee_serie = ';'.join(item.get('annee_serie', []) or [] )
        details = ';'.join(item.get('details', []))
        
        
        self.cursor.execute("""
        INSERT INTO imdb_data (titre, genre, serie, pegi, duree, saisons, annee, annee_serie, score, nombre_vote, description, casting_principal, langue, pays, details) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            item.get("titre", ""),
            genre,
            serie,
            pegi,
            duree,
            saisons,
            annee,
            annee_serie,
            score,
            nombre_vote,
            item.get("description", ""),
            casting_principal,
            langue,
            pays,
            details
        ))
        return item

    def convert_score(self, score_str):
        try:
            return float(score_str)
        except ValueError:
            return 0

    def convert_nombre_vote(self, nombre_vote_str):
        nombre_vote_str = nombre_vote_str.upper().replace('K', '000').replace('M', '000000')
        try:
            return int(re.sub("[^0-9]", "", nombre_vote_str))  # Retire les caractères non numériques
        except ValueError:
            return 0


    def convert_time(self, duree):
        print(f"Conversion de la durée: '{duree}'")  # Débogage
        parts = duree.split(' ')
        heures = 0
        minutes = 0
        for part in parts:
            if 'h' in part:
                heures = int(part.replace('h', '')) * 60
            elif 'm' in part:
                minutes = int(part.replace('m', ''))
        total_minutes = heures + minutes
        print(f"Total en minutes: {total_minutes}")  # Débogage
        return total_minutes