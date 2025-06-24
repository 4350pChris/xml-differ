from fastapi import APIRouter, HTTPException

from ..db.models import Paragraph

router = APIRouter(
    prefix="/diff",
    tags=["diff"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{left_id}/{right_id}", response_description="Diff endpoint")
async def get_diff(left_id: str, right_id: str):
    left = await Paragraph.get(left_id)
    if left is None:
        raise HTTPException(status_code=404, detail="Left paragraph not found")
    right = await Paragraph.get(right_id)
    if right is None:
        raise HTTPException(status_code=404, detail="Right paragraph not found")

    # Here you would implement the actual diff logic
    # For now, we just return a placeholder response
    return {
        "left_id": left.id,
        "right_id": right.id,
        "diff": f"Diff between {left.content} and {right.content}",
    }
