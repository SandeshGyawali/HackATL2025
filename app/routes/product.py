from fastapi import APIRouter
from app.database import db

router = APIRouter()

@router.get("/product")
async def get_products():
    products = await db["product"].find().to_list(None)
    return products

@router.get("/production-step/{product_id}")
async def get_production_steps(product_id: str):
    steps = await db["production_step"].find({"product_id": product_id}).to_list(None)
    
    for step in steps:
        # Get time
        time_data = await db["production_step_time"].find_one({"step_id": step["_id"]})
        step["estimated_hours"] = time_data["estimated_hours"] if time_data else 0
        
        # Get materials and costs
        materials = await db["production_step_material"].find({"step_id": step["_id"]}).to_list(None)
        total_cost = 0
        
        for material in materials:
            price_data = await db["production_step_material_price"].find_one({"material_id": material["_id"]})
            if price_data:
                material["unit_price"] = price_data["unit_price"]
                total_cost += material["quantity"] * price_data["unit_price"]
        
        step["materials"] = materials
        step["total_cost"] = total_cost
    
    return steps

@router.get("/estimate/time/{product_id}")
async def get_time_estimate(product_id: str):
    steps = await db["production_step"].find({"product_id": product_id}).to_list(None)
    total_hours = 0
    
    for step in steps:
        time_data = await db["production_step_time"].find_one({"step_id": step["_id"]})
        if time_data:
            total_hours += time_data["estimated_hours"]
    
    return {"product_id": product_id, "total_estimated_hours": total_hours}

@router.get("/estimate/cost/{product_id}")
async def get_cost_estimate(product_id: str):
    steps = await db["production_step"].find({"product_id": product_id}).to_list(None)
    total_cost = 0
    
    for step in steps:
        materials = await db["production_step_material"].find({"step_id": step["_id"]}).to_list(None)
        
        for material in materials:
            price_data = await db["production_step_material_price"].find_one({"material_id": material["_id"]})
            if price_data:
                total_cost += material["quantity"] * price_data["unit_price"]
    
    return {"product_id": product_id, "total_estimated_cost": total_cost}