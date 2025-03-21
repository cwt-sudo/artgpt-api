from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import uvicorn

app = FastAPI()

# OpenAI API Key（请替换为你的 API Key）
OPENAI_API_KEY = "your_openai_api_key"
openai.api_key = OPENAI_API_KEY

# 示例：获取市场数据
def fetch_market_data(artist: str):
    market_data = {
        "Pablo Picasso": {
            "average_price": "$1.2M",
            "recent_auction": "Sotheby’s, March 2024, Sold for $1.5M",
            "market_trend": "Rising demand in contemporary auctions"
        },
        "Vincent van Gogh": {
            "average_price": "$5.8M",
            "recent_auction": "Christie’s, February 2024, Sold for $6.1M",
            "market_trend": "Stable with high collector interest"
        }
    }
    return market_data.get(artist, {"message": "No market data available"})

class QueryRequest(BaseModel):
    query: str

@app.post("/analyze")
def analyze_query(request: QueryRequest):
    user_query = request.query.lower()
    response_text = ""

    if "market" in user_query or "value" in user_query:
        artist_name = "Pablo Picasso"
        market_data = fetch_market_data(artist_name)
        response_text = f"Market Analysis for {artist_name}: {market_data}"
    else:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": request.query}]
            )
            response_text = response["choices"][0]["message"]["content"]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return {"response": response_text}

@app.get("/")
def root():
    return {"message": "artgpt AI Server is running with enhanced features!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
