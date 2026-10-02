# Muzz_Factory_UMB.py
# Módulo de lógica para el generador de plantillas papercraft UMB
from PIL import Image
import os
import io
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# ============================================
# CONFIGURACIÓN DE PÁGINAS
# ============================================

TAMANO_PAGINA = (512, 724)
TAMANO_PDF = (1024, 1448)

# Colores sólidos para Página 5
COLORES_FONDO_P5 = {
    "BLANCO": (255, 255, 255),
    "NEGRO": (0, 0, 0),
    "GRIS": (128, 128, 128),
    "ROSA": (209, 74, 222),
    "VERDE": (70, 163, 77),
}

# -------------------------------------------------
# SUPERPOSICIÓN 3D
# -------------------------------------------------
SUPERPOSICION_3D = {
    "capa_1": {"skin": (16, 32, 40, 48), "posicion": (16, 16, 40, 32)},
    "capa_2": {"skin": (40, 32, 56, 48), "posicion": (40, 16, 56, 32)},
    "capa_3": {"skin": (48, 48, 64, 64), "posicion": (32, 48, 48, 64)},
    "capa_4": {"skin": (0, 32, 16, 48),  "posicion": (0, 16, 16, 32)},
    "capa_5": {"skin": (0, 48, 16, 64),  "posicion": (16, 48, 32, 64)},
}

# -------------------------------------------------
# PÁGINA 1
# -------------------------------------------------
PAGINA_1 = {
    "cabeza_frente":  {"skin": (0, 0, 24, 16), "plantilla": (156, 92, 348, 220)},
    "cabeza_atras":   {"skin": (24, 8, 32, 16), "plantilla": (220, 28, 284, 92), "transform": "rotar_180"},
    "cabeza_abajo":   {"skin": (16, 0, 24, 8), "plantilla": (220, 220, 284, 284), "transform": "voltear_vertical"},

    "torso_central":   {"skin": (16, 16, 40, 28), "plantilla": (188, 316, 380, 412)},
    "torso_hombro_i":  {"skin": (16, 20, 20, 24), "plantilla": (116, 348, 148, 380)},
    "torso_hombro_d":  {"skin": (28, 20, 32, 24), "plantilla": (404, 324, 436, 356)},
    "torso_cintura_i": {"skin": (16, 24, 20, 28), "plantilla": (433, 457, 465, 489)},
    "torso_cintura_d": {"skin": (28, 24, 32, 28), "plantilla": (465, 457, 497, 489)},

    "brazo_normal_i":  {"skin": (52, 20, 56, 24), "plantilla": (19, 483, 51, 515), "tipo": "normal"},
    "brazo_normal_d":  {"skin": (44, 52, 48, 56), "plantilla": (59, 483, 91, 515), "tipo": "normal"},

    "brazo_slim_i":    {"skin": (51, 20, 54, 23), "plantilla": (23, 487, 47, 511), "tipo": "slim"},
    "brazo_slim_d":    {"skin": (43, 52, 46, 55), "plantilla": (63, 487, 87, 511), "tipo": "slim"},

    "estirar_1":       {"origen": (220, 411, 284, 412), "destino": (220, 412, 284, 467)},
}

