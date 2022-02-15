В Docker происходит создание tex-файла и генерация pdf. Результат лежит в `artifacts/example.pdf`. 
Чтобы достать pdf из запущенного контейнера, можно выполнить 
```bash
docker cp CONTAINER:/src/artifacts/example.pdf .
```