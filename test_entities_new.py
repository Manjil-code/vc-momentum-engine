from scout.entity_loader import EntityLoader

loader = EntityLoader()
entities = loader.load()

print(f"Total loaded: {len(entities)}")
print(entities[:3])
