import psycopg2
import re

class PostgreSQLPipeline:
    
    def __init__(self):
        self.hostname = 'localhost'
        self.username = 'postgres'
        self.password = 'azerton'
        self.database = 'imdb_data'
        self.connection = psycopg2.connect(host=self.hostname, user=self.username, password=self.password, dbname=self.database)
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

        # Assure que la table existe avec la contrainte UNIQUE sur 'url' et 'titre'
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS imdb_data(
            id SERIAL PRIMARY KEY,
            titre TEXT UNIQUE,
            genre TEXT,
            type_ TEXT,
            pegi TEXT,
            duree INT,
            saisons TEXT,
            annee TEXT,
            score INT,
            nombre_vote INT,
            description TEXT,
            casting_principal TEXT,
            langue TEXT,
            pays TEXT,
            details TEXT,
            url TEXT UNIQUE
        );
        """)

    def process_item(self, item, spider):
        # Convertir les champs nécessaires
        score = self.convert_score(item.get('score', 0))
        nombre_vote = self.convert_nombre_vote(item.get('nombre_vote', '0'))
        genre = ';'.join(item.get('genre', []))
        casting_principal = ';'.join(item.get('casting_principal', []))
        langue = ';'.join(item.get('langue', []))
        pays = ';'.join(item.get('pays', []))
        annee = item.get('annee', 0)
        pegi = item.get('pegi')
        duree = self.convert_time(item.get('duree', '0'))
        type_ = item.get('type_')
        saisons = item.get('saisons')
        details = ';'.join(item.get('details', []))
        url = item.get('url', '')
        
        # Vérifier si le titre existe déjà
        self.cursor.execute("SELECT * FROM imdb_data WHERE titre = %s", (item.get("titre", ""),))
        result = self.cursor.fetchone()
        
        if result:
            spider.logger.info(f"Le titre '{item.get('titre', '')}' existe déjà dans la base de données.")
        else:
            # Insérer l'item s'il n'existe pas déjà
            self.cursor.execute("""
            INSERT INTO imdb_data (titre, genre, type_, pegi, duree, saisons, annee, score, nombre_vote, description, casting_principal, langue, pays, details, url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                item.get("titre", ""),
                genre,
                type_,
                pegi,
                duree,
                saisons,
                annee,
                score,
                nombre_vote,
                item.get("description", ""),
                casting_principal,
                langue,
                pays,
                details,
                url,
            ))
            spider.logger.info(f"L'item '{item.get('titre', '')}' a été inséré dans la base de données.")
        return item

    def convert_score(self, score_str):
        try:
            return float(score_str)
        except ValueError:
            return 0

    def convert_nombre_vote(self, nombre_vote_str):
        nombre_vote_str = nombre_vote_str.upper().replace('K', '000').replace('M', '000000')
        try:
            return int(re.sub("[^0-9]", "", nombre_vote_str))
        except ValueError:
            return 0

    def convert_time(self, duree):
        if isinstance(duree, int):
            return duree
        parts = duree.split(' ')
        heures = 0
        minutes = 0
        for part in parts:
            if 'h' in part:
                heures = int(part.replace('h', '')) * 60
            elif 'm' in part:
                minutes = int(part.replace('m', ''))
        return heures + minutes
