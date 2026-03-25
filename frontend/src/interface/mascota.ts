import type { Especie } from "./especie"
import type { Propietario } from "./propietario"

export interface Mascota {
  id?: number
  nombre: string
  fecha_nac: string
  sexo: string
  propietario: Propietario
  especie: Especie
}
