import type { Especialidad } from './Especialidad'

export interface Veterinario {
  id?: number
  nombre: string
  apellido: string
  matricula: string
  telefono: string
  email: string
  especialidades: Especialidad[] | number[]
}