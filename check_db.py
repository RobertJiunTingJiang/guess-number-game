from supabase import create_client, Client

SUPABASE_URL = "https://tavstphloajcmrfkgzkv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRhdnN0cGhsb2FqY21yZmtnemt2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc5MzcxNzUsImV4cCI6MjA4MzUxMzE3NX0.GG-f63-TTGbWapOQrKLxjQt3axCnMOcqUIp_24eHwLg"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    # 嘗試抓取一筆資料來查看欄位名稱
    response = supabase.table("py_scores_0120c").select("*").limit(1).execute()
    print("Columns found in table:", response.data[0].keys() if response.data else "No data found, cannot determine columns directly.")
except Exception as e:
    print("Error:", e)
