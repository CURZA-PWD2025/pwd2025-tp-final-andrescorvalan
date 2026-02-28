import { ref } from 'vue';

// Variable para mantener la ultima seccion visitada (entidad especie, mascota, etc.)
// Se usa para determinar si se debe leer desde la base de datos (al entrar a la seccion)
// o no (cuando navagamos dentro de la seccion)
export const ultimaEntidadVisitada = ref<string | null>(null);

export function usarNavegacion() {
  const debeRefrescar = (nombreEntidad: string): boolean => {
    // Si se quiere ir a una nueva seccion, leer de la base de datos (True)
    if (ultimaEntidadVisitada.value !== nombreEntidad) {
      ultimaEntidadVisitada.value = nombreEntidad;
      return true;
    }
    // Si es la misma seccion usar solo el store (False)
    return false;
  };

  return { debeRefrescar };
}