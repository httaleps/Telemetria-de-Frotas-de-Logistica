import json
import os
from datetime import date

ARQUIVO = "leituras_db.json"

def _carregar():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)

def _salvar(db):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)

def _achar_bucket(db, caminhao_id, data):
    for i, doc in enumerate(db):
        if doc["caminhao_id"] == caminhao_id and doc["data_leitura"] == data:
            return i, doc
    return None, None

def criar_bucket(caminhao_id, placa, motorista, data=None):
   
    if data is None:
        data = str(date.today())

    db = _carregar()
    idx, existente = _achar_bucket(db, caminhao_id, data)
    if existente:
        print(f"[AVISO] Bucket já existe para {caminhao_id} em {data}.")
        return existente

    bucket = {
        "_id": f"{caminhao_id}_{data}",
        "caminhao_id": caminhao_id,
        "placa": placa,
        "motorista": motorista,
        "data_leitura": data,
        "total_leituras": 0,
        "temp_min": None,
        "temp_max": None,
        "temp_media": None,
        "leituras": []
    }
    db.append(bucket)
    _salvar(db)
    print(f"[CREATE] Bucket criado: {bucket['_id']}")
    return bucket

def inserir_leitura(caminhao_id, placa, motorista, time, temp_c, umidade, data=None):

    if data is None:
        data = str(date.today())

    db = _carregar()
    idx, bucket = _achar_bucket(db, caminhao_id, data)

    if bucket is None:
        criar_bucket(caminhao_id, placa, motorista, data)
        db = _carregar()
        idx, bucket = _achar_bucket(db, caminhao_id, data)

    nova_leitura = {"time": time, "temp_C": temp_c, "umidade": umidade}
    bucket["leituras"].append(nova_leitura)

    bucket["total_leituras"] += 1

    temps = [l["temp_C"] for l in bucket["leituras"]]
    bucket["temp_min"] = min(temps)
    bucket["temp_max"] = max(temps)
    bucket["temp_media"] = round(sum(temps) / len(temps), 2)

    db[idx] = bucket
    _salvar(db)
    print(f"[UPDATE] Leitura inserida em {bucket['_id']} | "
          f"temp={temp_c}°C | total={bucket['total_leituras']}")
    return bucket

def ler_bucket(caminhao_id, data):

    db = _carregar()
    _, bucket = _achar_bucket(db, caminhao_id, data)

    if bucket is None:
        print(f"[READ] Nenhum registro encontrado para {caminhao_id} em {data}.")
        return None

    print(f"[READ] {bucket['_id']} — {bucket['total_leituras']} leituras | "
          f"min={bucket['temp_min']}°C | max={bucket['temp_max']}°C | "
          f"média={bucket['temp_media']}°C")
    return bucket

def listar_todos():

    db = _carregar()
    if not db:
        print("[READ] Nenhum dado salvo ainda.")
        return []
    for doc in db:
        print(f"  • {doc['_id']} | {doc['total_leituras']} leituras | "
              f"motorista: {doc['motorista']}")
    return db

def deletar_bucket(caminhao_id, data):

    db = _carregar()
    idx, bucket = _achar_bucket(db, caminhao_id, data)

    if bucket is None:
        print(f"[DELETE] Bucket não encontrado: {caminhao_id} em {data}.")
        return False

    db.pop(idx)
    _salvar(db)
    print(f"[DELETE] Bucket removido: {caminhao_id}_{data}")
    return True