# -------------------------------------------------
# PÁGINA 2
# -------------------------------------------------
PAGINA_2 = {
    "cadera_1":  {"skin": (16, 24, 32, 29), "plantilla": (20, 76, 148, 116)},
    "cadera_2":  {"skin": (32, 28, 40, 29), "plantilla": (52, 148, 116, 156), "transform": "rotar_180"},
    "cadera_3":  {"skin": (20, 29, 28, 30), "plantilla": (172, 100, 236, 108)},
    "cadera_4":  {"skin": (16, 29, 20, 30), "plantilla": (164, 68, 172, 100), "transform": "rotar_90_izq"},
    "cadera_5":  {"skin": (28, 29, 32, 30), "plantilla": (236, 68, 244, 100), "transform": "rotar_90_der"},
    "cadera_6":  {"skin": (32, 29, 40, 30), "plantilla": (172, 60, 236, 68), "transform": "rotar_180"},
    "cadera_7":  {"skin": (20, 30, 28, 32), "plantilla": (276, 68, 340, 84)},
    "cadera_8":  {"skin": (16, 30, 20, 32), "plantilla": (260, 36, 276, 68), "transform": "rotar_90_der"},
    "cadera_9":  {"skin": (28, 30, 32, 32), "plantilla": (340, 36, 356, 68), "transform": "rotar_90_izq"},
    "cadera_10": {"skin": (32, 30, 40, 32), "plantilla": (276, 20, 340, 36), "transform": "rotar_180"},
    "cadera_11": {"skin": (28, 16, 36, 20), "plantilla": (276, 84, 340, 116), "transform": "voltear_vertical"},

    "pierna_1":  {"skin": (4, 16, 8, 20), "plantilla": (68, 204, 100, 236)},
    "pierna_2":  {"skin": (0, 20, 4, 24), "plantilla": (35, 204, 67, 236), "transform": "rotar_90_der"},
    "pierna_3":  {"skin": (8, 20, 12, 24), "plantilla": (101, 204, 133, 236), "transform": "rotar_90_izq"},
    "pierna_4":  {"skin": (0, 20, 16, 24), "plantilla": (36, 332, 164, 364)},
    "pierna_5":  {"skin": (0, 24, 16, 29), "plantilla": (36, 452, 165, 492)},
    "pierna_6":  {"skin": (0, 24, 16, 32), "plantilla": (36, 548, 164, 612)},
    "pierna_7":  {"skin": (8, 16, 12, 20), "plantilla": (100, 612, 132, 644), "transform": "voltear_vertical", "rotar": "rotar_90_izq"},
    "pierna_8":  {"skin": (20, 48, 24, 52), "plantilla": (236, 204, 268, 236)},
    "pierna_9":  {"skin": (16, 52, 20, 56), "plantilla": (203, 204, 235, 236), "transform": "rotar_90_der"},
    "pierna_10": {"skin": (24, 52, 28, 56), "plantilla": (269, 204, 301, 236), "transform": "rotar_90_izq"},
    "pierna_11": {"skin": (16, 52, 28, 56), "plantilla": (204, 332, 300, 364)},
    "pierna_12": {"skin": (28, 52, 32, 56), "plantilla": (172, 332, 204, 364)},
    "pierna_13": {"skin": (16, 56, 28, 61), "plantilla": (204, 452, 300, 492)},
    "pierna_14": {"skin": (28, 56, 32, 61), "plantilla": (172, 452, 204, 492)},
    "pierna_15": {"skin": (16, 56, 28, 64), "plantilla": (204, 548, 300, 612)},
    "pierna_16": {"skin": (28, 56, 32, 64), "plantilla": (172, 548, 204, 612)},
    "pierna_17": {"skin": (24, 48, 28, 52), "plantilla": (204, 612, 236, 644), "transform": "voltear_vertical", "rotar": "rotar_90_der"},

    "estirar_1":  {"origen": (68, 332, 100, 334), "destino": (68, 268, 100, 332)},
    "estirar_2":  {"origen": (132, 332, 164, 334), "destino": (132, 308, 164, 332)},
    "estirar_3":  {"origen": (172, 332, 204, 334), "destino": (172, 308, 204, 332)},
    "estirar_4":  {"origen": (236, 332, 268, 334), "destino": (236, 268, 268, 332)},
    "estirar_5":  {"origen": (68, 491, 100, 492), "destino": (68, 492, 100, 540)},
    "estirar_6":  {"origen": (236, 490, 268, 492), "destino": (236, 492, 268, 540)},
}

