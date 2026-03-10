from fastapi import FastAPI, HTTPException, status, Form, Body, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime

app = FastAPI()

# Настройка Jinja2 и статических файлов
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# Модель для ответов и хранения в базе данных
class Sensor(BaseModel):
    name: str = Field(..., description="Название датчика")
    addr: int = Field(..., ge=9, le=128, description="I2C-адрес модуля")
    input: int = Field(..., ge=0, le=7, description="Номер входа модуля")
    readout: Decimal | None = Field(default=None, description="Показания датчика")

class Facility(BaseModel):
    sn: int = Field(..., description="Серийный номер узла")
    name: str = Field(..., description="Название объекта")
    addr: str | None = Field(default=None, description="Адрес объекта")
    sensors: list[Sensor] = Field(default=[], description="Список датчикоы объекта")
    update_time: datetime | None = Field(default=None, description="Время последнего обновления показаний")

# Инициализируем messages_db как список объектов Message
facilities_db: list[Facility] = [Facility(sn=0, name="Офис ВН", addr="Великий Новгород, ул.Менделдеева, д.4а",
                                          sensors=[Sensor(name="Датчик 1", addr=10, input=0, readout=Decimal(101.5))])]

# GET /messages: Возвращает весь список сообщений
@app.get("/facilities", response_model=list[Facility])
async def get_facilities() -> list[Facility]:
    return facilities_db

@app.get("/facility/{sn}", response_model=Facility)
async def put_facility(sn: int) -> Facility:
    for i, fclt in enumerate(facilities_db):
        if fclt.sn == sn:
            return facilities_db[i]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Объект с заданным серийным номером не найден")

@app.put("/facility/{sn}", response_model=Facility)
async def put_facility(sn: int, facility: Facility = Body(...)) -> Facility:
    for i, fclt in enumerate(facilities_db):
        if fclt.sn == sn:
            facilities_db[i] = facility
            return facilities_db[i]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Объект с заданным серийным номером не найден")

@app.get("/web/facilities", response_class=HTMLResponse)
async def get_facilities_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "facilities": facilities_db})

@app.get("/web/facilities/{sn}", response_class=HTMLResponse)
async def get_facility_page(request: Request, sn: int):
    for i, fclt in enumerate(facilities_db):
        if fclt.sn == sn:
            facility = facilities_db[i]
            break
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Объект с заданным серийным номером не найден")

    return templates.TemplateResponse("facility.html", {"request": request, "facility": facility})
