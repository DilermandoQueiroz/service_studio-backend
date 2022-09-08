FROM python:3.9

WORKDIR /sql_app/

# Install Poetry
RUN pip install poetry

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /sql_app/

# Allow installing dev dependencies to run tests
# ARG INSTALL_DEV=true
# RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"
RUN poetry config virtualenvs.create false && poetry install

COPY ./sql_app /sql_app/
ENV PYTHONPATH=/sql_app/

RUN poetry shell

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]