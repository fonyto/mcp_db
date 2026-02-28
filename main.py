import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import psycopg2 
from psycopg2.extras import RealDictCursor
from fastmcp import FastMCP

app = FastMCP("company-db-server")

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        port= int(os.environ.get("DB_PORT")),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),        
        database=os.environ.get("DB_DATABASE"),
        cursor_factory = RealDictCursor
    )
    return conn 


#Herramienta
@app.tool
def list_tracks(limit: int = 5) -> List[Dict[str, Any]]:
    """Listar los tracks disponibles en la base de datos"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
        """SELECT album_id, name, composer FROM track ORDER BY composer LIMIT %s""", 
        (limit,))

        rows = cursor.fetchall()
        tracks = []
        for row in rows:
            tracks.append({
                "album_id": row["album_id"], 
                "name": row["name"],
                "composer": row["composer"]
            })       
        cursor.close()
        conn.close()

        return tracks

    except Exception as e:
        return {
            "error": f'Error al obtener los tracks: {str(e)}'
        }
    
if __name__ == "__main__":
    app.run(transport="sse", host="0.0.0.0", port=3000)
