import os
import platform
import sys
from collections import OrderedDict


class LRUSimulator:
    def __init__(self):
        self.page_frames = OrderedDict()
        self.page_faults = 0
        self.page_size = 0
        self.frame_count = 0
        self.addresses = []
        self.page_numbers = []
        self.separator = ','

    def clear(self):
        """Clear console screen reliably across platforms"""
        if platform.system() == "Windows":
            os.system('cls')
        else:
            os.system('clear')
    def read_addresses_from_file(self):
        """Read addresses from a text file in format '0100,0822,0555'"""
        while True:
            filename = input("Ingrese el nombre del archivo (ej., addresses.txt): ").strip()
            try:
                with open(filename, 'r') as file:
                    content = file.read().strip()
                    self.addresses = [addr.strip() for addr in content.split(self.separator) if addr.strip()]
                    for address in self.addresses:
                        try:
                            page_num = int(address)
                        except ValueError:
                            print(f"Formato de dirección inválido: {self.addresses}")
                            self.run_again()
        
                    print(f"Se encontraron {len(self.addresses)} direcciones en este archivo: {filename}.")
                    if len(self.addresses) == 0:
                        self.run_again()
   
                    confirmation = input('¿Desea continuar? (y/n): ').lower().strip()
                    if confirmation == 'y':
                        return True
  
            except FileNotFoundError:
                print(f"Error: Archivo '{filename}' no encontrado.")
                choice = input("¿Desea intentar de nuevo o con otro archivo? (y/n): ").lower().strip()
                self.exit_program(choice)
            except Exception as e:
                print(f"Error: {e}")
                choice = input("¿Desea intentar con otro archivo? (y/n): ").lower().strip()
                self.exit_program(choice)
            
               
    def exit_program(self,choice):
         if choice == 'n':
                    exit_choice = input("¿Deseas salir del programa? (y/n)")
                    if exit_choice == 'y':
                        print("Cerrando el programa de simulación...")
                        sys.exit(0)
                    else: 
                        self.clear()

    def get_page_size(self):
        """Prompt user for page size in bytes"""
        while True:
            try:
                self.page_size = int(input("\nIngresa el tamaño de página en bytes (ej., 200): "))
                if self.page_size <= 0:
                    print("El tamaño de página debe ser un número positivo.")
                    continue
                confirmation = input(f'Tamaño de página: {self.page_size} Desea continuar? (y/n) ')
                if confirmation == "y":
                    return True
            except ValueError:
                print("El tamaño de página debe ser un número entero.")
    
    def get_frame_count(self):
        """Prompt user for number of frames in physical memory"""
        while True:
            try:
                self.frame_count = int(input("\nIngrese el número de frames disponibles en memoria física: "))
                if self.frame_count <= 0:
                    print("El número de frames debe ser un número positivo.")
                    continue
                print(f'Número de frames: {self.frame_count}')
                confirmation = input(f'Desea continuar? (y/n) ')
                if confirmation == "y":
                    return True
            except ValueError:
                print("El número de frames debe ser un número entero.")
    
    def calculate_page_numbers(self):
        """Convert the adresses string to page reference string"""
        self.page_numbers = []
        for address in self.addresses:
            try:
                page_num = int(address) // self.page_size 
                self.page_numbers.append(page_num)
            except ValueError:
                print(f"Formato de dirección inválido: {address}")
                self.run_again()
        
    
    def simulate_lru(self):
        """Perform LRU simulation on the page numbers"""
        if not self.page_numbers:
            print("No hay páginas en el String de Referencia.")
            self.run_again()
        
        self.page_frames = OrderedDict()
        self.page_faults = 0
        
        print("==============================")
        print("\nEmpezando la simulación de LRU...")
        print(f"\nTamaño de Página: {self.page_size} bytes")
        print(f"Número de Frames: {self.frame_count}")
        print(f"Direcciones Totales: {len(self.addresses)}")
        print(f"String de Referencia: {self.page_numbers}")

        for i, page_num in enumerate(self.page_numbers, 1):
            print(f"\nProcesando la dirección {i}/{len(self.page_numbers)}: {self.addresses[i-1]} -> Página {page_num}")
            
            if page_num in self.page_frames:
                # Page is in memory, move to end to mark as recently used
                self.page_frames.move_to_end(page_num)
                print(f"Página {page_num} ya en memoria. Actualizando su uso.")
            else:
                # Page fault occurred
                self.page_faults += 1
                print(f"--> Falta de Página! Cargando la página {page_num} en memoria.")
                print(f"Número de faltas actual: {self.page_faults}.")
                if len(self.page_frames) >= self.frame_count:
                    # Remove least recently used page
                    lru_page, _ = self.page_frames.popitem(last=False)
                    print(f"Removiendo la página {lru_page} para hacer espacio.")
                
                # Add new page
                self.page_frames[page_num] = True
                print(f"Página {page_num} agregada a memoria.")
            
            # Display current memory state
            self.display_memory_state()
        
        print("\nSimulación completada!")
        print(f"Total de Faltas de Página: {self.page_faults}")
        print("==============================")
    
    def display_memory_state(self):
        """Display current pages in memory"""
        pages = list(self.page_frames.keys())
        print(f"Número de páginas en memoria (MRU -> LRU): {pages}")
    
    def run_again(self):
        run_again = input("\nDeseas realizar otra simulación? (y/n): ")
        if run_again == "y":
            self.clear()
            self.run()
        else: 
            print("Cerrando el programa de simulación...")
            sys.exit(0)

    def run(self):
        """Main execution method"""
        print("Simulador de LRU: Reemplazo de páginas")
        print("==============================")
        
        # Get input file
        
        if not self.read_addresses_from_file():
            return
        
        # Get page size
        if not self.get_page_size():
            return
        
        # Get frame count
        if not self.get_frame_count():
            return
        
        # Calculate page numbers
        self.calculate_page_numbers()
        
        # Run simulation
        self.simulate_lru()

        # Run another simulation
        self.run_again()

if __name__ == "__main__":
    simulator = LRUSimulator()
    simulator.run()