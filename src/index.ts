import 'dotenv/config'
import { sql } from '@vercel/postgres'

const result = await sql`SELECT * FROM Reports`
console.log(result.rows)
