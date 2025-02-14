import os
import json
import sqlite3
import requests

def download_bible_data():
    """Download Bible data using the ESV API"""
    api_key = os.getenv('ESV_API_KEY', 'default-key')  # You'll need to get an API key from https://api.esv.org/
    headers = {
        'Authorization': f'Token {api_key}'
    }
    
    # Define the books of the Bible with their chapter counts
    bible_structure = {
        'Genesis': 50, 'Exodus': 40, 'Leviticus': 27, 'Numbers': 36, 'Deuteronomy': 34,
        'Joshua': 24, 'Judges': 21, 'Ruth': 4, '1 Samuel': 31, '2 Samuel': 24,
        '1 Kings': 22, '2 Kings': 25, '1 Chronicles': 29, '2 Chronicles': 36,
        'Ezra': 10, 'Nehemiah': 13, 'Esther': 10, 'Job': 42, 'Psalms': 150,
        'Proverbs': 31, 'Ecclesiastes': 12, 'Song of Solomon': 8, 'Isaiah': 66,
        'Jeremiah': 52, 'Lamentations': 5, 'Ezekiel': 48, 'Daniel': 12,
        'Hosea': 14, 'Joel': 3, 'Amos': 9, 'Obadiah': 1, 'Jonah': 4,
        'Micah': 7, 'Nahum': 3, 'Habakkuk': 3, 'Zephaniah': 3, 'Haggai': 2,
        'Zechariah': 14, 'Malachi': 4, 'Matthew': 28, 'Mark': 16, 'Luke': 24,
        'John': 21, 'Acts': 28, 'Romans': 16, '1 Corinthians': 16, '2 Corinthians': 13,
        'Galatians': 6, 'Ephesians': 6, 'Philippians': 4, 'Colossians': 4,
        '1 Thessalonians': 5, '2 Thessalonians': 3, '1 Timothy': 6, '2 Timothy': 4,
        'Titus': 3, 'Philemon': 1, 'Hebrews': 13, 'James': 5, '1 Peter': 5,
        '2 Peter': 3, '1 John': 5, '2 John': 1, '3 John': 1, 'Jude': 1,
        'Revelation': 22
    }
    
    bible_data = []
    
    for book, num_chapters in bible_structure.items():
        print(f"Processing {book}...")
        book_data = {'name': book, 'chapters': []}
        
        for chapter in range(1, num_chapters + 1):
            url = f'https://api.esv.org/v3/passage/text/?q={book}+{chapter}&include-verse-numbers=false&include-headings=false&include-passage-references=false'
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                verses = response.json()['passages'][0].strip().split('\n\n')
                book_data['chapters'].append(verses)
            else:
                print(f"Error downloading {book} chapter {chapter}: {response.status_code}")
                return None
        
        bible_data.append(book_data)
    
    return bible_data

def init_database():
    # Create database in the same directory as this script
    db_path = os.path.join(os.path.dirname(__file__), 'bible.db')
    
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bible_verses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book TEXT NOT NULL,
        chapter INTEGER NOT NULL,
        verse INTEGER NOT NULL,
        text TEXT NOT NULL,
        translation TEXT NOT NULL,
        UNIQUE(book, chapter, verse, translation)
    )
    ''')
    
    # Create index for faster lookups
    cursor.execute('''
    CREATE INDEX IF NOT EXISTS verse_lookup 
    ON bible_verses (book, chapter, verse, translation)
    ''')
    
    try:
        # For testing purposes, let's add some sample verses
        sample_verses = [
            ('John', 3, 16, 'For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life.', 'NIV'),
            ('Romans', 8, 28, 'And we know that in all things God works for the good of those who love him, who have been called according to his purpose.', 'NIV'),
            ('Philippians', 4, 13, 'I can do all this through him who gives me strength.', 'NIV'),
            ('Jeremiah', 29, 11, '"For I know the plans I have for you," declares the LORD, "plans to prosper you and not to harm you, plans to give you hope and a future."', 'NIV'),
        ]
        
        cursor.executemany('''
        INSERT OR REPLACE INTO bible_verses 
        (book, chapter, verse, text, translation)
        VALUES (?, ?, ?, ?, ?)
        ''', sample_verses)
        
        conn.commit()
        print("Database initialized with sample verses successfully!")
        print("Note: To use the full Bible database, please obtain an ESV API key from https://api.esv.org/")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        conn.rollback()
    
    finally:
        conn.close()

if __name__ == '__main__':
    init_database()