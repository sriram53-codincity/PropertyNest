import sys
with open('app/routes/application_routes.py', 'r', encoding='utf8') as f:
    content = f.read()

target = '@router.post("/", response_model=ApplicationResponse)'
print('Target 1:', target in content)

with open('app/models/pg_models.py', 'r', encoding='utf8') as f:
    content2 = f.read()

print('Target 2:', 'ForeignKey("property_nest.properties.id")' in content2)
print('Target 3:', 'ForeignKey("property_nest.users.id")' in content2)
