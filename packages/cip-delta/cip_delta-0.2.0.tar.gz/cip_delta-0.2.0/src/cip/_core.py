import numpy as np
import hashlib
import random
import logging
from scipy.linalg import eigh, pinv
from ._internals import (
    _carregar_delta_pi,
    _construir_matriz_cossenos,
    _codificar_bloco,
    _decodificar_bloco,
    _preparar_blocos,
)

# ==== Interface Pública ====

def cip_cifrar_blocos_bytes(dados: bytes, delta_array=None, size=1024, offset=None):
    """
    Cifra os dados binários projetando cada bloco em uma base espectral derivada de Δπ(x).
    Retorna um dicionário com os vetores cifrados, offset usado e tamanho da base.
    """
    if delta_array is None:
        delta_array = _carregar_delta_pi()

    max_offset = len(delta_array) - size
    if max_offset <= 0:
        raise ValueError("Δπ(x) insuficiente para o tamanho da base solicitado.")

    if offset is None:
        offset = random.randint(0, max_offset)

    F_values = delta_array[offset:offset + size]
    x_values = np.arange(5_000_000 + offset, 5_000_000 + offset + size)
    C = _construir_matriz_cossenos(F_values, x_values)
    _, autovetores = eigh(C)
    base = autovetores[:, -size:]

    blocos = _preparar_blocos(dados, size)
    cifrado = [base @ _codificar_bloco(bloco, size) for bloco in blocos]

    return {
        'cifrado': cifrado,
        'offset': offset,
        'size': size
    }

def cip_assinar_blocos_bytes(dados: bytes, delta_array=None, size=1024, offset=None):
    """
    Gera uma lista de assinaturas SHA-256 das projeções espectrais dos blocos.
    Retorna (assinaturas, chave com offset e size).
    """
    if delta_array is None:
        delta_array = _carregar_delta_pi()

    max_offset = len(delta_array) - size
    if max_offset <= 0:
        raise ValueError("Δπ(x) insuficiente para o tamanho da base solicitado.")

    if offset is None:
        offset = random.randint(0, max_offset)

    F_values = delta_array[offset:offset + size]
    x_values = np.arange(5_000_000 + offset, 5_000_000 + offset + size)
    C = _construir_matriz_cossenos(F_values, x_values)
    _, autovetores = eigh(C)
    base = autovetores[:, -size:]
    base_inv = pinv(base)

    assinaturas = []
    for i in range(0, len(dados), size):
        bloco = dados[i:i + size].ljust(size, b'\x00')
        vetor = _codificar_bloco(bloco, size)
        projecao = base_inv @ vetor
        hash_val = hashlib.sha256(projecao.astype(np.float32).tobytes()).hexdigest()
        assinaturas.append(hash_val)

    chave = {'offset': offset, 'size': size}
    return assinaturas, chave

def cip_verificar_blocos_bytes(dados: bytes, assinaturas_ref: list, delta_array=None, offset=None, size=1024):
    """
    Verifica a integridade espectral dos blocos de dados com base nas assinaturas fornecidas.

    Retorna:
        (n_blocos_alterados, n_total_blocos)
    """
    if delta_array is None:
        delta_array = _carregar_delta_pi()

    if offset is None:
        raise ValueError("Offset deve ser fornecido para verificação.")

    if offset + size > len(delta_array):
        raise ValueError(
            f"Offset + size = {offset + size} excede o comprimento de Δπ(x) ({len(delta_array)}).\n"
            f"Diminua o offset ou o size, ou carregue um vetor Δπ mais extenso."
        )

    F_values = delta_array[offset:offset + size]
    x_values = np.arange(5_000_000 + offset, 5_000_000 + offset + size)
    C = _construir_matriz_cossenos(F_values, x_values)
    _, autovetores = eigh(C)
    base = autovetores[:, -size:]
    base_inv = pinv(base)

    alterados = 0
    for i in range(0, len(dados), size):
        bloco = dados[i:i + size].ljust(size, b'\x00')
        vetor = _codificar_bloco(bloco, size)
        projecao = base_inv @ vetor
        hash_val = hashlib.sha256(projecao.astype(np.float32).tobytes()).hexdigest()

        if i // size >= len(assinaturas_ref) or hash_val != assinaturas_ref[i // size]:
            alterados += 1

    total_blocos = (len(dados) + size - 1) // size
    return alterados, total_blocos

def cip_decifrar_blocos_bytes(data: dict, delta_array=None):
    """
    Reconstrói os dados originais a partir de um pacote cifrado (dicionário contendo
    'cifrado', 'offset' e 'size').
    """
    if delta_array is None:
        delta_array = _carregar_delta_pi()

    if 'offset' not in data or 'cifrado' not in data or 'size' not in data:
        raise ValueError("O pacote de dados está incompleto. 'cifrado', 'offset' e 'size' são obrigatórios.")

    offset = int(data['offset'])
    size = int(data['size'])

    if offset + size > len(delta_array):
        raise ValueError("Offset + size excede o comprimento do vetor Δπ(x)")

    F_values = delta_array[offset:offset + size]
    x_values = np.arange(5_000_000 + offset, 5_000_000 + offset + size)
    C = _construir_matriz_cossenos(F_values, x_values)
    _, autovetores = eigh(C)
    base = autovetores[:, -size:]
    base_inv = pinv(base)

    blocos = []
    for bloco in data['cifrado']:
        vetor_reconstruido = base_inv @ bloco
        blocos.append(_decodificar_bloco(vetor_reconstruido))

    return b''.join(blocos)

