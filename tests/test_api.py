from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


# =========================
# FUNÇÕES AUXILIARES
# =========================

def fazer_login():
    response = client.post(
        "/auth/login",
        data={
            "username": "caua@email.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def criar_hotel(token):
    response = client.post(
        "/hoteis/",
        json={
            "nome": "Hotel Teste",
            "localizacao": "Brasília",
            "nota": 4.5
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    return response.json()["id"]


def criar_quarto(token):
    hotel_id = criar_hotel(token)

    response = client.post(
        "/quartos/",
        json={
            "numero": 301,
            "preco": 300.0,
            "disponivel": True,
            "hotel_id": hotel_id
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    return response.json()["id"]


# =========================
# AUTENTICAÇÃO
# =========================

def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["mensagem"] == "API Hoteleira funcionando com sucesso!"


def test_login_usuario():
    response = client.post(
        "/auth/login",
        data={
            "username": "caua@email.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200

    dados = response.json()

    assert "access_token" in dados
    assert dados["token_type"] == "bearer"


# =========================
# HOTÉIS
# =========================

def test_criar_hotel():
    token = fazer_login()

    response = client.post(
        "/hoteis/",
        json={
            "nome": "Hotel Teste",
            "localizacao": "Brasília",
            "nota": 4.5
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    dados = response.json()

    assert dados["nome"] == "Hotel Teste"
    assert dados["localizacao"] == "Brasília"
    assert dados["nota"] == 4.5
    assert "id" in dados


def test_listar_hoteis():
    token = fazer_login()

    response = client.get(
        "/hoteis/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_buscar_hotel():
    token = fazer_login()
    hotel_id = criar_hotel(token)

    response = client.get(
        f"/hoteis/{hotel_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    dados = response.json()

    assert dados["id"] == hotel_id


def test_atualizar_hotel():
    token = fazer_login()
    hotel_id = criar_hotel(token)

    response = client.put(
        f"/hoteis/{hotel_id}",
        json={
            "nome": "Hotel Atualizado",
            "nota": 5.0
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    dados = response.json()

    assert dados["id"] == hotel_id
    assert dados["nome"] == "Hotel Atualizado"
    assert dados["nota"] == 5.0


def test_excluir_hotel():
    token = fazer_login()
    hotel_id = criar_hotel(token)

    response = client.delete(
        f"/hoteis/{hotel_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    buscar = client.get(
        f"/hoteis/{hotel_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert buscar.status_code == 404


# =========================
# QUARTOS
# =========================

def test_criar_quarto():
    token = fazer_login()
    hotel_id = criar_hotel(token)

    response = client.post(
        "/quartos/",
        json={
            "numero": 101,
            "preco": 250.0,
            "disponivel": True,
            "hotel_id": hotel_id
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    dados = response.json()

    assert dados["numero"] == 101
    assert dados["preco"] == 250.0
    assert dados["disponivel"] is True
    assert dados["hotel_id"] == hotel_id
    assert "id" in dados


def test_listar_quartos():
    token = fazer_login()

    response = client.get(
        "/quartos/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_buscar_quarto():
    token = fazer_login()
    hotel_id = criar_hotel(token)

    criar = client.post(
        "/quartos/",
        json={
            "numero": 102,
            "preco": 300.0,
            "disponivel": True,
            "hotel_id": hotel_id
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert criar.status_code == 200

    quarto_id = criar.json()["id"]

    response = client.get(
        f"/quartos/{quarto_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["id"] == quarto_id


def test_atualizar_quarto():
    token = fazer_login()
    hotel_id = criar_hotel(token)

    criar = client.post(
        "/quartos/",
        json={
            "numero": 103,
            "preco": 350.0,
            "disponivel": True,
            "hotel_id": hotel_id
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert criar.status_code == 200

    quarto_id = criar.json()["id"]

    response = client.put(
        f"/quartos/{quarto_id}",
        json={
            "numero": 203,
            "preco": 400.0
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    dados = response.json()

    assert dados["numero"] == 203
    assert dados["preco"] == 400.0


def test_excluir_quarto():
    token = fazer_login()
    hotel_id = criar_hotel(token)

    criar = client.post(
        "/quartos/",
        json={
            "numero": 104,
            "preco": 200.0,
            "disponivel": True,
            "hotel_id": hotel_id
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert criar.status_code == 200

    quarto_id = criar.json()["id"]

    response = client.delete(
        f"/quartos/{quarto_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    buscar = client.get(
        f"/quartos/{quarto_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert buscar.status_code == 404


# =========================
# RESERVAS
# =========================

def test_criar_reserva():
    token = fazer_login()
    quarto_id = criar_quarto(token)

    response = client.post(
        "/reservas/",
        json={
            "hospede": "Cauã",
            "data_entrada": "2026-11-01",
            "data_saida": "2026-11-05",
            "quarto_id": quarto_id
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    dados = response.json()

    assert dados["hospede"] == "Cauã"
    assert dados["data_entrada"] == "2026-11-01"
    assert dados["data_saida"] == "2026-11-05"
    assert dados["quarto_id"] == quarto_id
    assert "id" in dados


def test_listar_reservas():
    token = fazer_login()

    response = client.get(
        "/reservas/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_buscar_reserva():
    token = fazer_login()
    quarto_id = criar_quarto(token)

    criar = client.post(
        "/reservas/",
        json={
            "hospede": "Cauã",
            "data_entrada": "2026-11-10",
            "data_saida": "2026-11-15",
            "quarto_id": quarto_id
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert criar.status_code == 200

    reserva_id = criar.json()["id"]

    response = client.get(
        f"/reservas/{reserva_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["id"] == reserva_id


def test_atualizar_reserva():
    token = fazer_login()
    quarto_id = criar_quarto(token)

    criar = client.post(
        "/reservas/",
        json={
            "hospede": "Cauã",
            "data_entrada": "2026-11-20",
            "data_saida": "2026-11-25",
            "quarto_id": quarto_id
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert criar.status_code == 200

    reserva_id = criar.json()["id"]

    response = client.put(
        f"/reservas/{reserva_id}",
        json={
            "hospede": "Cauã Atualizado"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["hospede"] == "Cauã Atualizado"


def test_excluir_reserva():
    token = fazer_login()
    quarto_id = criar_quarto(token)

    criar = client.post(
        "/reservas/",
        json={
            "hospede": "Cauã",
            "data_entrada": "2026-12-01",
            "data_saida": "2026-12-05",
            "quarto_id": quarto_id
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert criar.status_code == 200

    reserva_id = criar.json()["id"]

    response = client.delete(
        f"/reservas/{reserva_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    buscar = client.get(
        f"/reservas/{reserva_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert buscar.status_code == 404

    