# -------------------------------------------------
# PÁGINA 3 - NORMAL
# -------------------------------------------------
PAGINA_3_NORMAL = {
    "brazo_n1a": {"skin": (40, 20, 52, 24), "plantilla": (60, 76, 156, 108)},
    "brazo_n1b": {"skin": (40, 20, 52, 24), "plantilla": (60, 388, 156, 420)},
    "brazo_n2a": {"skin": (52, 20, 56, 24), "plantilla": (28, 76, 60, 108)},
    "brazo_n2b": {"skin": (52, 20, 56, 24), "plantilla": (28, 388, 60, 420)},
    "brazo_n3a": {"skin": (44, 16, 48, 20), "plantilla": (60, 44, 92, 76), "transform": "rotar_90_izq"},
    "brazo_n3b": {"skin": (44, 16, 48, 20), "plantilla": (60, 356, 92, 388), "transform": "rotar_90_izq"},
    "brazo_n4a": {"skin": (40, 24, 44, 28), "plantilla": (116, 132, 148, 164), "transform": "rotar_90_der"},
    "brazo_n4b": {"skin": (40, 24, 44, 28), "plantilla": (116, 444, 148, 476), "transform": "rotar_90_der"},
    "brazo_n5a": {"skin": (48, 24, 52, 28), "plantilla": (180, 132, 212, 164), "transform": "rotar_90_izq"},
    "brazo_n5b": {"skin": (48, 24, 52, 28), "plantilla": (180, 444, 212, 476), "transform": "rotar_90_izq"},
    "brazo_n6a": {"skin": (52, 24, 56, 26), "plantilla": (148, 116, 180, 132), "transform": "rotar_180"},
    "brazo_n6b": {"skin": (52, 24, 56, 26), "plantilla": (148, 428, 180, 444), "transform": "rotar_180"},
    "brazo_n7a": {"skin": (40, 24, 56, 32), "plantilla": (28, 212, 156, 276)},
    "brazo_n7b": {"skin": (40, 24, 56, 32), "plantilla": (28, 524, 156, 588)},
    "brazo_n8a": {"skin": (48, 16, 52, 20), "plantilla": (60, 276, 92, 308), "transform": "voltear_vertical"},
    "brazo_n8b": {"skin": (48, 16, 52, 20), "plantilla": (60, 588, 92, 620), "transform": "voltear_vertical"},

    "brazo_n9a":  {"skin": (32, 52, 48, 56), "plantilla": (356, 76, 484, 108)},
    "brazo_n9b":  {"skin": (32, 52, 48, 56), "plantilla": (356, 388, 484, 420)},
    "brazo_n10a": {"skin": (36, 48, 40, 52), "plantilla": (420, 44, 452, 76), "transform": "rotar_90_der"},
    "brazo_n10b": {"skin": (36, 48, 40, 52), "plantilla": (420, 356, 452, 388), "transform": "rotar_90_der"},
    "brazo_n11a": {"skin": (32, 56, 36, 60), "plantilla": (300, 132, 332, 164), "transform": "rotar_90_der"},
    "brazo_n11b": {"skin": (32, 56, 36, 60), "plantilla": (300, 444, 332, 476), "transform": "rotar_90_der"},
    "brazo_n12a": {"skin": (40, 56, 44, 60), "plantilla": (364, 132, 396, 164), "transform": "rotar_90_izq"},
    "brazo_n12b": {"skin": (40, 56, 44, 60), "plantilla": (364, 444, 396, 476), "transform": "rotar_90_izq"},
    "brazo_n13a": {"skin": (44, 56, 48, 58), "plantilla": (332, 116, 364, 132), "transform": "rotar_180"},
    "brazo_n13b": {"skin": (44, 56, 48, 58), "plantilla": (332, 428, 364, 444), "transform": "rotar_180"},
    "brazo_n14a": {"skin": (32, 56, 44, 64), "plantilla": (388, 212, 484, 276)},
    "brazo_n14b": {"skin": (32, 56, 44, 64), "plantilla": (388, 524, 484, 588)},
    "brazo_n15a": {"skin": (44, 56, 48, 64), "plantilla": (356, 212, 388, 276)},
    "brazo_n15b": {"skin": (44, 56, 48, 64), "plantilla": (356, 524, 388, 588)},
    "brazo_n16a": {"skin": (40, 48, 44, 52), "plantilla": (420, 276, 452, 308), "transform": "voltear_vertical"},
    "brazo_n16b": {"skin": (40, 48, 44, 52), "plantilla": (420, 588, 452, 620), "transform": "voltear_vertical"},

    "estirar_n1":  {"origen": (60, 44, 92, 46), "destino": (60, 22, 92, 44)},
    "estirar_n2":  {"origen": (60, 212, 92, 214), "destino": (60, 163, 92, 212)},
    "estirar_n3":  {"origen": (124, 212, 156, 214), "destino": (124, 195, 156, 212)},
    "estirar_n4":  {"origen": (60, 356, 92, 358), "destino": (60, 334, 92, 356)},
    "estirar_n5":  {"origen": (60, 524, 92, 526), "destino": (60, 475, 92, 524)},
    "estirar_n6":  {"origen": (124, 524, 156, 526), "destino": (124, 507, 156, 524)},
    "estirar_n7":  {"origen": (420, 44, 452, 46), "destino": (420, 22, 452, 44)},
    "estirar_n8":  {"origen": (356, 212, 388, 214), "destino": (356, 195, 388, 212)},
    "estirar_n9":  {"origen": (420, 212, 452, 214), "destino": (420, 163, 452, 212)},
    "estirar_n10": {"origen": (420, 356, 452, 358), "destino": (420, 334, 452, 356)},
    "estirar_n11": {"origen": (356, 524, 388, 526), "destino": (356, 507, 388, 524)},
    "estirar_n12": {"origen": (420, 524, 452, 526), "destino": (420, 475, 452, 524)},
}

