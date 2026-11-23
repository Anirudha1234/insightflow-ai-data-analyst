from app.services.sql_generator import generate_sql

question = "Which 5 products generated the highest revenue in 2025?"

sql = generate_sql(question)

print("\nUSER QUESTION:")
print(question)

print("\nGENERATED SQL:")
print(sql)
