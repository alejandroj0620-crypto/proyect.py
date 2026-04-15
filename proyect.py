import tkinter as tk
from tkinter import messagebox
from abc import ABC, abstractmethod
import datetime

# ================== LOGGER ==================
class Logger:
    @staticmethod
    def log(mensaje):
        with open("logs.txt", "a") as f:
            f.write(f"{datetime.datetime.now()} - {mensaje}\n")


# ================== EXCEPCIONES ==================
class SistemaError(Exception):
    pass

class ClienteError(SistemaError):
    pass

class ServicioError(SistemaError):
    pass

class ReservaError(SistemaError):
    pass


# ================== CLASE ABSTRACTA ==================
class Entidad(ABC):
    def __init__(self, id):
        self._id = id

    @abstractmethod
    def mostrar(self):
        pass


# ================== CLIENTE ==================
class Cliente(Entidad):
    def __init__(self, id, nombre, email):
        super().__init__(id)
        if not nombre:
            raise ClienteError("Nombre inválido")
        if "@" not in email:
            raise ClienteError("Email inválido")

        self.__nombre = nombre
        self.__email = email

    def mostrar(self):
        return f"{self.__nombre} ({self.__email})"

    def get_nombre(self):
        return self.__nombre


# ================== SERVICIO ABSTRACTO ==================
class Servicio(ABC):
    def __init__(self, nombre, precio_base):
        self.nombre = nombre
        self.precio_base = precio_base

    @abstractmethod
    def calcular_costo(self, tiempo):
        pass


# ================== SERVICIOS ==================
class ReservaSala(Servicio):
    def calcular_costo(self, horas):
        return self.precio_base * horas


class AlquilerEquipo(Servicio):
    def calcular_costo(self, dias):
        return self.precio_base * dias


class Asesoria(Servicio):
    def calcular_costo(self, horas):
        return self.precio_base * horas * 1.2


# ================== RESERVA ==================
class Reserva:
    def __init__(self, cliente, servicio, tiempo):
        if tiempo <= 0:
            raise ReservaError("Tiempo inválido")

        self.cliente = cliente
        self.servicio = servicio
        self.tiempo = tiempo
        self.estado = "Pendiente"

    def confirmar(self):
        self.estado = "Confirmada"

    def cancelar(self):
        self.estado = "Cancelada"

    def procesar(self):
        try:
            costo = self.servicio.calcular_costo(self.tiempo)
            self.confirmar()
            return costo
        except Exception as e:
            raise ReservaError("Error al procesar reserva") from e


# ================== SISTEMA ==================
class Sistema:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def agregar_cliente(self, cliente):
        self.clientes.append(cliente)

    def agregar_servicio(self, servicio):
        self.servicios.append(servicio)

    def crear_reserva(self, reserva):
        self.reservas.append(reserva)


# ================== INTERFAZ TKINTER ==================
class App:
    def __init__(self, root):
        self.sistema = Sistema()
        self.root = root
        self.root.title("Software FJ")

        # CLIENTE
        tk.Label(root, text="Nombre").grid(row=0, column=0)
        self.nombre = tk.Entry(root)
        self.nombre.grid(row=0, column=1)

        tk.Label(root, text="Email").grid(row=1, column=0)
        self.email = tk.Entry(root)
        self.email.grid(row=1, column=1)

        tk.Button(root, text="Agregar Cliente", command=self.agregar_cliente).grid(row=2, column=1)

        # RESERVA
        tk.Label(root, text="Tiempo").grid(row=3, column=0)
        self.tiempo = tk.Entry(root)
        self.tiempo.grid(row=3, column=1)

        tk.Button(root, text="Crear Reserva", command=self.crear_reserva).grid(row=4, column=1)

        # SERVICIOS POR DEFECTO
        self.sistema.agregar_servicio(ReservaSala("Sala", 50))
        self.sistema.agregar_servicio(AlquilerEquipo("Equipo", 30))
        self.sistema.agregar_servicio(Asesoria("Asesoria", 80))

    def agregar_cliente(self):
        try:
            cliente = Cliente(len(self.sistema.clientes), self.nombre.get(), self.email.get())
            self.sistema.agregar_cliente(cliente)
            messagebox.showinfo("Éxito", "Cliente agregado")
        except Exception as e:
            Logger.log(str(e))
            messagebox.showerror("Error", str(e))

    def crear_reserva(self):
        try:
            if not self.sistema.clientes:
                raise ReservaError("No hay clientes")

            cliente = self.sistema.clientes[-1]
            servicio = self.sistema.servicios[0]

            tiempo = int(self.tiempo.get())

            reserva = Reserva(cliente, servicio, tiempo)
            costo = reserva.procesar()

            self.sistema.crear_reserva(reserva)

            messagebox.showinfo("Reserva", f"Costo: {costo}")
        except Exception as e:
            Logger.log(str(e))
            messagebox.showerror("Error", str(e))


# ================== MAIN ==================
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
