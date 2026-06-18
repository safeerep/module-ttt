from fastapi import APIRouter, Depends, status
from talkingdb.models.graph.graph import GraphModel
from talkingdb.models.api.response import ErrorResponse
from talkingdb.clients.sqlite import sqlite_conn
from talkingdb.helpers.auth import verify_api_key

router = APIRouter(prefix="/v1", tags=["Tree"])

@router.get(
    "/tree/json",
    status_code=status.HTTP_200_OK,
    summary="Get document graph as JSON",
    description=(
        "Retrieve the node-link JSON representation of an indexed document graph. "
        "The graph can be used for visualization, analysis, or integration with "
        "graph-based front-end components."
    ),
    responses={
        401: {"model": ErrorResponse, "description": "Invalid or missing API key"},
        404: {"model": ErrorResponse, "description": "Graph ID not found"},
        500: {"model": ErrorResponse, "description": "Failed to load graph"},
    },
)
async def document_tree_json(
    graph_id: str,
    api_key: str = Depends(verify_api_key),
):
    with sqlite_conn() as conn:
        gm = GraphModel.load(conn, graph_id, True)
    
    return gm.g_json()
