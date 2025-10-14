class MenuItem:
    # Clase base para todos los items del menú.
    
    def __init__(self, nombre: str, precio: float):
        self._nombre = nombre
        self._precio = precio

    def get_name(self) -> str:
        return self._nombre

    def get_price(self) -> float:
        return self._precio
    
    def set_name(self, nombre: str) -> None:
        self._nombre = nombre

    def set_price(self, precio: float) -> None:
        self._precio = precio  
    
    def get_total(self) -> float:
        # Calcular precio total para este item.
        return self._precio
    
    def __str__(self) -> str:
        return f"{self._nombre}: ${self._precio:.2f}"

class Bebida(MenuItem):
    # Bebida con opción de tamaño.
    
    def __init__(self, nombre: str, precio: float, tamaño: str = "regular") -> None:
        super().__init__(nombre, precio)
        self._tamaño = tamaño
        
        # Ajustar
        #  precio basado en el tamaño
        if tamaño == "pequeño":
            self._precio = precio * 0.8
        elif tamaño == "grande":
            self._precio = precio * 1.3

    def get_tamaño(self) -> str:
        return self._tamaño

    def set_tamaño(self, tamaño: str):
        self._tamaño = tamaño
    
    def __str__(self) -> str:
        return f"{self._nombre} ({self._tamaño}): ${self._precio:.2f}"

class Entrada(MenuItem):
    # Entradas con opción para compartir.
    
    def __init__(self, nombre: str, precio: float, compartido: bool = False):
        super().__init__(nombre, precio)
        self._compartido = compartido
    
    def get_compartido(self) -> bool:
        return self._compartido

    def set_compartido(self, compartido: bool) ->None :
        self._compartido = compartido

    def __str__(self) -> str:
        info_compartir = " (para compartir)" if self._compartido else ""
        return f"{self._nombre}{info_compartir}: ${self._precio:.2f}"

class PlatoPrincipal(MenuItem):
    # plato principal con tipo de proteína.
    
    def __init__(self, nombre: str, precio: float, proteina: str):
        super().__init__(nombre, precio)
        self._proteina = proteina

    def get_proteina(self) ->str:
        return self._proteina
    
    def set_proteina(self, proteina: str) ->None:
        self._proteina = proteina
    
    def __str__(self) -> str:
        return f"{self._nombre} ({self._proteina}): ${self._precio:.2f}"

class Pedido:
    
    def __init__(self, numero_mesa: int):
        self._numero_mesa = numero_mesa
        self.items = []

    def get_numero_mesa(self) ->int:
        return self._numero_mesa
    
    def set_numero_mesa(self, numero_mesa: int) ->None:
        self._numero_mesa = numero_mesa
    
    def agregar_item(self, item: MenuItem) -> None:
        self.items.append(item)
    
    def get_subtotal(self) -> float:
        # Calcular subtotal antes de descuentos.
        return sum(item.get_total() for item in self.items)
    
    def aplicar_descuento(self, subtotal: float) -> tuple:
        """
        Aplicar descuentos basados en la composición del pedido.
        Retorna: (monto_descuento, razon_descuento)
        """
        # Verificar descuento de bebida (bebida gratis por pedido de mas de $25)
        tiene_plato_principal = any(isinstance(item, PlatoPrincipal) for item in self.items)
        contador_bebidas = sum(1 for item in self.items if isinstance(item, Bebida))
        
        if tiene_plato_principal and subtotal > 25 and contador_bebidas > 0:
            # Encontrar la bebida más barata
            bebidas = [item for item in self.items if isinstance(item, Bebida)]
            if bebidas:
                bebida_mas_barata = min(bebidas, key=lambda x: x._precio)
                return bebida_mas_barata._precio, "Bebida gratis por pedido de mas de $25"
        
        return 0.0, "No se aplicó descuento"
    
    def get_total(self) -> float:
        # Calcular total final después de descuentos.
        subtotal = self.get_subtotal()
        monto_descuento, razon_descuento = self.aplicar_descuento(subtotal)
        return subtotal - monto_descuento
    
    def mostrar_factura(self) -> None:
        # Mostrar la factura formateada.
        print(f"\n{'='*50}")
        print(f"MESA {self._numero_mesa} - FACTURA FINAL")
        print(f"{'='*50}")
        
        for i, item in enumerate(self.items, 1):
            print(f"{i:2d}. {item}")
        
        subtotal = self.get_subtotal()
        monto_descuento, razon_descuento = self.aplicar_descuento(subtotal)
        propina = subtotal * 0.05  # 5% de propina
        total_final = subtotal - monto_descuento + propina
        
        print(f"\n{'='*50}")
        print(f"Subtotal: ${subtotal:.2f}")
        if monto_descuento > 0:
            print(f"Descuento: -${monto_descuento:.2f} ({razon_descuento})")
        print(f"propina (5%): ${propina:.2f}")
        print(f"{'-'*50}")
        print(f"TOTAL: ${total_final:.2f}")
        print(f"{'='*50}")


