import { eq } from "drizzle-orm"

import { users } from "$schema"
import { db } from "$repo/db"

export async function getUser(id: string) {
  return db.query.users.findFirst({
    where: eq(users.id, id)
  })
}
