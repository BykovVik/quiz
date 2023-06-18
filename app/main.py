import uvicorn
import requests
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db import get_database
from pydantic_schemas import QuestionRequest
from models import Question
from typing import List

app = FastAPI()

@app.post("/questions/", response_model=List[QuestionRequest])
def create_questions(questions: QuestionRequest, db: Session = Depends(get_database)):

    created_questions = []
    for i in range(questions.questions_num):
        while True:
            # Попробуем получить случайный вопрос через API
            response = requests.get('https://jservice.io/api/random?count=1')
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Service unavailable")
            
            question_data = response.json()[0]
            # Проверяем, есть ли такой же вопрос в базе данных
            existing_question = (
                db.query(Question)
                .filter(Question.question_text == question_data['question'])
                .first()
            )
            if not existing_question:
                # Если вопрос уникальный, сохраняем его
                new_question = Question(
                    question_text=question_data['question'],
                    answer_text=question_data['answer'],
                    created_at=datetime.now(timezone.utc)
                )
                try:
                    db.add(new_question)
                    db.commit()
                    break
                except IntegrityError:
                    db.rollback()
            # Если вопрос уже есть в базе данных, попробуем получить другой вопрос

        created_questions.append(new_question)

    return created_questions

@app.get("/questions/latest", response_model=QuestionRequest)
def get_latest_question(db: Session = Depends(get_database)):
    latest_question = (
        db.query(Question)
        .order_by(Question.created_at.desc())
        .first()
    )
    if not latest_question:
        raise HTTPException(status_code=404, detail="No questions found")
    return latest_question


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)