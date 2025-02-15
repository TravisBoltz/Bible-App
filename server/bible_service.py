from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os

class BibleService:
    def __init__(self):
        db_path = os.path.join(os.path.dirname(__file__), 'bible-sqlite.db')
        self.engine = create_engine(f'sqlite:///{db_path}')
        self.Session = sessionmaker(bind=self.engine)

        # Cache book mappings
        self.book_mappings = self._initialize_book_mappings()

    def _initialize_book_mappings(self):
        """Initialize book mappings from the database"""
        session = self.Session()
        try:
            # Get both key_english and key_abbreviations_english mappings
            main_mappings = session.execute(
                text("SELECT b, n FROM key_english")  # Changed from 'id' to 'b'
            ).all()
            abbr_mappings = session.execute(
                text("SELECT a, b FROM key_abbreviations_english")
            ).all()

            # Create a dictionary of book IDs to names and include abbreviations
            mappings = {}
            id_to_name = {str(r[0]): r[1] for r in main_mappings}
            for abbr, book_id in abbr_mappings:
                book_name = id_to_name.get(str(book_id))
                if book_name:
                    mappings[abbr.lower()] = book_id
                    mappings[book_name.lower()] = book_id

            return mappings
        finally:
            session.close()

    def _normalize_book_name(self, book_name):
        """Convert book name or abbreviation to book ID"""
        # Handle common variations
        book_name = book_name.lower().strip()
        book_name = book_name.replace('1st', '1').replace('2nd', '2').replace('3rd', '3')
        book_name = book_name.replace('first', '1').replace('second', '2').replace('third', '3')
        
        # Try direct lookup
        book_id = self.book_mappings.get(book_name)
        if book_id:
            return book_id
        
        # Try partial matches
        for stored_name, stored_id in self.book_mappings.items():
            if stored_name.startswith(book_name):
                return stored_id
        
        return None

    def get_verse(self, book, chapter, verse, translation='kjv'):
        """Get a single verse from the Bible database"""
        session = self.Session()
        try:
            book_id = self._normalize_book_name(book)
            if not book_id:
                return None

            # Select the appropriate translation table
            table_name = f't_{translation.lower()}'
            
            result = session.execute(
                text(f"""
                SELECT ke.n as book_name, v.c as chapter, v.v as verse, v.t as text
                FROM {table_name} v
                JOIN key_english ke ON ke.b = v.b  # Changed from 'id' to 'b'
                WHERE v.b = :book 
                AND v.c = :chapter 
                AND v.v = :verse
                """),
                {"book": book_id, "chapter": chapter, "verse": verse}
            ).first()

            if result:
                return {
                    'reference': f"{result.book_name} {result.chapter}:{result.verse}",
                    'text': result.text,
                    'translation': translation.upper()
                }
            return None
        finally:
            session.close()

    def get_verse_range(self, book, chapter, start_verse, end_verse, translation='kjv'):
        """Get a range of verses from the Bible database"""
        session = self.Session()
        try:
            book_id = self._normalize_book_name(book)
            if not book_id:
                return []

            # Select the appropriate translation table
            table_name = f't_{translation.lower()}'
            
            results = session.execute(
                text(f"""
                SELECT ke.n as book_name, v.c as chapter, v.v as verse, v.t as text
                FROM {table_name} v
                JOIN key_english ke ON ke.b = v.b  # Changed from 'id' to 'b'
                WHERE v.b = :book 
                AND v.c = :chapter 
                AND v.v BETWEEN :start_verse AND :end_verse
                ORDER BY v.v
                """),
                {
                    "book": book_id,
                    "chapter": chapter,
                    "start_verse": start_verse,
                    "end_verse": end_verse
                }
            ).all()

            return [
                {
                    'reference': f"{r.book_name} {r.chapter}:{r.verse}",
                    'text': r.text,
                    'translation': translation.upper()
                }
                for r in results
            ]
        finally:
            session.close()

    def search_text(self, search_term, translation='kjv'):
        """Search for verses containing specific text"""
        session = self.Session()
        try:
            # Select the appropriate translation table
            table_name = f't_{translation.lower()}'
            
            results = session.execute(
                text(f"""
                SELECT ke.n as book_name, v.c as chapter, v.v as verse, v.t as text
                FROM {table_name} v
                JOIN key_english ke ON ke.b = v.b  # Changed from 'id' to 'b'
                WHERE v.t LIKE :search_term
                LIMIT 10
                """),
                {"search_term": f"%{search_term}%"}
            ).all()

            return [
                {
                    'reference': f"{r.book_name} {r.chapter}:{r.verse}",
                    'text': r.text,
                    'translation': translation.upper()
                }
                for r in results
            ]
        finally:
            session.close()

    def get_available_translations(self):
        """Get list of available translations"""
        session = self.Session()
        try:
            results = session.execute(
                text("""
                SELECT table, abbreviation, version
                FROM bible_version_key
                """)
            ).all()
            return [
                {
                    'id': r.table.replace('t_', ''),
                    'abbreviation': r.abbreviation,
                    'name': r.version
                }
                for r in results
            ]
        finally:
            session.close()

bible_service = BibleService()