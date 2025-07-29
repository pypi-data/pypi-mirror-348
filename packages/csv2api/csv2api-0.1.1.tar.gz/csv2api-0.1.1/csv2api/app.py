from fastapi import FastAPI, HTTPException
import pandas as pd

app = FastAPI()
dataframe = pd.DataFrame()
csv_path = None

@app.on_event("startup")
def load_csv_on_start():
    global dataframe
    if csv_path:
        dataframe = pd.read_csv(csv_path)
        print(f"[STARTUP] Loaded {len(dataframe)} rows")

@app.get("/rows")
def get_all_rows():
    if dataframe.empty:
        raise HTTPException(status_code=503, detail="Dataframe not loaded yet.")
    return dataframe.to_dict(orient="records")

@app.get("/rows/{row_id}")
def get_row(row_id: int):
    if dataframe.empty:
        raise HTTPException(status_code=503, detail="Dataframe not loaded yet.")
    if 0 <= row_id < len(dataframe):
        return dataframe.iloc[row_id].to_dict()
    raise HTTPException(status_code=404, detail="Row not found")

@app.get("/search")
def search_rows(column: str, value: str):
    if dataframe.empty:
        raise HTTPException(status_code=503, detail="Dataframe not loaded yet.")
    if column not in dataframe.columns:
        raise HTTPException(status_code=400, detail="Invalid column name")
    filtered = dataframe[dataframe[column].astype(str) == value]
    return filtered.to_dict(orient="records")

def run_api(file):
    global csv_path
    csv_path = file
    import uvicorn
    uvicorn.run("csv2api.app:app", host="127.0.0.1", port=8000)


