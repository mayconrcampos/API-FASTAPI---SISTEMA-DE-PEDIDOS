FROM python:3.11.2-bullseye

# WORKDIR /app

ENV DB_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/prova
ENV DB_URL_TESTS=postgresql+asyncpg://postgres:postgres@localhost:5432/prova_tests
ENV JWT_SECRET=8X0EzuMh7W0h1sKB-9gJ7XFbjP_4gjYkh8X11AI9n0c

COPY . .

RUN pip install --upgrade pip && pip install python-dotenv && pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app"]