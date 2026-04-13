import type { Mascota } from "./mascota"
import type { Veterinario } from "./veterinario"

export interface Turno {
  id?: number
  fecha_hora: string
  motivo: string
  estado: string
  mascota: Mascota
  veterinario: Veterinario
}
