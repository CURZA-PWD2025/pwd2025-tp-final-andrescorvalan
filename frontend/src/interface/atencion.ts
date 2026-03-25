import type { Mascota } from "./mascota"
import type { Veterinario } from "./veterinario"

export interface Atencion {
  id?: number
  fecha: string
  diagnostico: string
  tratamiento: string
  observaciones: string
  mascota: Mascota
  veterinario: Veterinario
}
