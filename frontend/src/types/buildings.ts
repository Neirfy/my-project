import { Base } from "./api";
import { Pagination } from "./pagination";

export type Building = {
  id: number,
  name: string,
  address: string,
}

export type BuildingResponse = Base<Pagination<Building>>
