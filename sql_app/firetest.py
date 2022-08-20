from distutils.command import check
import firebase_admin
from firebase_admin import auth, credentials
import custom_logger as logging

logger = logging.getmylogger(__name__)

def checkToken():
    try: 
        cred = credentials.Certificate('shared/firebase-admin-private-key.json')
        firebase_app = firebase_admin.initialize_app(cred)
        token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImE4YmZhNzU2NDk4ZmRjNTZlNmVmODQ4YWY5NTI5ZThiZWZkZDM3NDUiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZWFzZXNlcnZpY2UtOGE4MjgiLCJhdWQiOiJlYXNlc2VydmljZS04YTgyOCIsImF1dGhfdGltZSI6MTY2MDk0NjQyOCwidXNlcl9pZCI6ImljV2xpU2ExbFRiVmFFN0hGbXVocjZOMnRVVTIiLCJzdWIiOiJpY1dsaVNhMWxUYlZhRTdIRm11aHI2TjJ0VVUyIiwiaWF0IjoxNjYwOTQ2NDI4LCJleHAiOjE2NjA5NTAwMjgsImVtYWlsIjoibHVhbi52aWFuYUBvdXRsb29rLmNvbS5iciIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJsdWFuLnZpYW5hQG91dGxvb2suY29tLmJyIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.JRa6WDqxaMMF3SUfol5Xn85BbDNcke-tTxmiD5-WLaxy0DY9T_EQsW77Il0nrrb8PrHT7mndTUuE4PI-cLp_oBqPowREr9CUPoI6venWoBSPfIOKlboX4uNTN8kHDLNHqDDYC-nVjKhpBmGZFUX2GFxAJJ4blyqid0Ycevlt0AhAZSXDCP2MigRMH5e-R2cPMCRK_luDB_-_EvdGfQZ5WfkEV-f7kZg5TvCi3hIO_XW84qm4PNRoHCh3ZBg90WRA8kpg3FIARbLqGAnrRZwCSTGaf2FH7at9Jh2jM4lL1jQztZAEkLjiADykXQzE2fkTym9Ch3JaDceSVqmO12yEcw"
        print(auth.verify_id_token(token, app=firebase_app))
    except Exception as e:
        logger.critical(e)
        print(e)

checkToken()