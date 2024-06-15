import { db } from "$repo/db";


export async function load() {
  return {dashboards: await db.query.prompts.findMany({
    
  })}
}