# -------------------------------------------------
# PÁGINA 3 - SLIM
# -------------------------------------------------
PAGINA_3_SLIM = {
    "brazo_s1a": {"skin": (40, 20, 51, 24), "plantilla": (52, 76, 140, 108)},
    "brazo_s1b": {"skin": (40, 20, 51, 24), "plantilla": (52, 388, 140, 420)},
    "brazo_s2a": {"skin": (51, 20, 54, 24), "plantilla": (28, 76, 52, 108)},
    "brazo_s2b": {"skin": (51, 20, 54, 24), "plantilla": (28, 388, 52, 420)},
    "brazo_s3a": {"skin": (44, 16, 47, 20), "plantilla": (52, 52, 84, 76), "transform": "rotar_90_izq"},
    "brazo_s3b": {"skin": (44, 16, 47, 20), "plantilla": (52, 364, 84, 388), "transform": "rotar_90_izq"},
    "brazo_s4a": {"skin": (40, 24, 44, 28), "plantilla": (116, 132, 148, 164), "transform": "rotar_90_der"},
    "brazo_s4b": {"skin": (40, 24, 44, 28), "plantilla": (116, 444, 148, 476), "transform": "rotar_90_der"},
    "brazo_s5a": {"skin": (47, 24, 51, 28), "plantilla": (172, 132, 204, 164), "transform": "rotar_90_izq"},
    "brazo_s5b": {"skin": (47, 24, 51, 28), "plantilla": (172, 444, 204, 476), "transform": "rotar_90_izq"},
    "brazo_s6a": {"skin": (51, 24, 54, 26), "plantilla": (148, 116, 172, 132), "transform": "rotar_180"},
    "brazo_s6b": {"skin": (51, 24, 54, 26), "plantilla": (148, 428, 172, 444), "transform": "rotar_180"},
    "brazo_s7a": {"skin": (40, 24, 54, 32), "plantilla": (28, 212, 140, 276)},
    "brazo_s7b": {"skin": (40, 24, 54, 32), "plantilla": (28, 524, 140, 588)},
    "brazo_s8a": {"skin": (47, 16, 50, 20), "plantilla": (60, 276, 84, 308), "transform": "voltear_vertical"},
    "brazo_s8b": {"skin": (47, 16, 50, 20), "plantilla": (60, 588, 84, 620), "transform": "voltear_vertical"},

    "brazo_s9a":  {"skin": (32, 52, 46, 56), "plantilla": (372, 76, 484, 108)},
    "brazo_s9b":  {"skin": (32, 52, 46, 56), "plantilla": (372, 388, 484, 420)},
    "brazo_s10a": {"skin": (36, 48, 39, 52), "plantilla": (428, 52, 460, 76), "transform": "rotar_90_der"},
    "brazo_s10b": {"skin": (36, 48, 39, 52), "plantilla": (428, 364, 460, 388), "transform": "rotar_90_der"},
    "brazo_s11a": {"skin": (32, 56, 36, 60), "plantilla": (308, 132, 340, 164), "transform": "rotar_90_der"},
    "brazo_s11b": {"skin": (32, 56, 36, 60), "plantilla": (308, 444, 340, 476), "transform": "rotar_90_der"},
    "brazo_s12a": {"skin": (39, 56, 43, 60), "plantilla": (364, 132, 396, 164), "transform": "rotar_90_izq"},
    "brazo_s12b": {"skin": (39, 56, 43, 60), "plantilla": (364, 444, 396, 476), "transform": "rotar_90_izq"},
    "brazo_s13a": {"skin": (43, 56, 46, 58), "plantilla": (340, 116, 364, 132), "transform": "rotar_180"},
    "brazo_s13b": {"skin": (43, 56, 46, 58), "plantilla": (340, 428, 364, 444), "transform": "rotar_180"},
    "brazo_s14a": {"skin": (32, 56, 43, 64), "plantilla": (396, 212, 484, 276)},
    "brazo_s14b": {"skin": (32, 56, 43, 64), "plantilla": (396, 524, 484, 588)},
    "brazo_s15a": {"skin": (43, 56, 46, 64), "plantilla": (372, 212, 396, 276)},
    "brazo_s15b": {"skin": (43, 56, 46, 64), "plantilla": (372, 524, 396, 588)},
    "brazo_s16a": {"skin": (39, 48, 42, 52), "plantilla": (428, 276, 452, 308), "transform": "voltear_vertical"},
    "brazo_s16b": {"skin": (39, 48, 42, 52), "plantilla": (428, 588, 452, 620), "transform": "voltear_vertical"},

    "estirar_s1":  {"origen": (52, 52, 84, 54), "destino": (52, 22, 84, 52)},
    "estirar_s2":  {"origen": (60, 212, 84, 214), "destino": (60, 163, 84, 212)},
    "estirar_s3":  {"origen": (116, 212, 140, 214), "destino": (116, 195, 140, 212)},
    "estirar_s4":  {"origen": (52, 364, 84, 366), "destino": (52, 334, 84, 364)},
    "estirar_s5":  {"origen": (60, 524, 84, 526), "destino": (60, 475, 84, 524)},
    "estirar_s6":  {"origen": (116, 524, 140, 526), "destino": (116, 507, 140, 524)},
    "estirar_s7":  {"origen": (428, 52, 460, 54), "destino": (428, 22, 460, 52)},
    "estirar_s8":  {"origen": (372, 212, 396, 214), "destino": (372, 195, 396, 212)},
    "estirar_s9":  {"origen": (428, 212, 452, 214), "destino": (428, 163, 452, 212)},
    "estirar_s10": {"origen": (428, 364, 460, 366), "destino": (428, 334, 460, 364)},
    "estirar_s11": {"origen": (372, 524, 396, 526), "destino": (372, 507, 396, 524)},
    "estirar_s12": {"origen": (428, 524, 452, 526), "destino": (428, 475, 452, 524)},
}

