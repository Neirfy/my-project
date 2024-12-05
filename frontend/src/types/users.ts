import { Base } from "./api";
import { User } from "./auth";
import { Pagination } from "./pagination";

export type UsersResponse = Base<Pagination<User>>
