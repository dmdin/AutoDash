import {db} from '$repo/db'

export async function load() {
  return {
    templates: await db.query.savedTemplates.findMany(), 
    sources: await db.query.sources.findMany(),
  }
}