# -------------------------------------------------
# PÁGINA 4 - SOLO CAPA
# -------------------------------------------------
PAGINA_4 = {}

# -------------------------------------------------
# PÁGINA 5
# -------------------------------------------------
PAGINA_5 = {
    "cabeza3d_1a": {"skin": (32, 0, 56, 16), "plantilla": (36, 492, 228, 620)},
    "cabeza3d_1b": {"skin": (32, 0, 56, 16), "plantilla": (268, 100, 484, 244)},
    "cabeza3d_2": {"skin": (40, 8, 48, 16), "plantilla": (92, 252, 164, 324)},
    "cabeza3d_3a": {"skin": (40, 0, 48, 16), "plantilla": (92, 92, 164, 236)},
    "cabeza3d_3b": {"skin": (40, 0, 48, 16), "plantilla": (340, 340, 412, 484), "transform": "rotar_180"},
    "cabeza3d_4a": {"skin": (32, 8, 40, 16), "plantilla": (20, 92, 92, 164), "transform": "rotar_90_der"},
    "cabeza3d_4b": {"skin": (32, 8, 40, 16), "plantilla": (20, 324, 92, 396), "transform": "rotar_90_izq"},
    "cabeza3d_4c": {"skin": (32, 8, 40, 16), "plantilla": (412, 484, 484, 556)},
    "cabeza3d_5a": {"skin": (48, 8, 56, 16), "plantilla": (164, 92, 236, 164), "transform": "rotar_90_izq"},
    "cabeza3d_5b": {"skin": (48, 8, 56, 16), "plantilla": (164, 324, 236, 396), "transform": "rotar_90_der"},
    "cabeza3d_6": {"skin": (48, 8, 64, 16), "plantilla": (268, 484, 412, 556)},
    "cabeza3d_7a": {"skin": (56, 8, 64, 16), "plantilla": (92, 20, 164, 92), "transform": "rotar_180"},
    "cabeza3d_7b": {"skin": (56, 8, 64, 16), "plantilla": (340, 28, 412, 100), "transform": "rotar_180"},
    "cabeza3d_7c": {"skin": (56, 8, 64, 16), "plantilla": (92, 396, 164, 468), "transform": "rotar_180"},
    "cabeza3d_8a": {"skin": (48, 0, 56, 8), "plantilla": (92, 324, 164, 396), "transform": "voltear_vertical"},
    "cabeza3d_8b": {"skin": (48, 0, 56, 8), "plantilla": (340, 244, 412, 316), "transform": "voltear_vertical"},
    "cabeza3d_8c": {"skin": (48, 0, 56, 8), "plantilla": (340, 556, 412, 628), "transform": "voltear_vertical", "rotar": "rotar_180"},
}

