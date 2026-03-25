import type { Especialidad } from './especialidad'

export interface Veterinario {
  id?: number
  nombre: string
  apellido: string
  matricula: string
  telefono: string
  email: string
  especialidades: Especialidad[] | number[]
}