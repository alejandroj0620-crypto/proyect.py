import logging
from abc import ABC, abstractmethod
from datetime import datetime

# ===================== LOG CONFIG =====================
logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ===================== EXCEPCIONES =====================
class SistemaError(Exception):
    pass

class ValidacionError(SistemaError):
    pass

class ReservaError(SistemaError):
    pass

# ===================== CLASE ABSTRACTA =====================
class Entidad(ABC):
    def __init__(self, id):
        self._id = id

    @abstractmethod
    def mostrar_info(self):
        pass

# ===================== CLIENTE =====================
class Cliente(Entidad):
    def __init__(self, id, nombre, email):
        super().__init__(id)
        self.nombre = nombre
        self.email = email

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor:
            raise ValidacionError("Nombre inválido")
        self._nombre = valor

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        if "@" not in valor:
            raise ValidacionError("Email inválido")
        self._email = valor

    def mostrar_info(self):
        return f"Cliente: {self.nombre} - {self.email}"

# ===================== SERVICIO =====================
class Servicio(ABC):
    def __init__(self, nombre, precio_base):
        self.nombre = nombre
        self.precio_base = precio_base

    @abstractmethod
    def calcular_costo(self, *args, **kwargs):
        pass

    @abstractmethod
    def descripcion(self):
        pass

# ===================== SERVICIOS ESPECÍFICOS =====================
class ReservaSala(Servicio):
    def calcular_costo(self, horas=1, impuestos=0):
        return (self.precio_base * horas) * (1 + impuestos)

    def descripcion(self):
        return "Reserva de sala"

class AlquilerEquipo(Servicio):
    def calcular_costo(self, dias=1, descuento=0):
        return (self.precio_base * dias) * (1 - descuento)

    def descripcion(self):
        return "Alquiler de equipo"

class Asesoria(Servicio):
    def calcular_costo(self, horas=1, tarifa_extra=0):
        return (self.precio_base * horas) + tarifa_extra

    def descripcion(self):
        return "Asesoría especializada"

# ===================== RESERVA =====================
class Reserva:
    def __init__(self, cliente, servicio, duracion):
        if not isinstance(cliente, Cliente):
            raise ReservaError("Cliente inválido")
        if not isinstance(servicio, Servicio):
            raise ReservaError("Servicio inválido")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def confirmar(self):
        try:
            if self.duracion <= 0:
                raise ReservaError("Duración inválida")
            self.estado = "Confirmada"
            logging.info("Reserva confirmada")
        except Exception as e:
            logging.error(f"Error al confirmar reserva: {e}")
            raise

    def cancelar(self):
        self.estado = "Cancelada"
        logging.info("Reserva cancelada")

    def procesar(self):
        try:
            costo = self.servicio.calcular_costo(self.duracion)
        except Exception as e:
            logging.error("Error en cálculo", exc_info=True)
            raise ReservaError("Error procesando reserva") from e
        else:
            return costo
        finally:
            logging.info("Proceso de reserva ejecutado")

# ===================== SISTEMA =====================
class Sistema:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def agregar_cliente(self, cliente):
        try:
            self.clientes.append(cliente)
        except Exception as e:
            logging.error(f"Error agregando cliente: {e}")

    def agregar_servicio(self, servicio):
        self.servicios.append(servicio)

    def crear_reserva(self, cliente, servicio, duracion):
        try:
            reserva = Reserva(cliente, servicio, duracion)
            reserva.confirmar()
            self.reservas.append(reserva)
        except Exception as e:
            logging.error(f"Error creando reserva: {e}")

# ===================== SIMULACIÓN =====================
def simulacion():
    sistema = Sistema()

    try:
        c1 = Cliente(1, "Juan", "juan@mail.com")
        c2 = Cliente(2, "", "correo_invalido")  # error
    except Exception as e:
        logging.error(f"Error cliente: {e}")

    s1 = ReservaSala("Sala", 50)
    s2 = AlquilerEquipo("Proyector", 30)
    s3 = Asesoria("Consultoría", 100)

    sistema.agregar_cliente(c1)
    sistema.agregar_servicio(s1)
    sistema.agregar_servicio(s2)
    sistema.agregar_servicio(s3)

    for i in range(10):
        try:
            sistema.crear_reserva(c1, s1, i - 5)  # genera errores también
        except Exception as e:
            logging.error(e)

    print("Simulación completada. Revisar software_fj.log")

if __name__ == "__main__":
    simulacion()
