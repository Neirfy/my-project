export enum Post {
  register = '/user/register',
  login = '/auth/login',
  logout = '/auth/logout',
  smart = '/b24/create_smart',
  // partners= '/sales_returns',
  // profit = '/profit',
  // disputs = '/disputs',
}

export enum Get {
  refresh = '/auth/token/new',
  me = '/user/me',
  productsSearchWithQuantity = '/b24/search_products_with_quantity',
  builgingsSearch = '/b24/search_object',
  users = '/user/list'
}

export enum Put {
  updateUser = '/user'
}

export enum Delete {
  user = '/user'
}

export type Methods = 'GET' | 'PUT' | 'POST' | 'DELETE'

export type Token = {
  access_token: string
  token_type: string
}
