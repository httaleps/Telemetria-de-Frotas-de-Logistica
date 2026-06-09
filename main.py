from crud import inserir_leitura, ler_bucket, listar_todos, deletar_bucket

print("=" * 55)
print("  DEMONSTRAÇÃO DO CRUD - BUCKET PATTERN")
print("=" * 55)

print("\nInserindo leituras do sensor (a cada 10s)...")
inserir_leitura("CAM_IVECO_8H54", "EQY-8H54", "Tales Sousa", "23:18:00", -15, 85.0, "2026-06-08")
inserir_leitura("CAM_IVECO_8H54", "EQY-8H54", "Tales Sousa", "23:18:10", -16, 85.5, "2026-06-08")
inserir_leitura("CAM_IVECO_8H54", "EQY-8H54", "Tales Sousa", "23:18:20", -15, 85.0, "2026-06-08")
inserir_leitura("CAM_IVECO_8H54", "EQY-8H54", "Tales Sousa", "23:18:30", -14, 86.0, "2026-06-08")

print("\nBuscando bucket para o relatório diário...")
bucket = ler_bucket("CAM_IVECO_8H54", "2026-06-08")

print("\nTodos os buckets salvos:")
listar_todos()

print("\nDeletando bucket (simulando dado inválido)...")
deletar_bucket("CAM_IVECO_8H54", "2026-06-08")

print("\nApós deletar:")
listar_todos()

print("\n" + "=" * 55)