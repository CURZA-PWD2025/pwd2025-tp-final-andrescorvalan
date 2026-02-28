import type { Especie } from "./Especie"
import type { Propietario } from "./Propietario"

export interface Mascota {
  id?: number
  nombre: string
  fecha_nac: string
  propietario: Propietario
  especie: Especie
}
