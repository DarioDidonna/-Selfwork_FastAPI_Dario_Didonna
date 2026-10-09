from fastapi import FastAPI, HTTPException, Path, Query, Depends
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

app = FastAPI(
    title="Sapori di Puglia API",
    description="API avanzata per la gestione di ricette tradizionali pugliesi con validazione completa e modelli Pydantic per Query.",
    version="1.4.0"
)

# 1. MODELLI PYDANTIC (Corpo della richiesta e Risposta)

class Recipe(BaseModel):
    id: int
    title: str
    category: str
    description: str
    prep_time_minutes: int = Field(..., gt=0)
    featured: bool = False

class RecipeCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=100, description="Titolo della ricetta")
    category: str = Field(..., description="Categoria (es. Primo, Pizzeria, Dolce)")
    description: str = Field(..., min_length=10, description="Descrizione dettagliata")
    prep_time_minutes: int = Field(..., gt=0, le=300, description="Tempo di preparazione in minuti (max 300)")
    featured: Optional[bool] = False

class RecipeUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=100)
    category: Optional[str] = None
    description: Optional[str] = Field(None, min_length=10)
    prep_time_minutes: Optional[int] = Field(None, gt=0, le=300)
    featured: Optional[bool] = None

# 2. MODELLO PYDANTIC PER I QUERY PARAMETERS

class RecipeQueryParams(BaseModel):
    category: Optional[str] = Field(None, description="Filtra per categoria esatta")
    search: Optional[str] = Field(None, min_length=2, description="Cerca una parola chiave nel testo")
    max_prep_time: Optional[int] = Field(None, gt=0, description="Filtra per tempo massimo di preparazione")
    limit: int = Field(10, ge=1, le=50, description="Numero massimo di risultati da restituire")
    
    @field_validator('category')
    def case_insensitive_category(cls, v: Optional[str]) -> Optional[str]:
        if v:
            return v.capitalize()
        return v


# Database in-memory 
recipes_db = [
    Recipe(
        id=1,
        title="Orecchiette con Cime di Rapa",
        category="Primo",
        description="Il piatto simbolo della tradizione barese, condito con cime di rapa fresche, acciughe e aglio.",
        prep_time_minutes=30,
        featured=True
    ),
    Recipe(
        id=2,
        title="Focaccia Barese",
        category="Pizzeria",
        description="Soffice e croccante, condita con pomodorini freschi, olive barese e olio extravergine d'oliva.",
        prep_time_minutes=45,
        featured=True
    ),
    Recipe(
        id=3,
        title="Pasticciotto Leccese",
        category="Dolce",
        description="Guscio di pasta frolla ripieno di crema pasticcera, tipico del Salento.",
        prep_time_minutes=40,
        featured=False
    ),
    Recipe(
        id=4,
        title="Riso, Patate e Cozze",
        category="Primo",
        description="La tiella barese per eccellenza, un mix perfetto di riso, patate, cozze e pomodorini cotti al forno.",
        prep_time_minutes=60,
        featured=True
    )
]

@app.get("/", tags=["Home"])
def read_root():
    return {
        "message": "Benvenuto nelle API di Sapori di Puglia con Validazione Avanzata! 🌿🍝",
        "docs_url": "/docs"
    }

# Endpoint con Modello Pydantic per i Query Parameters
@app.get("/recipes", response_model=List[Recipe], tags=["Ricette"])
def get_recipes(query_params: RecipeQueryParams = Depends()):
    """
    Restituisce la lista delle ricette filtrata tramite un **modello Pydantic** dedicato ai Query Parameters.
    """
    result = recipes_db

    if query_params.category:
        result = [r for r in result if r.category.lower() == query_params.category.lower()]

    if query_params.search:
        s = query_params.search.lower()
        result = [r for r in result if s in r.title.lower() or s in r.description.lower()]

    if query_params.max_prep_time:
        result = [r for r in result if r.prep_time_minutes <= query_params.max_prep_time]

    return result[:query_params.limit]

# Endpoint con Path Parameter 
@app.get("/recipes/{recipe_id}", response_model=Recipe, tags=["Ricette"])
def get_recipe(
    recipe_id: int = Path(
        ..., 
        title="ID della Ricetta", 
        description="Deve essere un numero intero positivo compreso tra 1 e 1000",
        ge=1, 
        le=1000
    )
):
    """Restituisce i dettagli di una singola ricetta tramite Path Parameter validato."""
    for recipe in recipes_db:
        if recipe.id == recipe_id:
            return recipe
    raise HTTPException(status_code=404, detail="Ricetta non trovata.")

@app.post("/recipes", response_model=Recipe, status_code=201, tags=["Ricette"])
def create_recipe(body: RecipeCreate):
    new_id = max([r.id for r in recipes_db], default=0) + 1
    new_recipe = Recipe(id=new_id, **body.model_dump())
    recipes_db.append(new_recipe)
    return new_recipe

@app.patch("/recipes/{recipe_id}", response_model=Recipe, tags=["Ricette"])
def patch_recipe(
    recipe_id: int = Path(..., ge=1, description="ID della ricetta da aggiornare parzialmente"),
    body: RecipeUpdate = None
):
    for recipe in recipes_db:
        if recipe.id == recipe_id:
            stored_data = recipe.model_dump()
            update_data = body.model_dump(exclude_unset=True)
            
            for key, value in update_data.items():
                stored_data[key] = value
                
            updated_recipe = Recipe(**stored_data)
            recipe_index = recipes_db.index(recipe)
            recipes_db[recipe_index] = updated_recipe
            return updated_recipe
            
    raise HTTPException(status_code=404, detail="Ricetta non trovata.")