class MetodoDePago:
    def pago(self, monto:float):
        raise NotImplementedError("Metodo de pago no disponible")
    
class PagEnEfectivo(MetodoDePago):
    def __init__(self, dinero_entregado: float):
        super().__init__()
        self.dinero_entregado = dinero_entregado

    def pago(self, monto):
        if self.dinero_entregado >= monto:
            print(f"Pago en efectivo realizado. Cambio: ${self.dinero_entregado - monto:.2f}")
        else:
            print(f"fondos insuficiente. falta ${monto - self.dinero_entregado:.2f}")

class PagoConTarjeta(MetodoDePago):
    def __init__(self, numero_de_tarjeta: str, cvv: int):
        super().__init__()
        self.__numero_de_tarjeta = numero_de_tarjeta
        self.__cvv = cvv

    def pago(self, monto: float):
        print(f"Pagando ${monto:.2f} con la tarjete terminada en {self.__numero_de_tarjeta[-4:]}")


def crear_menu():
    menu = [
        # Bebidas
        Bebida("Coca-Cola", 2.50, "regular"),
        Bebida("Té Helado", 2.25, "regular"),
        Bebida("Café", 2.00, "regular"),
        Bebida("Jugo de Naranja Natural", 4.50, "grande"),
        Bebida("Agua Mineral", 1.50, "pequeño"),
        
        # Entradas
        Entrada("Palitos de Mozzarella", 8.99),
        Entrada("Alitas de Pollo", 12.99, True),
        Entrada("Pan de Ajo", 5.99),
        Entrada("Nachos", 10.99, True),
        Entrada("Sopa del Día", 6.99),
        
        # Platos Principales
        PlatoPrincipal("Salmón a la Parrilla", 22.99, "salmón"),
        PlatoPrincipal("Filete Ribeye", 28.99, "res"),
        PlatoPrincipal("Pollo a la Parmesana", 18.99, "pollo"),
        PlatoPrincipal("Pasta Vegetariana", 16.99, "vegetariano"),
        PlatoPrincipal("Hamburguesa BBQ", 15.99, "res"),
        PlatoPrincipal("Ensalada César", 12.99, "pollo"),
        PlatoPrincipal("Lasagna", 17.99, "res"),
        PlatoPrincipal("Pescado del Día", 24.99, "pescado")
    ]
    return menu

def mostrar_menu(menu):
    """Mostrar el menú disponible."""
    print(f"\n{'='*40}")
    print("MENÚ DEL RESTAURANTE")
    print(f"{'='*40}")
    
    print("\n--- BEBIDAS ---")
    for i, item in enumerate(menu[:5], 1):
        print(f"{i:2d}. {item}")
    
    print("\n--- ENTRADAS ---")
    for i, item in enumerate(menu[5:10], 6):
        print(f"{i:2d}. {item}")
    
    print("\n--- PLATOS PRINCIPALES ---")
    for i, item in enumerate(menu[10:], 11):
        print(f"{i:2d}. {item}")

def demo_sistema():
    # Crear menú
    menu = crear_menu()
    
    # Mostrar menú disponible
    mostrar_menu(menu)
    
    # Crear un pedido de ejemplo
    pedido1 = Pedido(numero_mesa=5)

    # Agregar items al pedido (simulando una orden real)
    pedido1.agregar_item(menu[5])   # Palitos de Mozzarella
    pedido1.agregar_item(menu[6])   # Alitas de Pollo (compartido)
    pedido1.agregar_item(menu[10])  # Salmón a la Parrilla
    pedido1.agregar_item(menu[0])   # Coca-Cola
    pedido1.agregar_item(menu[4])   # Agua mineral
    pedido1.agregar_item(menu[15])  # Ensalada César
    
    pedido1.mostrar_factura()

    #pago en efectivo
    total = pedido1.get_total()
    Pago_Efectivo = PagEnEfectivo(70)
    Pago_Efectivo.pago(total)

    print(f"\n{'='*50}")

    #pago con tarjeta
    Pago_tarjeta = PagoConTarjeta("284303484336" , 7520 )
    Pago_tarjeta.pago(total)

    print(f"\n{'='*50}")

demo_sistema()