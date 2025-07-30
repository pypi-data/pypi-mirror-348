from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from pathlib import Path
from pandas import DataFrame
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class DataItem(BaseModel):
    id: str
    dataset: str
    meta: Dict[str, Any] = {}
    media: Dict[str, Any] = {}
    label: Optional[Any] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class DataResponse(BaseModel):
    items: List[DataItem]
    total: int

def create_app(df: DataFrame) -> FastAPI:
    """Create a FastAPI app with the loaded dataframe."""
    app = FastAPI(title="AnyEval API")
    
    # Set up CORS to allow the frontend to access the API
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Get the directory of the static files
    static_dir = Path(__file__).parent / "static"
    
    # Define API routes first (before mounting static files)
    @app.get("/api/data", response_model=DataResponse)
    async def get_data(
        offset: int = 0, 
        limit: int = 10, 
        dataset: Optional[str] = None
    ):
        """Get data items with pagination."""
        filtered_df = df.copy()
        
        # Apply dataset filter if provided
        if dataset:
            filtered_df = filtered_df[filtered_df["dataset"] == dataset]
        
        total = len(filtered_df)
        
        # Apply pagination
        if offset >= total:
            return {"items": [], "total": total}
        
        end_idx = min(offset + limit, total)
        page_df = filtered_df.iloc[offset:end_idx]
        
        # Convert to list of dictionaries
        items = page_df.to_dict(orient="records")
        
        return {
            "items": items,
            "total": total
        }
    
    @app.get("/api/datasets")
    async def get_datasets():
        """Get list of unique datasets."""
        datasets = df["dataset"].unique().tolist()
        return {"datasets": datasets}
    
    @app.get("/api/data/{item_id}", response_model=DataItem)
    async def get_item(item_id: str):
        """Get a specific data item by ID."""
        item = df[df["id"] == item_id]
        if len(item) == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        return item.iloc[0].to_dict()
    
    @app.put("/api/data/{item_id}")
    async def update_item(item_id: str, item: DataItem):
        """Update a data item (e.g. for evaluation)."""
        # Find the index of the item
        idx = df.index[df["id"] == item_id].tolist()
        if not idx:
            raise HTTPException(status_code=404, detail="Item not found")
        
        # Update the item in the dataframe
        df.loc[idx[0]] = item.dict()
        
        return {"message": "Item updated successfully"}

    # Mount static files for specific paths
    # Create additional mount for the nested static directory
    app.mount("/static/js", StaticFiles(directory=static_dir / "static" / "js"), name="js")
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    
    # Serve index.html for the root path
    @app.get("/", response_class=FileResponse)
    async def get_index():
        """Serve the index.html file."""
        index_path = static_dir / "index.html"
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {"message": "Frontend not installed"}
    
    # Serve index.html for any other unmatched path (SPA routing)
    @app.get("/{path:path}")
    async def serve_spa(path: str):
        # Exclude API paths
        if path.startswith("api/"):
            raise HTTPException(status_code=404, detail="Not Found")
        
        # Serve index.html for all other paths for SPA routing
        index_path = static_dir / "index.html"
        if os.path.exists(index_path):
            return FileResponse(index_path)
        
        raise HTTPException(status_code=404, detail="Not Found")
    
    return app 