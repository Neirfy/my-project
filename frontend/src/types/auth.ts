import { Token } from "@/api/types";
import { Base } from "./api";

type Departapent = {
  name: string,
  parent_id: number,
  sort: number,
  leader: string,
  phone: string,
  email: string,
  status: number,
  id: number,
  del_flag: boolean,
  created_time: string,
  updated_time: string
}

type Menu = {
  title: string,
  name: string,
  parent_id: number,
  sort: number,
  icon: string,
  path: string,
  menu_type: number,
  component: string,
  perms: string,
  status: number,
  show: number,
  cache: number,
  remark: string,
  id: number,
  created_time: string,
  updated_time: string
}

type Role = {
  name: string,
  data_scope: number,
  status: number,
  remark: string,
  id: number,
  created_time: string,
  updated_time: string,
  menus: Menu[]
}

export type User = {
  dept_id: number,
  username: string,
  nickname: string,
  fio: string,
  email: string,
  phone: string,
  id: number,
  uuid: string,
  avatar: string,
  status: number,
  is_superuser: boolean,
  is_staff: boolean,
  is_multi_login: boolean,
  join_time: string,
  last_login_time: string,
  dept: Departapent,
  roles: Role[]
}

export type UserRegister  = {
  username: string,
  password: string,
  nickname: string,
  fio: string,
  email: string
}

export type UserUpdate = {
  dept_id: number,
  username: string,
  nickname: string,
  fio: string,
  email: string
  phone: string,
}

type Login = {
  user: User
} & Token

export type LoginResponse = Base<Login>
export type UserMeResponse = Base<User>
