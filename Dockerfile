FROM python:3.13.2
WORKDIR /BudgetApp

COPY . /BudgetApp
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501
CMD ["streamlit", "run", "app.py"]