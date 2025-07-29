import numpy as np
import logging
from importlib import resources

# ==== Funções internas ====

def _carregar_delta_pi() -> np.ndarray:
    with resources.files("cip.dados").joinpath("delta_pi_5M_a_10M.npy").open("rb") as f:
        return np.load(f)

def _codificar_bloco(bloco, bloco_size: int) -> np.ndarray:
    """
    Converte um bloco (str, bytes, bytearray ou np.ndarray) em vetor float32 padronizado com tamanho fixo.
    - Se for string: codifica em UTF-8
    - Se for bytes ou bytearray: usa diretamente
    - Se for np.ndarray: converte e ajusta
    """
    if isinstance(bloco, np.ndarray):
        vetor = bloco.astype(np.float32)
    elif isinstance(bloco, str):
        bloco = bloco.encode("utf-8")
        vetor = np.frombuffer(bloco, dtype=np.uint8).astype(np.float32)
    elif isinstance(bloco, (bytes, bytearray)):
        vetor = np.frombuffer(bloco, dtype=np.uint8).astype(np.float32)
    else:
        raise TypeError("O bloco deve ser str, bytes, bytearray ou np.ndarray.")

    if len(vetor) > bloco_size:
        vetor = vetor[:bloco_size]
    elif len(vetor) < bloco_size:
        padding = np.zeros(bloco_size - len(vetor), dtype=np.float32)
        vetor = np.concatenate([vetor, padding])

    return vetor

def _decodificar_bloco(vetor: np.ndarray) -> bytes:
    vetor_int = np.clip(np.round(vetor), 0, 255).astype(np.uint8)
    return bytes(vetor_int)

def _construir_matriz_cossenos(F_values, x_values):
    N = len(x_values)
    C = np.zeros((N, N), dtype=np.float64)
    for i in range(N):
        for j in range(N):
            C[i, j] = np.cos(F_values[i] * np.log(x_values[j])) + np.cos(F_values[j] * np.log(x_values[i]))
    C /= np.max(np.abs(C))
    return C
    
def _preparar_blocos(dados: bytes, size: int):
    if not isinstance(dados, (bytes, bytearray)):
        raise TypeError("Dados devem estar no formato bytes ou bytearray.")
    blocos = []
    for i in range(0, len(dados), size):
        bloco = dados[i:i + size]
        bloco = bloco[:size].ljust(size, b'\x00')
        blocos.append(np.frombuffer(bloco, dtype=np.uint8))
    return blocos
    
def _empacotar_para_envio(pacote: dict, caminho: str, incluir_offset: bool = False):
    pacote_salvo = dict(pacote)  # cópia segura
    if not incluir_offset:
        pacote_salvo.pop("offset", None)
        logging.debug("Pacote exportado sem offset.")
    else:
        logging.debug(f"Pacote exportado com offset={pacote['offset']} e size={pacote['size']}")
    np.savez_compressed(caminho, **pacote_salvo)
    
def _carregar_para_decifrar(caminho: str) -> dict:
    with np.load(caminho, allow_pickle=True) as npz:
        return dict(npz)

