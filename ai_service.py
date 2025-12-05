import random

def mock_ai_analysis(file_name: str, file_size: int, version: int) -> str:
    """
    Mock AI-анализ документа без использования реального OpenAI API
    """
    size_comments = [
        "Файл относительно небольшой",
        "Файл среднего размера",
        "Достаточно большой файл"
    ]
    
    version_comments = [
        "новое изменение выглядит незначительным",
        "существенные изменения в новой версии",
        "это первая версия файла" if version == 1 else "очередное обновление документа"
    ]
    
    size_kb = file_size / 1024
    
    if size_kb < 100:
        size_comment = size_comments[0]
    elif size_kb < 1000:
        size_comment = size_comments[1]
    else:
        size_comment = size_comments[2]
    
    version_comment = version_comments[random.randint(0, len(version_comments) - 1)]
    
    analysis = f"{size_comment}, {version_comment}. "
    analysis += f"Документ '{file_name}' версии {version} имеет размер {size_kb:.2f} KB."
    
    return analysis
