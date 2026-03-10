# level 1

# from fastapi import FastAPI

# app = FastAPI()

# # -----------------------------
# # ❌ FAULTY FUNCTION
# # Causes Internal Server Error
# # -----------------------------
# def calculate_discount(price):
#     discount = price * 0.1
#     final_price = price - discount
#     return final_price  # ✅ correct variable name


# # -----------------------------
# # ✅ WORKING ROUTE (until faulty function is called)
# # -----------------------------
# @app.get("/product")
# def get_product():
#     product = {
#         "name": "Laptop",
#         "price": 50000
#     }

#     # ❌ Calling faulty function
#     discounted_price = calculate_discount(product["price"])

#     return {
#         "product": product["name"],
#         "final_price": discounted_price
#     }



# level 2

# from fastapi import FastAPI, Form
# import asyncio

# app = FastAPI()

# # ----------------------------------
# # ❌ FAULTY ASYNC FUNCTION
# # ----------------------------------
# async def fetch_user_from_db(user_id: int):
#     await asyncio.sleep(1)

#     fake_db = {
#         1: {"name": "Aryan", "role": "Admin"},
#         2: {"name": "Riya", "role": "User"}
#     }

#     # ❌ Logical mistake: returning None sometimes
#     if user_id in fake_db:
#         return fake_db[user_id]
#     else:
#         return None
#     # user_id not in fake_db → returns None implicitly


# # ----------------------------------
# # ❌ ROUTE THAT CRASHES AT RUNTIME
# # ----------------------------------
# @app.get("/user")
# async def get_user(user_id: int = Form(...)):

#     user = await fetch_user_from_db(user_id)

#     # ❌ Runtime error if user is None
#     if user is None:
#         return {"error": "User not found"}

#     return {
#         "username": user["name"],
#         "role": user["role"]
#     }


# level 3

from fastapi import FastAPI, Depends
import asyncio

app = FastAPI()

# -----------------------------------
# ❌ FAULTY DEPENDENCY FUNCTION
# -----------------------------------
async def get_current_user():
    await asyncio.sleep(0.5)

    fake_auth_db = {
        "token123": {"id": 1, "name": "Aryan"},
    }

    # token = fake_auth_db["token123"]  # ❌ hardcoded wrong token
    token = "token123"  # ✅ correct token 

    # ❌ returns None if token invalid
    if token in fake_auth_db:
        return fake_auth_db[token]
    else:  
        return None


# -----------------------------------
# ❌ BUSINESS LOGIC FUNCTION
# -----------------------------------
async def get_user_dashboard(user: dict,fake_auth_db: dict):
    
    # ❌ assumes user is always valid
    if user is None:
        raise Exception("User not authenticated")
    if user not in fake_auth_db.values():
        raise Exception("User not authenticated")
    return {
        "welcome": f"Hello {user['name']}",
        "role": "Admin"
    }


# -----------------------------------
# ❌ ROUTE (CRASHES AT RUNTIME)
# -----------------------------------
@app.get("/dashboard")
# async def dashboard(user=Depends(get_current_user)):
#     data = await get_user_dashboard(user)
#     return data
async def dashboard(user=Depends(get_current_user)):
    fake_auth_db = {
        "token123": {"id": 1, "name": "Aryan"},
    } 
    data = await get_user_dashboard(user,fake_auth_db)
    return data
