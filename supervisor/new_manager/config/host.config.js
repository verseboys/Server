'use strict'
import config from '../config'

let host = config.env.dev?config.env.devService:config.env.proService

export default {
    host
}