# ============================================
# CLASE PRINCIPAL
# ============================================

class UMB_Generator:
    def __init__(self):
        self.skin_original = None
        self.skin_trabajo = None
        self.skin_tipo = None
        self.skin_path = None
        self.plantillas = {1: None, 2: None, 3: None, 4: None, 5: None}
        self.capas = self.cargar_capas()
        self.capas_extra = self.cargar_capas_extra()
        self.capas_cape = self.cargar_capas_cape()
        self.modo_slim = False
        
        self.modo_borde = False
        self.bordes_activos = {1: False, 2: False, 3: False}
        
        self.modo_croma = False
        self.cromas_colores = {1: "OFF", 2: "OFF", 3: "OFF", 5: "OFF"}
        
        self.modo_fondo_p5 = "DESACTIVADO"
        self.capas_cape_activas = {1: False, 2: False, 3: False, 4: False, 5: False}
    
    def _ruta_recurso(self, nombre):
        """Busca un recurso en static/ o en la carpeta actual."""
        posibles = [
            os.path.join("static", nombre),
            nombre,
            os.path.join(os.path.dirname(__file__), "static", nombre),
            os.path.join(os.path.dirname(__file__), nombre),
        ]
        for p in posibles:
            if os.path.exists(p):
                return p
        return None
    
    def cargar_capas(self):
        capas = {}
        for i in range(1, 6):
            ruta = self._ruta_recurso(f"CSP{i}.png")
            capas[f"{i}_normal"] = Image.open(ruta).convert("RGBA") if ruta else None
        
        ruta = self._ruta_recurso("CSP1_slim.png")
        capas["1_slim"] = Image.open(ruta).convert("RGBA") if ruta else None
        
        ruta = self._ruta_recurso("CSP3_slim.png")
        capas["3_slim"] = Image.open(ruta).convert("RGBA") if ruta else None
        
        return capas
    
    def cargar_capas_extra(self):
        extras = {}
        
        bordes = [
            ("line1.png", "borde_1"),
            ("line2.png", "borde_2"),
            ("line3.png", "borde_3"),
            ("line3_slim.png", "borde_3_slim"),
        ]
        for archivo, clave in bordes:
            ruta = self._ruta_recurso(archivo)
            extras[clave] = Image.open(ruta).convert("RGBA") if ruta else None
        
        cromas = [
            ("c1_b.png", "croma_1_NEGRO"), ("c1_g.png", "croma_1_VERDE"), ("c1_p.png", "croma_1_ROSA"),
            ("c2_b.png", "croma_2_NEGRO"), ("c2_g.png", "croma_2_VERDE"), ("c2_p.png", "croma_2_ROSA"),
            ("c3_b.png", "croma_3_NEGRO"), ("c3_g.png", "croma_3_VERDE"), ("c3_p.png", "croma_3_ROSA"),
            ("c3_b_slim.png", "croma_3_NEGRO_slim"), ("c3_g_slim.png", "croma_3_VERDE_slim"), ("c3_p_slim.png", "croma_3_ROSA_slim"),
            ("c5_b.png", "croma_5_NEGRO"), ("c5_g.png", "croma_5_VERDE"), ("c5_p.png", "croma_5_ROSA"),
        ]
        for archivo, clave in cromas:
            ruta = self._ruta_recurso(archivo)
            extras[clave] = Image.open(ruta).convert("RGBA") if ruta else None
        
        return extras
    
    def cargar_capas_cape(self):
        capas = {}
        for i in range(1, 6):
            ruta = self._ruta_recurso(f"cape{i}.png")
            capas[i] = Image.open(ruta).convert("RGBA") if ruta else None
        return capas
    
    def importar_skin(self, path):
        self.skin_path = path
        self.skin_original = Image.open(path).convert("RGBA")
        w, h = self.skin_original.size
        
        if w == 64 and h == 64:
            self.skin_tipo = "clasica"
        elif w == 128 and h == 128:
            self.skin_tipo = "bedrock"
        else:
            raise ValueError("La skin debe ser 64×64 o 128×128")
        
        return self.skin_tipo
    
    def aplicar_superposicion_3d(self):
        if not self.skin_original:
            return None
        
        skin_modificada = self.skin_original.copy()
        factor = 1 if self.skin_tipo == "clasica" else 2
        
        for nombre, datos in SUPERPOSICION_3D.items():
            x1, y1, x2, y2 = datos["skin"]
            x1, y1, x2, y2 = x1*factor, y1*factor, x2*factor, y2*factor
            
            if x2 <= x1 or y2 <= y1:
                continue
            
            capa = self.skin_original.crop((x1, y1, x2, y2))
            
            px1, py1, px2, py2 = datos["posicion"]
            px1, py1, px2, py2 = px1*factor, py1*factor, px2*factor, py2*factor
            
            ancho = px2 - px1
            alto = py2 - py1
            if ancho > 0 and alto > 0:
                capa = capa.resize((ancho, alto), Image.NEAREST)
                skin_modificada.paste(capa, (px1, py1), capa)
        
        self.skin_trabajo = skin_modificada
        return skin_modificada
    
    def aplicar_estirar(self, plantilla, estiramientos):
        for nombre, datos in estiramientos.items():
            x1, y1, x2, y2 = datos["origen"]
            dx1, dy1, dx2, dy2 = datos["destino"]
            
            region = plantilla.crop((x1, y1, x2, y2))
            ancho = dx2 - dx1
            alto = dy2 - dy1
            
            if ancho > 0 and alto > 0:
                region = region.resize((ancho, alto), Image.NEAREST)
                plantilla.paste(region, (dx1, dy1), region)
        
        return plantilla
    
    def aplicar_capas_extra(self, plantilla, pagina):
        if self.modo_borde and self.bordes_activos.get(pagina, False):
            if pagina == 1:
                clave = "borde_1"
            elif pagina == 2:
                clave = "borde_2"
            elif pagina == 3:
                clave = "borde_3_slim" if self.modo_slim else "borde_3"
            else:
                clave = None
            
            if clave and self.capas_extra.get(clave):
                capa = self.capas_extra[clave]
                if capa.size == TAMANO_PAGINA:
                    plantilla = Image.alpha_composite(plantilla, capa)
        
        if self.modo_croma:
            color = self.cromas_colores.get(pagina, "OFF")
            if color != "OFF":
                if pagina == 1:
                    clave = f"croma_1_{color}"
                elif pagina == 2:
                    clave = f"croma_2_{color}"
                elif pagina == 3:
                    clave = f"croma_3_{color}_slim" if self.modo_slim else f"croma_3_{color}"
                elif pagina == 5:
                    clave = f"croma_5_{color}"
                else:
                    clave = None
                
                if clave and self.capas_extra.get(clave):
                    capa = self.capas_extra[clave]
                    if capa.size == TAMANO_PAGINA:
                        plantilla = Image.alpha_composite(plantilla, capa)
        
        return plantilla
    
    def aplicar_capas_cape(self, plantilla):
        for i in range(1, 6):
            if self.capas_cape_activas.get(i, False) and self.capas_cape.get(i):
                capa = self.capas_cape[i]
                if capa.size == TAMANO_PAGINA:
                    plantilla = Image.alpha_composite(plantilla, capa)
        return plantilla
    
    def generar_pagina(self, numero_pagina, coordenadas):
        if not self.skin_trabajo:
            return None
        
        factor = 1 if self.skin_tipo == "clasica" else 2
        
        if numero_pagina == 5 and self.modo_fondo_p5 != "DESACTIVADO":
            color = COLORES_FONDO_P5[self.modo_fondo_p5]
            plantilla = Image.new('RGBA', TAMANO_PAGINA, color)
        else:
            plantilla = Image.new('RGBA', TAMANO_PAGINA, 'white')
        
        if numero_pagina != 4:
            for nombre, datos in coordenadas.items():
                if "estirar" in nombre:
                    continue
                
                if numero_pagina in [1, 3]:
                    if datos.get("tipo") == "normal" and self.modo_slim:
                        continue
                    if datos.get("tipo") == "slim" and not self.modo_slim:
                        continue
                
                x1, y1, x2, y2 = datos["skin"]
                x1, y1, x2, y2 = x1*factor, y1*factor, x2*factor, y2*factor
                
                if x2 <= x1 or y2 <= y1:
                    continue
                
                cara = self.skin_trabajo.crop((x1, y1, x2, y2))
                
                transform = datos.get("transform")
                if transform == "rotar_180":
                    cara = cara.rotate(180)
                elif transform == "rotar_90_izq":
                    cara = cara.rotate(90, expand=True)
                elif transform == "rotar_90_der":
                    cara = cara.rotate(-90, expand=True)
                elif transform == "voltear_vertical":
                    cara = cara.transpose(Image.FLIP_TOP_BOTTOM)
                
                if "rotar" in datos:
                    rot = datos["rotar"]
                    if rot == "rotar_90_izq":
                        cara = cara.rotate(90, expand=True)
                    elif rot == "rotar_90_der":
                        cara = cara.rotate(-90, expand=True)
                
                px1, py1, px2, py2 = datos["plantilla"]
                ancho = px2 - px1
                alto = py2 - py1
                
                if ancho <= 0 or alto <= 0:
                    continue
                
                cara = cara.resize((ancho, alto), Image.NEAREST)
                plantilla.paste(cara, (px1, py1), cara)
            
            estiramientos = {k: v for k, v in coordenadas.items() if "estirar" in k}
            plantilla = self.aplicar_estirar(plantilla, estiramientos)
        
        # Aplicar capa CSP
        if numero_pagina == 1:
            capa = self.capas.get("1_slim") if (self.modo_slim and self.capas.get("1_slim")) else self.capas.get("1_normal")
        elif numero_pagina == 2:
            capa = self.capas.get("2_normal")
        elif numero_pagina == 3:
            capa = self.capas.get("3_slim") if (self.modo_slim and self.capas.get("3_slim")) else self.capas.get("3_normal")
        elif numero_pagina == 4:
            capa = self.capas.get("4_normal")
        elif numero_pagina == 5:
            capa = self.capas.get("5_normal")
        else:
            capa = None
        
        if capa and capa.size == TAMANO_PAGINA:
            plantilla = Image.alpha_composite(plantilla, capa)
        
        plantilla = self.aplicar_capas_extra(plantilla, numero_pagina)
        
        if numero_pagina == 5 and self.modo_fondo_p5 != "DESACTIVADO":
            plantilla = self.aplicar_capas_cape(plantilla)
        
        return plantilla
    
    def generar_todas(self):
        if not self.skin_original:
            return
        
        self.aplicar_superposicion_3d()
        
        self.plantillas[1] = self.generar_pagina(1, PAGINA_1)
        self.plantillas[2] = self.generar_pagina(2, PAGINA_2)
        
        if self.modo_slim:
            self.plantillas[3] = self.generar_pagina(3, PAGINA_3_SLIM)
        else:
            self.plantillas[3] = self.generar_pagina(3, PAGINA_3_NORMAL)
        
        self.plantillas[4] = self.generar_pagina(4, PAGINA_4)
        self.plantillas[5] = self.generar_pagina(5, PAGINA_5)
    
    def exportar_pdf_memoria(self, buffer):
        """Exporta todas las páginas a un PDF en memoria (para web)."""
        if not any(self.plantillas.values()):
            return False
        
        c = canvas.Canvas(buffer, pagesize=(TAMANO_PDF[0], TAMANO_PDF[1]))
        
        for num in range(1, 6):
            if self.plantillas[num]:
                img_pdf = self.plantillas[num].resize(TAMANO_PDF, Image.LANCZOS)
                temp_path = f"temp_pag{num}.png"
                img_pdf.save(temp_path)
                c.drawImage(ImageReader(temp_path), 0, 0, 
                           width=TAMANO_PDF[0], height=TAMANO_PDF[1])
                os.remove(temp_path)
                if num < 5:
                    c.showPage()
        
        c.save()
        return True