from fastapi import FastAPI
from .purchase import router as purchase_router
from ..auth.middleware import router as middleware_router
from ..auth.user import router as user_router
from .inventory import router as inventory_router

app1 = FastAPI( 
               title = "Tickety",
               version = "0.1.0"
               )
app1.include_router(inventory_router)


app2 = FastAPI(
    title = "Tickety",
    version = "0.1.0"
)

app2.include_router(purchase_router)
app2.include_router(middleware_router)
app2.include_router(user_router)