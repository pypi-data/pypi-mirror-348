from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fit_tech.app.db.seed import run_seeds
from fit_tech.app.core.security import get_current_user_optional
from fit_tech.app.api.routes import auth, workouts, exercises, recipes, ingredients, reminders
from fit_tech.app.db.session import engine, Base

app = FastAPI(title="FitTech API", version="1.0.0")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await run_seeds()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=str(BASE_DIR/"static")), name="static")

templates = Jinja2Templates(directory=str(BASE_DIR/"templates"))

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(workouts.router, prefix="/api/workouts", tags=["workouts"])
app.include_router(exercises.router, prefix="/api/exercises", tags=["exercises"])
app.include_router(recipes.router, prefix="/api/recipes", tags=["recipes"])
app.include_router(ingredients.router, prefix="/api/ingredients", tags=["ingredients"])
app.include_router(reminders.router, prefix="/api/reminders", tags=["reminders"])

@app.get("/")
async def index(request: Request, current_user=Depends(get_current_user_optional)):
    return templates.TemplateResponse("index.html", {"request": request, "current_user": current_user, 'bot_username': "fit_tech_bot"})

@app.get("/login")
async def login_page(request: Request, current_user=Depends(get_current_user_optional)):
    return templates.TemplateResponse("login.html", {"request": request, "current_user": current_user, 'bot_username': "fit_tech_bot"})

@app.get("/register")
async def register_page(request: Request, current_user=Depends(get_current_user_optional)):
    return templates.TemplateResponse("register.html", {"request": request, "current_user": current_user, 'bot_username': "fit_tech_bot"})

@app.get("/workouts")
async def workouts_page(request: Request, current_user=Depends(get_current_user_optional)):
    return templates.TemplateResponse("workouts.html", {"request": request, "current_user": current_user, 'bot_username': "fit_tech_bot"})

@app.get("/workouts/{workout_id}")
async def workout_detail(request: Request, workout_id: int, current_user=Depends(get_current_user_optional)):
    return templates.TemplateResponse("workout_detail.html", {"request": request, "current_user": current_user, "workout_id": workout_id, 'bot_username': "fit_tech_bot"})

@app.get("/recipes")
async def recipes_page(request: Request, current_user=Depends(get_current_user_optional)):
    return templates.TemplateResponse("recipes.html",{"request": request, "current_user": current_user, 'bot_username': "fit_tech_bot"})
    
@app.get("/recipes/{recipe_id}")
async def recipe_detail(request: Request, recipe_id: int, current_user=Depends(get_current_user_optional)):
    return templates.TemplateResponse("recipe_detail.html",{"request": request, "current_user": current_user, "recipe_id": recipe_id, 'bot_username': "fit_tech_bot"})

@app.get("/kcal-calculator")
async def kcal_calculator(request: Request, current_user=Depends(get_current_user_optional)):
    return templates.TemplateResponse("kcal_calculator.html", {"request": request, "current_user": current_user, 'bot_username': "fit_tech_bot"})

@app.get("/reminders")
async def reminders_page(request: Request, current_user=Depends(get_current_user_optional)):
    return templates.TemplateResponse("reminders.html",{"request": request, "current_user": current_user, 'bot_username': "fit_tech_bot"})

@app.get("/webapp")
async def webapp_page(request: Request, current_user=Depends(get_current_user_optional)):
    return templates.TemplateResponse("webapp.html",{"request": request, "current_user": current_user, 'bot_username': "fit_tech_bot"})


@app.get("/api/")
async def api_root():
    return {"message": "FitTech API is running"}

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}
