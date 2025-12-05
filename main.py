from fastapi import FastAPI, UploadFile, File as FastAPIFile, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from database import get_db, init_db
from models import File, Analysis
from schemas import FileResponse, AnalysisResponse
from ai_service import mock_ai_analysis
import os
import shutil
from typing import List
from contextlib import asynccontextmanager

STORAGE_PATH = os.getenv("STORAGE_PATH", "./storage")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаем директорию для хранения файлов
    os.makedirs(STORAGE_PATH, exist_ok=True)
    # Инициализируем БД
    await init_db()
    yield

app = FastAPI(title="Documents API", lifespan=lifespan)

@app.post("/files/upload", response_model=FileResponse)
async def upload_file(
    file: UploadFile = FastAPIFile(...),
    db: AsyncSession = Depends(get_db)
):
    """Загрузка файла с автоматическим версионированием"""
    
    # Проверяем существующие версии файла
    result = await db.execute(
        select(File)
        .where(File.original_name == file.filename)
        .order_by(desc(File.version))
    )
    existing_file = result.scalars().first()
    
    # Определяем версию
    version = 1 if not existing_file else existing_file.version + 1
    
    # Формируем путь для сохранения
    file_extension = os.path.splitext(file.filename)[1]
    filename_without_ext = os.path.splitext(file.filename)[0]
    storage_filename = f"{filename_without_ext}_v{version}{file_extension}"
    file_path = os.path.join(STORAGE_PATH, storage_filename)
    
    # Сохраняем файл
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Получаем размер файла
    file_size = os.path.getsize(file_path)
    
    # Создаем запись в БД
    db_file = File(
        original_name=file.filename,
        version=version,
        path=file_path,
        file_size=file_size,
        uploaded_by=1
    )
    
    db.add(db_file)
    await db.commit()
    await db.refresh(db_file)
    
    return db_file

@app.get("/files", response_model=List[FileResponse])
async def get_files(db: AsyncSession = Depends(get_db)):
    """Получение списка всех файлов"""
    
    result = await db.execute(
        select(File).order_by(desc(File.uploaded_at))
    )
    files = result.scalars().all()
    
    return files

@app.post("/files/{file_id}/analyze", response_model=AnalysisResponse)
async def analyze_file(
    file_id: int,
    db: AsyncSession = Depends(get_db)
):
    """AI-анализ документа"""
    
    # Находим файл
    result = await db.execute(
        select(File).where(File.id == file_id)
    )
    file = result.scalars().first()
    
    if not file:
        raise HTTPException(status_code=404, detail="Файл не найден")
    
    # Проверяем, есть ли уже анализ
    existing_analysis = await db.execute(
        select(Analysis).where(Analysis.file_id == file_id)
    )
    if existing_analysis.scalars().first():
        raise HTTPException(status_code=400, detail="Анализ уже выполнен для этого файла")
    
    # Выполняем mock AI-анализ
    analysis_result = mock_ai_analysis(
        file_name=file.original_name,
        file_size=file.file_size,
        version=file.version
    )
    
    # Сохраняем результат
    db_analysis = Analysis(
        file_id=file_id,
        result=analysis_result
    )
    
    db.add(db_analysis)
    await db.commit()
    await db.refresh(db_analysis)
    
    return db_analysis

@app.get("/files/{file_id}/analysis", response_model=AnalysisResponse)
async def get_analysis(
    file_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Получение результата анализа файла"""
    
    result = await db.execute(
        select(Analysis).where(Analysis.file_id == file_id)
    )
    analysis = result.scalars().first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Анализ не найден")
    
    return analysis

@app.get("/")
async def root():
    return {"message": "Documents API. Используйте /docs для документации"}
